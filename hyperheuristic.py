from segmentTree import STItems
from typing import List
from knapsack import Knapsack, Item
from simpleHeuristic import SimpleHeuristic, heuristicComparison
from metaheuristic import Metaheuristic
from features import getAllFeatures, getFeature
from tensorflow import keras
from LSTMModel import buildModel
import numpy as np
import pandas as pd
import os
class HyperheuristicNaive(object):
    def __init__(self, heuristicNames: List[str]):
        self.currentHeuristic = 0
        self.heuristics = [SimpleHeuristic(name) for name in heuristicNames]
    
    def getHeuristic(self, items: List[Item]):
        pastHeuristic = self.currentHeuristic
        if getFeature("NORM_CORRELATION", items) > 0.5:
            self.currentHeuristic += 1
            self.currentHeuristic %= len(self.heuristics)
        return self.heuristics[pastHeuristic]
    
    def nextItem(self, kp: Knapsack, items: List[Item]):
        return self.getHeuristic(items).nextItem(kp, items)

class Hyperheuristic(object):
    def __init__(self, trainModel = False, modelTrainedFilename = 'lstm_model.h5', trainDataFilename = 'traindata.csv', prevStates = 2):
        tapia_path = "C:/Users/Angel/Documents/Tec/1Semester/Fundamentos/Knapsack_project/Hyper-heuristic-Knapsack/"
        dany_path =  "/Volumes/GoogleDrive/My Drive/MCCNotes/Jlab projects/GITHUB_repositories/DANY_repositories/Hyper-heuristic-Knapsack/"
        ramon_path = dany_path 
        modelPath = tapia_path+modelTrainedFilename
        trainPath = tapia_path+trainDataFilename

        if os.stat(modelPath).st_size == 0 or trainModel:
            buildModel(modelPath, trainPath)
        self.model = keras.models.load_model(modelPath)
        self.numPrevStates = prevStates
        self.previousStates = []
        df = pd.read_csv(trainPath, dtype={'ID': str})
        self.n_id = len(df.ID.unique())
    
    def getHeuristic(self, items: List[Item]):
        newState = np.pad(getAllFeatures(items), (0, self.n_id),'constant')
        self.previousStates.append(newState)
        diffStates = self.numPrevStates - len(self.previousStates)
        if diffStates == -1:
            self.previousStates.pop(0)
            diffStates += 1
        while diffStates > 0:
            self.previousStates.append(newState)
            diffStates -= 1
        inputModel = self.previousStates.copy()
        inputModel = np.array(inputModel)
        inputModel = inputModel.reshape((1, self.numPrevStates, len(inputModel[0])))
        outputModel = self.model.predict(inputModel)

        return list(heuristicComparison.keys())[np.argmax(outputModel)]

def hyperheuristicSolver(kp: Knapsack, items: List[Item], trainModel = False, stopCritaria = 10):
    hh = Hyperheuristic(trainModel)
    mh = Metaheuristic()
    countNones = 0
    while countNones < stopCritaria:
        nextHeuristic = hh.getHeuristic(items)
        nextItem = SimpleHeuristic(nextHeuristic).apply(kp, items)
        if nextItem == None:
            countNones += 1
            continue
        countNones = 0
        mh.addHeuristic(nextHeuristic)
    return kp


def hyperheuristicSolverWithST(kp: Knapsack, items: List[Item], trainModel = False, stopCritaria = 10):
    hh = Hyperheuristic(trainModel)
    mh = Metaheuristic()
    sh = STItems(items)
    countNones = 0
    while countNones < stopCritaria:
        nextHeuristic = hh.getHeuristic(items)
        nextItem, idx = sh.nextItem(nextHeuristic, kp.getCapacity())
        if nextItem == None:
            countNones += 1
            continue
        countNones = 0
        sh.eraseItem(idx)
        kp.pack(nextItem)
        items.remove(nextItem)
        mh.addHeuristic(nextHeuristic)
    return kp

