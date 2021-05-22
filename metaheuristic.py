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
    
    def cleanHeuristics(self, C, items: [Item]):
        kp = Knapsack(C)
        mh = []
        for heuristicName in self.sequenceHeuristics:
            nextItem = SimpleHeuristic(heuristicName).apply(kp, items)
            if nextItem != None:
                mh.append(heuristicName)
        self.sequenceHeuristics = mh

    def solveInstance(self, C, items: [Item]):
        kp = Knapsack(C)
        for heuristicName in self.sequenceHeuristics:
            SimpleHeuristic(heuristicName).apply(kp, items)
            
        return kp
    
    def convertToDict(self, C, items: [Item], fileName = 'traindata.csv', backTime = 0, overwrite = False):
        flatten = lambda t: [elem for sublist in t for elem in sublist]
        labels = [feature+"_"+str(i) for i in range(backTime, -1, -1) for feature in features.keys()]
        labels.append("NextHeuristic")

        featureDataFrame = []
        featureDict = dict()
        featuresMemory = [[None]*len(features.keys())]*(backTime+1)

        kp = Knapsack(C)
        for heuristicName in self.sequenceHeuristics:
            featuresMemory.pop(0)
            featuresMemory.append(getAllFeatures(items))
            for name, value in zip(labels, flatten(featuresMemory)+[heuristicName]):
                featureDict[name] = value
            featureDataFrame.append(featureDict.copy())

            SimpleHeuristic(heuristicName).apply(kp, items)
        saveDataCSV(fileName, featureDataFrame, labels, overwrite)

    def copy(self):
        mh_copy = Metaheuristic()
        mh_copy.sequenceHeuristics = self.sequenceHeuristics.copy()
        return mh_copy

    def __str__(self):
        mh_str = "mh:\t"
        for sh in self.sequenceHeuristics:
            mh_str += "\n\t"+sh
        return mh_str


def SimulatedAnnealing(kp: Knapsack, items: [Item], n_iterations = 1001, temp = 200, stopCriteria = 10):
    np.random.seed(0)

    mh = Metaheuristic()
    heuristicNames = list(heuristicComparison.keys())
    countNone = 0

    kp_best = kp.copy()
    mh_best = Metaheuristic()
    n_iterations = max(n_iterations, 2*len(items))
    for i in range(1, n_iterations):
        if countNone == stopCriteria:
            break
        
        nextHeuristic = np.random.choice(heuristicNames)
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
        t = temp/np.log(i+1)
        metropolis = np.exp(-diff/t)
        if diff < 0 or np.random.rand() < metropolis:
            kp = kp_candidate
            items = items_candidate
            mh.addHeuristic(nextHeuristic)
        else:
            countNone += 1
    return kp_best, mh_best

def RandomSearch(kp: Knapsack, items = [Item], stopCriteria = 10):
    np.random.seed(0)

    mh = Metaheuristic()
    heuristicNames = list(heuristicComparison.keys())
    countNone = 0

    while countNone < stopCriteria:
        nextHeuristic = np.random.choice(heuristicNames)
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

def solveMetaheuristic(method: str, kp: Knapsack, items: [Item], saveMetaheuristic = False, fileName = 'traindata.csv', backTime = 0, overwrite = False):
    mh = Metaheuristic()
    C = kp.getCapacity()
    items_copy = items.copy()
    if method == 'SimulatedAnnealing':
        kp, mh = SimulatedAnnealing(kp, items)
    else:
        kp, mh = RandomSearch(kp, items)
    if saveMetaheuristic:
        mh.convertToDict(C, items_copy, fileName, backTime, overwrite)
    return kp.getValue()
