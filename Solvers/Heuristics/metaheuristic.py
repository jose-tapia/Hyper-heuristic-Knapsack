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
        # Only considered heuristics that changes the instance
        kp = Knapsack(W)
        mh = []
        for heuristic in self.sequenceHeuristics:
            nextItem = SimpleHeuristic(heuristic).apply(kp, items)
            if nextItem != None:
                mh.append(heuristic)
        self.sequenceHeuristics = mh

    def solveInstance(self, W: int, items: List[Item]):
        # Apply the sequence of heuristics saved in the given instance
        kp = Knapsack(W)
        for heuristic in self.sequenceHeuristics:
            SimpleHeuristic(heuristic).apply(kp, items)
        return kp
    
    def saveMetaheuristic(self, W: int, items: List[Item], fileName = 'traindata.csv', overwrite = False):
        # Save the sequence of heuristics in a CSV file
        labels = list(featuresCalculation.keys())+['NextHeuristic']

        featureDataFrame = []
        featureDict = dict()

        kp = Knapsack(W)
        for heuristic in self.sequenceHeuristics:
            # Obtain the characterization of the instance and store it
            values = getAllFeatures(items) + [heuristic]
            for name, value in zip(labels, values):
                featureDict[name] = value
            featureDataFrame.append(featureDict.copy())

            SimpleHeuristic(heuristic).apply(kp, items)
        # Save the sequence of characterization in a CSV file
        saveDataCSV(fileName, featureDataFrame, labels, overwrite)
    
    def stats(self):
        # Obtain the repetitions of the heuristics for the given sequence
        mhstats = dict()
        for heuristic in list(heuristicComparison.keys()):
            mhstats[heuristic] = 0
        for heuristic in self.sequenceHeuristics:
            mhstats[heuristic] += 1
        return mhstats

    def copy(self):
        # Deep copy of the class
        mh_copy = Metaheuristic()
        mh_copy.sequenceHeuristics = self.sequenceHeuristics.copy()
        return mh_copy

    def __str__(self):
        # Convert the class to str method
        mh_str = 'mh:\t\n'
        for sh in self.sequenceHeuristics:
            mh_str += '\t'+sh+'\n'
        return mh_str


def SimulatedAnnealing(kp: Knapsack, items: List[Item], n_iterations = 100, temp = 200, stopCriteria = 10):
    # Simulated Annealing implementation
    #  Initialization of the variables
    mh = Metaheuristic()
    heuristics = list(heuristicComparison.keys())
    countNone = 0

    kp_best = kp.copy()
    mh_best = Metaheuristic()
    n_iterations = max(n_iterations, 2*len(items))
    for i in range(n_iterations):
        if countNone == stopCriteria:
            # Stop criteria met
            break
        
        # Choice randomly the next heuristic
        nextHeuristic = np.random.choice(heuristics)
        kp_candidate = kp.copy()
        items_candidate = items.copy()
        nextItem = SimpleHeuristic(nextHeuristic).apply(kp_candidate, items_candidate)
        if nextItem == None:
            # Heuristic does not change the instance
            countNone += 1
            continue        
        countNone = 0

        if kp_best.getValue() < kp_candidate.getValue():
            # Heuristic improve the performance of the solution
            kp_best = kp_candidate.copy()
            mh_best = mh.copy()
            mh_best.addHeuristic(nextHeuristic)

        # Calculate the metropolis variable
        diff = kp.getValue() - kp_candidate.getValue()
        t = temp/(i+1)
        if -10 <= -diff/t and -diff/t <= 0:
            metropolis = np.exp(-diff/t)
        elif -diff/t <= -10:
            metropolis = 0
        else:
            metropolis = 1
        # Acceptance criteria
        if diff < 0 or np.random.rand() <= metropolis:
            kp = kp_candidate
            items = items_candidate
            mh.addHeuristic(nextHeuristic)
        else:
            countNone += 1
    # Return the best solution reached
    return kp_best, mh_best

def RandomSearch(kp: Knapsack, items: List[Item], stopCriteria = 10):
    # Random Search implementation

    #  Initialize the variables
    mh = Metaheuristic()
    heuristics = list(heuristicComparison.keys())
    countNone = 0

    while countNone < stopCriteria:
        # Choice randomly the next heuristic
        nextHeuristic = np.random.choice(heuristics)
        kp_candidate = kp.copy()
        items_candidate = items.copy()
        nextItem = SimpleHeuristic(nextHeuristic).apply(kp_candidate, items_candidate)

        if nextItem == None or kp_candidate.getValue() <= kp.getValue():
            # Reject the heuristic
            countNone += 1
            continue
        countNone = 0

        # Accept the heuristic
        kp = kp_candidate
        items = items_candidate
        mh.addHeuristic(nextHeuristic)
    return kp, mh

def solveMetaheuristic(method: str, kp: Knapsack, items: List[Item], saveMetaheuristic = False, fileName = 'traindata.csv', overwrite = False):
    W = kp.getCapacity()
    items_copy = items.copy()

    # Execute the chosen method
    if method == 'SimulatedAnnealing':
        kp, mh = SimulatedAnnealing(kp, items)
    elif method == 'RandomSearch':
        kp, mh = RandomSearch(kp, items)
    else:
        return 0
    
    # Save the sequence of heuristics
    if saveMetaheuristic:
        mh.saveMetaheuristic(W, items_copy, fileName, overwrite)
    return kp.getValue()
