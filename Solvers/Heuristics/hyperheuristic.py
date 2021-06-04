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
        # Change the heuristic each time that the norm correlation of the data is greater than 0.5
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
        
        # Train the model for the HH
        if os.path.exists(modelFilename) or trainModel:
            buildModel(modelPath, trainPath)
        self.model = keras.models.load_model(modelPath)
        
        # Prepare the history of the HH
        self.numPrevStates = prevStates
        self.previousStates = []
        self.timeline = dict()   
        df = pd.read_csv(trainPath, dtype={'ID': str})
        self.n_id = len(df.ID.unique())
    
    def reset(self):
        # Reset the history of the HH
        self.previousStates = []
        self.timeline = dict()
    
    def getHeuristic(self, items: List[Item]):
        # Prepare the characterization of the current state
        newState = np.pad(getAllFeatures(items), (0, self.n_id), 'constant')
        self.previousStates.append(newState)
        
        # Prepare the states considered as input for the LSTM model
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
        # Use the LSTM model
        outputModel = self.model.predict(inputModel)[0]

        # Check the history of the HH
        inputModel = str(self.previousStates)
        if inputModel not in self.timeline:
            self.timeline[inputModel] = set()
        for pastMoves in self.timeline[inputModel]:
            outputModel[pastMoves] = 0
        if sum(outputModel) == 0:
            return None
        outputModel /= sum(outputModel)

        if self.choiceSelector == 'probability':    
            # Choice the heuristic interpreting the output of the LSTM as a probability distribution
            nextMove = np.random.choice(range(len(outputModel)), p = outputModel)
        else:
            # Choice the heuristic that has the maximum value in the output
            nextMove = np.argmax(outputModel)
        # Save the heuristic in the history
        self.timeline[inputModel].add(nextMove)
        # Return the chosen heuristic
        return list(heuristicComparison.keys())[nextMove]

def hyperheuristicSolverHH(kp: Knapsack, items: List[Item], hh: Hyperheuristic, stopCritaria = 10):
    # Prepare the HH variables
    hh.reset()
    mh = Metaheuristic()
    kp_best = kp.copy()
    mh_best = mh.copy()
    countNone = 0
    while countNone < stopCritaria:
        # Choice the next heuristic
        nextHeuristic = hh.getHeuristic(items)
        # Apply the heuristic
        nextItem = SimpleHeuristic(nextHeuristic).apply(kp, items)
        if nextItem == None:
            # Reject the heuristic
            countNone += 1
            continue
        countNone = 0
        # Accept the heuristic
        mh.addHeuristic(nextHeuristic)
        # Save the best solution reached
        if kp_best.getValue() < kp.getValue():
            kp_best = kp.copy()
            mh_best = mh.copy()
    # Return the best solution reached
    return kp_best, mh_best


def hyperheuristicSolverMH(kp: Knapsack, items: List[Item], choiceSelector = 'probability', trainModel = False, modelTrainedFilename = 'model_lstm.h5', stopCritaria = 10):
    # Prepare the hyper-heuristic and use it
    hh = Hyperheuristic(choiceSelector, trainModel, modelTrainedFilename)
    # Return the knapsack solution and the sequence of heuristic used
    return hyperheuristicSolverHH(kp, items, hh, stopCritaria)

def hyperheuristicSolver(kp: Knapsack, items: List[Item], choiceSelector = 'probability', trainModel = False, stopCritaria = 10):
    # Return only the knapsack solution
    kp, _ = hyperheuristicSolverMH(kp, items, choiceSelector, trainModel, stopCritaria)
    return kp
