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
    #  Prepare the train dataset for the hyper-heuristic models
    generateTrainDataset(trainPath, True, trainDataset)

    # Second phase
    #  Train the ten hyper-heuristics based on LSTM
    HH = []
    for i in range(10):
        HH.append(Hyperheuristic('probability', trainModel = True, modelFilename = modelPath, trainFilename = trainPath, prevStates = 2))

    # Third phase
    #  Determine the methods to compare
    heuristics = list(heuristicComparison.keys())[:4]  
    methods = heuristics+['SimulatedAnnealing', 'RandomSearch', 'Hyperheuristic', 'MILP']
    #  Determine the number of times that each method will be repeated
    methodIterations = [1, 1, 1, 1, 10, 10, 10, 1]
    #  Prepare the dict to save the data
    resultsTestDict = dict()  
    for method in methods:
        resultsTestDict[method] = []
        resultsTestDict[f'{method}_time'] = []
    
    #  Obtain the path to each test instance 
    instances = obtainFilenames(tapia_path, testDataset)
    for instance in instances:
        # Read the instance
        n, W, weights, profits = loadInstance(instance)

        for method, iterations in zip(methods, methodIterations):
            sumResults, sumTime = 0, 0
            for i in range(iterations):
                kp = Knapsack(W)
                items = generateItemList(weights, profits)

                start = perf_counter()
                if method == 'Hyperheuristic':
                    # Run the respective HH
                    kp, mh = hyperheuristicSolverHH(kp, items, HH[i])
                    result = kp.getValue()
                else:
                    # Run the respective solver method
                    result = solver(method, kp, items)
                end = perf_counter()

                sumResults += result 
                sumTime += end-start
            # Store the average results and average time per method
            resultsTestDict[method].append(sumResults/iterations)
            resultsTestDict[f'{method}_time'].append(sumTime/iterations)
    # Save the results
    saveDictCSV(resultPath, resultsTestDict)
