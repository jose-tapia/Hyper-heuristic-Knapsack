import pandas as pd
from LSTMModel import generateTrainDataset
from knapsack import  Knapsack, generateItemsList
from IO import load_data, saveDictCSV
from solvers import solver
from metaheuristic import solveMetaheuristic
from hyperheuristic import hyperheuristicSolver
import numpy as np

if __name__ == '__main__':
    tapia_path = "C:/Users/Angel/Documents/Tec/1Semester/Fundamentos/Knapsack_project/Hyper-heuristic-Knapsack/Instances/"
    dany_path =  "/Volumes/GoogleDrive/My Drive/MCCNotes/Jlab projects/GITHUB_repositories/DANY_repositories/Hyper-heuristic-Knapsack/Instances/"

    heuristics = ['default',  'min_weight','max_value',  'max_ratio']
    capacity, lenItems, values_set, weight_set = load_data(tapia_path+"test.txt")
    
    solverMethods = ['SimulatedAnnealing', 'RandomSearch', 'hyperheuristic']
    maxObtained = dict()
    for method in solverMethods:
        maxObtained[method] = 0

    #generateTrainDataset()
        
    capacity, lenItems, values_set, weight_set = load_data(tapia_path+"test.txt")
    kp = Knapsack(capacity)
    items = generateItemsList(values_set, weight_set)
    #print(hyperheuristicSolver(kp, items, trainModel = True))

    resultsTestDict = dict()
    for i in range(1, 31):
        capacity, lenItems, values_set, weight_set = load_data(tapia_path+"Pisinger/pisinger_"+str(i)+".kp")

        ans = []
        for method in solverMethods:
            kp = Knapsack(capacity)
            items = generateItemsList(values_set, weight_set)
            result = solver(method, kp, items)
            ans.append(result)
            if method not in resultsTestDict:
                resultsTestDict[method] = []
            resultsTestDict[method].append(result)
        print(ans)

        maxObtained[solverMethods[np.argmax(ans)]] += 1
    print(maxObtained)

    saveDictCSV("testPisinger-MoreHeuristicsProbabilityNoLimited.csv", resultsTestDict)
#   