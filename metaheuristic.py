from simpleHeuristic import SimpleHeuristic, heuristicComparison
from knapsack import Knapsack, Item
from IO import saveDataCSV
from features import features, getAllFeatures
import numpy as np

class Metaheuristic(object):
    def __init__(self):
        self.sequenceHeuristics = []

    def addHeuristic(self, heuristicName: str):
        self.sequenceHeuristics.append(heuristicName)
    
    def solveInstance(self, C, items = [Item]):
        kp = Knapsack(C)
        for heuristicName in self.sequenceHeuristics:
            heuristic = SimpleHeuristic(heuristicName)
            nextItem = heuristic.nextItem(kp, items)
            if nextItem is not None:
                kp.pack(items[nextItem])
                items.pop(nextItem)
        return kp, items
    
    def convertToDict(self, C, items = [Item]):
        kp = Knapsack(C)
        featureDataFrame = []
        for heuristicName in self.sequenceHeuristics:
            featureDict = dict()
            featureValues = getAllFeatures(items)
            for name, value in zip(features.keys(), featureValues):
                featureDict[name] = value
            featureDict['NextHeuristic'] = heuristicName
            featureDataFrame.append(featureDict)

            heuristic = SimpleHeuristic(heuristicName)
            nextItem = heuristic.nextItem(kp, items)
            if nextItem is not None:
                kp.pack(items[nextItem])
                items.pop(nextItem)
        saveDataCSV("traindata.csv", featureDataFrame, features.keys()+["NextHeuristic"])

    def copy(self):
        mh_copy = Metaheuristic()
        mh_copy.sequenceHeuristics = self.sequenceHeuristics.copy()
        return mh_copy

    def __str__(self):
        mh_str = "mh:\t"
        for sh in self.sequenceHeuristics:
            mh_str += "\n\t"+sh
        return mh_str


def SimulatedAnnealing(kp: Knapsack, items = [Item], n_iterations = 1001, temp = 200, stopCriteria = 10):
    np.random.seed(0)

    mh = Metaheuristic()
    heuristicNames = list(heuristicComparison.keys())
    countNone = 0

    kp_best = kp.copy()
    mh_best = Metaheuristic()
    for i in range(1, n_iterations):
        if countNone == stopCriteria:
            break
        
        nextHeuristic = np.random.choice(heuristicNames)
        nextItem = SimpleHeuristic(nextHeuristic).nextItem(kp, items)
        if nextItem == None:
            countNone += 1
            continue        
        countNone = 0
        kp_candidate = kp.copy()
        kp_candidate.pack(items[nextItem])

        if kp_best.getValue() < kp_candidate.getValue():
            kp_best = kp_candidate
            mh_best = mh.copy()
            mh_best.addHeuristic(nextHeuristic)

        diff = kp.getValue() - kp_candidate.getValue() 
        t = temp/np.log(i+1)
        metropolis = np.exp(-diff/t)
        if diff < 0 or np.random.rand() < metropolis:
            kp.pack(items[nextItem])
            items.pop(nextItem)
            mh.addHeuristic(nextHeuristic)
        else:
            countNone += 1

    #print(mh_best)
    return kp_best.getValue()

def RandomSearch(kp: Knapsack, items = [Item], stopCriteria = 10):
    np.random.seed(0)

    mh = Metaheuristic()
    heuristicNames = list(heuristicComparison.keys())
    countNone = 0

    while countNone < stopCriteria:
        nextHeuristic = np.random.choice(heuristicNames)
        nextItem = SimpleHeuristic(nextHeuristic).nextItem(kp, items)
        if nextItem == None:
            countNone += 1
        else:
            countNone = 0
            kp.pack(items[nextItem])
            items.pop(nextItem)
            mh.addHeuristic(nextHeuristic)

    #print(mh)
    return kp.getValue()