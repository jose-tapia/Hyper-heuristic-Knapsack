from LSTM import generateTrainDataset, buildModel
from knapsack import  Knapsack, generateItemsList
from IO import load_data, obtainDirectory, obtainFilenames, saveDictCSV
from solvers import solver
from simpleHeuristic import heuristicComparison
from hyperheuristic import Hyperheuristic, hyperheuristicSolverMH, hyperheuristicSolverHH
from time import perf_counter
import numpy as np

if __name__ == '__main__':
    tapia_path = "C:/Users/Angel/Documents/Tec/1Semester/Fundamentos/Knapsack_project/Hyper-heuristic-Knapsack/"
    dany_path =  "/Volumes/GoogleDrive/My Drive/MCCNotes/Jlab projects/GITHUB_repositories/DANY_repositories/Hyper-heuristic-Knapsack/"    
    

    np.random.seed(0)
    #generateTrainDataset("traindata.csv", True, "OrtizBayliss")

    #buildModel(tapia_path+"lstm_model.h5", tapia_path+"traindata.csv")
    instances = obtainDirectory(tapia_path+"Instances/kplib/")
    heuristics = list(heuristicComparison.keys())
    resultsTestDict = dict()    
#    iteratMethods = [1, 1, 1, 1, 10, 10, 1, 10]
    iteratMethods = [1, 1, 1, 1, 10]
#    solverMethods = heuristics[:4]+['SimulatedAnnealing', 'RandomSearch', 'IP', 'hyperheuristic']
    solverMethods = heuristics[:4]+["hyperheuristic"]
    for method, n_iter in zip(solverMethods, iteratMethods):
        for i in range(n_iter):
            resultsTestDict[method+"_"+str(i)] = []
            resultsTestDict[method+"_time_"+str(i)] = []
    #for heuristic in heuristics:
    #    resultsTestDict[heuristic] = []
    HH = []
    for i in range(10):
        HH.append(Hyperheuristic('probability', trainModel = True))
    instances = obtainDirectory(tapia_path+"Instances/kplib/")
    for instance in instances:
        capacity, lenItems, values_set, weight_set = load_data(instance)

        for method, n_iter in zip(solverMethods, iteratMethods):
            for i in range(n_iter):
                kp = Knapsack(capacity)
                items = generateItemsList(values_set, weight_set)

                start = perf_counter()
                if method == 'hyperheuristic':
                    kp, mh = hyperheuristicSolverHH(kp, items, HH[i])
                    result = kp.getValue()
                else:
                    result = solver(method, kp, items)
                end = perf_counter()
                resultsTestDict[method+"_"+str(i)].append(result)
                resultsTestDict[method+"_time_"+str(i)].append(end-start)
        
        #kp = Knapsack(capacity)
        #items = generateItemsList(values_set, weight_set)
        #start = perf_counter()
        #kp, mh = hyperheuristicSolverMH(kp, items, modelTrainedFilename = 'lstm_model_Martello.h5')
        #end = perf_counter()
        #mhstats = mh.stats()
        #resultsTestDict['hyperheuristic'].append(kp.getValue())
        #resultsTestDict['hyperheuristic_time'].append(end-start)
        #for heuristic in heuristics:
        #    resultsTestDict[heuristic].append(mhstats[heuristic])

    saveDictCSV("testOrtizBayliss-Performance.csv", resultsTestDict)
