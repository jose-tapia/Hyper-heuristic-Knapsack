from typing import List
import numpy as np
from Solvers.Heuristics.simpleHeuristic import (SimpleHeuristic,
                                                heuristicComparison)
from Utils.features import featuresCalculation, getAllFeatures
from Utils.IO import saveDataCSV
from Utils.knapsack import Item, Knapsack


class Metaheuristic(object):
    def __init__(self):
        self.sequenceHeuristics = []

    def addHeuristic(self, heuristicName: str):
        self.sequenceHeuristics.append(heuristicName)
    
    def cleanHeuristics(self, W: int, items: List[Item]):
        kp = Knapsack(W)
        mh = []
        for heuristic in self.sequenceHeuristics:
            nextItem = SimpleHeuristic(heuristic).apply(kp, items)
            if nextItem != None:
                mh.append(heuristic)
        self.sequenceHeuristics = mh

    def solveInstance(self, W: int, items: List[Item]):
        kp = Knapsack(W)
        for heuristic in self.sequenceHeuristics:
            SimpleHeuristic(heuristic).apply(kp, items)
        return kp
    
    def saveMetaheuristic(self, W: int, items: List[Item], fileName = 'traindata.csv', overwrite = False):
        labels = list(featuresCalculation.keys())+['NextHeuristic']

        featureDataFrame = []
        featureDict = dict()

        kp = Knapsack(W)
        for heuristic in self.sequenceHeuristics:
            values = getAllFeatures(items) + [heuristic]
            for name, value in zip(labels, values):
                featureDict[name] = value
            featureDataFrame.append(featureDict.copy())

            SimpleHeuristic(heuristic).apply(kp, items)
        saveDataCSV(fileName, featureDataFrame, labels, overwrite)
    
    def stats(self):
        mhstats = dict()
        for heuristic in list(heuristicComparison.keys()):
            mhstats[heuristic] = 0
        for heuristic in self.sequenceHeuristics:
            mhstats[heuristic] += 1
        return mhstats

    def copy(self):
        mh_copy = Metaheuristic()
        mh_copy.sequenceHeuristics = self.sequenceHeuristics.copy()
        return mh_copy
    def __str__(self):
        mh_str = "mh:\t\n"
        for sh in self.sequenceHeuristics:
            mh_str += "\t"+sh+'\n'
        return mh_str


def SimulatedAnnealing(kp: Knapsack, items: List[Item], n_iterations = 100, temp = 200, stopCriteria = 10):
    mh = Metaheuristic()
    heuristics = list(heuristicComparison.keys())
    countNone = 0

    kp_best = kp.copy()
    mh_best = Metaheuristic()
    n_iterations = max(n_iterations, 2*len(items))
    for i in range(n_iterations):
        if countNone == stopCriteria:
            break
        
        nextHeuristic = np.random.choice(heuristics)
        kp_candidate = kp.copy()
        items_candidate = items.copy()
        nextItem = SimpleHeuristic(nextHeuristic).apply(kp_candidate, items_candidate)
        if nextItem == None:
            countNone += 1
            continue        
        countNone = 0

        if kp_best.getValue() < kp_candidate.getValue():
            kp_best = kp_candidate.copy()
            mh_best = mh.copy()
            mh_best.addHeuristic(nextHeuristic)

        diff = kp.getValue() - kp_candidate.getValue()
        t = temp/(i+1)
        if -10 <= -diff/t and -diff/t <= 0:
            metropolis = np.exp(-diff/t)
        elif -diff/t <= -10:
            metropolis = 0
        else:
            metropolis = 1
        if diff < 0 or np.random.rand() <= metropolis:
            kp = kp_candidate
            items = items_candidate
            mh.addHeuristic(nextHeuristic)
        else:
            countNone += 1
    return kp_best, mh_best

def RandomSearch(kp: Knapsack, items: List[Item], stopCriteria = 10):
    mh = Metaheuristic()
    heuristics = list(heuristicComparison.keys())
    countNone = 0

    while countNone < stopCriteria:
        nextHeuristic = np.random.choice(heuristics)
        kp_candidate = kp.copy()
        items_candidate = items.copy()
        nextItem = SimpleHeuristic(nextHeuristic).apply(kp_candidate, items_candidate)

        if nextItem == None or kp_candidate.getValue() <= kp.getValue():
            countNone += 1
            continue
        countNone = 0

        kp = kp_candidate
        items = items_candidate
        mh.addHeuristic(nextHeuristic)
    return kp, mh

def solveMetaheuristic(method: str, kp: Knapsack, items: List[Item], saveMetaheuristic = False, fileName = 'traindata.csv', overwrite = False):
    W = kp.getCapacity()
    items_copy = items.copy()

    if method == 'SimulatedAnnealing':
        kp, mh = SimulatedAnnealing(kp, items)
    elif method == 'RandomSearch':
        kp, mh = RandomSearch(kp, items)
    else:
        return 0
        
    if saveMetaheuristic:
        mh.saveMetaheuristic(W, items_copy, fileName, overwrite)
    return kp.getValue()
