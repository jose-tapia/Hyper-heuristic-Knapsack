from time import perf_counter
import numpy as np
from Solvers.Heuristics.hyperheuristic import (Hyperheuristic,
                                               hyperheuristicSolverHH)
from Solvers.Heuristics.LSTM import generateTrainDataset
from Solvers.Heuristics.simpleHeuristic import heuristicComparison
from Solvers.solvers import solver
from Utils.IO import loadInstance, obtainFilenames, saveDictCSV, tapia_path
from Utils.knapsack import Knapsack, generateItemList

if __name__ == '__main__':

    # To replicate the reported results, use:
    #   trainDataset = 'OrtizBayliss_Train'  
    #   testDataset = 'Pisinger'
    #   trainPath = 'Cache/traindata.csv'
    #   modelPath = 'Cache/hh_lstm.h5'
    #   resultPath = 'Cache/Performance.csv'

    trainDataset = 'OrtizBayliss_Train'
    testDataset = 'Pisinger'
    trainPath = 'Cache/traindata.csv' 
    modelPath = 'Cache/hh_lstm.h5'
    resultPath = 'Cache/Performance.csv'

    # First phase
    generateTrainDataset(trainPath, True, trainDataset)

    # Second phase
    HH = []
    for i in range(10):
        HH.append(Hyperheuristic('probability', trainModel = True, modelFilename = modelPath, trainFilename = trainPath, prevStates = 2))

    # Third phase
    heuristics = list(heuristicComparison.keys())[:4]
    resultsTestDict = dict()    
    methods = heuristics+['SimulatedAnnealing', 'RandomSearch', 'Hyperheuristic', 'MILP']
    methodIterations = [1, 1, 1, 1, 10, 10, 10, 1]
    for method in methods:
        resultsTestDict[method] = []
        resultsTestDict[f'{method}_time'] = []
        
    instances = obtainFilenames(tapia_path, testDataset)
    for instance in instances:
        n, W, weights, profits = loadInstance(instance)

        for method, iterations in zip(methods, methodIterations):
            sumResults, sumTime = 0, 0
            for i in range(iterations):
                kp = Knapsack(W)
                items = generateItemList(weights, profits)

                start = perf_counter()
                if method == 'Hyperheuristic':
                    kp, mh = hyperheuristicSolverHH(kp, items, HH[i])
                    result = kp.getValue()
                else:
                    result = solver(method, kp, items)
                end = perf_counter()
                sumResults += result 
                sumTime += end-start
            resultsTestDict[method].append(sumResults/iterations)
            resultsTestDict[f'{method}_time'].append(sumTime/iterations)
    
    saveDictCSV(resultPath, resultsTestDict)
