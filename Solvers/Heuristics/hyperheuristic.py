import os
from typing import List
import numpy as np
import pandas as pd
from Solvers.Heuristics.LSTM import buildModel
from Solvers.Heuristics.metaheuristic import Metaheuristic
from Solvers.Heuristics.simpleHeuristic import (SimpleHeuristic,
                                                heuristicComparison)
from tensorflow import keras
from Utils.features import getAllFeatures, getFeature
from Utils.IO import tapia_path
from Utils.knapsack import Item, Knapsack


class HyperheuristicNaive(object):
    def __init__(self, heuristicNames: List[str]):
        self.currentHeuristic = 0
        self.heuristics = [SimpleHeuristic(name) for name in heuristicNames]
    
    def getHeuristic(self, items: List[Item]):
        pastHeuristic = self.currentHeuristic
        if getFeature('NORM_CORRELATION', items) > 0.5:
            self.currentHeuristic += 1
            self.currentHeuristic %= len(self.heuristics)
        return self.heuristics[pastHeuristic]
    
    def nextItem(self, kp: Knapsack, items: List[Item]):
        return self.getHeuristic(items).nextItem(kp, items)

class Hyperheuristic(object):
    def __init__(self, choiceSelector = 'probability', trainModel = False, modelFilename = 'lstm_model.h5', trainFilename = 'traindata.csv', prevStates = 2):
        modelPath = tapia_path + modelFilename
        trainPath = tapia_path + trainFilename
        
        self.choiceSelector = choiceSelector
        
        if os.path.exists(modelFilename) or trainModel:
            buildModel(modelPath, trainPath)
        self.model = keras.models.load_model(modelPath)
        
        self.numPrevStates = prevStates
        self.previousStates = []
        self.timeline = dict()   
        df = pd.read_csv(trainPath, dtype={'ID': str})
        self.n_id = len(df.ID.unique())
    
    def reset(self):
        self.previousStates = []
        self.timeline = dict()
    
    def getHeuristic(self, items: List[Item]):
        newState = np.pad(getAllFeatures(items), (0, self.n_id), 'constant')
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
        outputModel = self.model.predict(inputModel)[0]

        inputModel = str(self.previousStates)
        if inputModel not in self.timeline:
            self.timeline[inputModel] = set()
        for pastMoves in self.timeline[inputModel]:
            outputModel[pastMoves] = 0
        if sum(outputModel) == 0:
            return None
        outputModel /= sum(outputModel)

        if self.choiceSelector == 'probability':    
            nextMove = np.random.choice(range(len(outputModel)), p = outputModel)
        else:
            nextMove = np.argmax(outputModel)
        self.timeline[inputModel].add(nextMove)
        return list(heuristicComparison.keys())[nextMove]

def hyperheuristicSolverHH(kp: Knapsack, items: List[Item], hh: Hyperheuristic, stopCritaria = 10):
    hh.reset()
    mh = Metaheuristic()
    kp_best = kp.copy()
    mh_best = mh.copy()
    countNone = 0
    while countNone < stopCritaria:
        nextHeuristic = hh.getHeuristic(items)
        nextItem = SimpleHeuristic(nextHeuristic).apply(kp, items)
        if nextItem == None:
            countNone += 1
            continue
        countNone = 0
        mh.addHeuristic(nextHeuristic)
        if kp_best.getValue() < kp.getValue():
            kp_best = kp.copy()
            mh_best = mh.copy()
    return kp_best, mh_best


def hyperheuristicSolverMH(kp: Knapsack, items: List[Item], choiceSelector = 'probability', trainModel = False, modelTrainedFilename = 'model_lstm.h5', stopCritaria = 10):
    hh = Hyperheuristic(choiceSelector, trainModel, modelTrainedFilename)
    return hyperheuristicSolverHH(kp, items, hh, stopCritaria)

def hyperheuristicSolver(kp: Knapsack, items: List[Item], choiceSelector = 'probability', trainModel = False, stopCritaria = 10):
    kp, mh = hyperheuristicSolverMH(kp, items, choiceSelector, trainModel, stopCritaria)
    return kp
