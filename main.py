from LSTM import generateTrainDataset, buildModel
from knapsack import  Knapsack, generateItemsList
from IO import load_data, obtainFilenames, saveDictCSV
from solvers import solver
from simpleHeuristic import heuristicComparison
from hyperheuristic import hyperheuristicSolverMH
from time import perf_counter

if __name__ == '__main__':
    tapia_path = "C:/Users/Angel/Documents/Tec/1Semester/Fundamentos/Knapsack_project/Hyper-heuristic-Knapsack/"
    dany_path =  "/Volumes/GoogleDrive/My Drive/MCCNotes/Jlab projects/GITHUB_repositories/DANY_repositories/Hyper-heuristic-Knapsack/"    
    
    #generateTrainDataset("traindata.csv", True, "OrtizBayliss")
    #buildModel(tapia_path+"lstm_model.h5", tapia_path+"traindata.csv")

    heuristics = list(heuristicComparison.keys())
    resultsTestDict = dict()    
    solverMethods = ['SimulatedAnnealing', 'RandomSearch', 'IP', 'hyperheuristic']
    for method in solverMethods:
        resultsTestDict[method] = []
        resultsTestDict[method+"_time"] = []
    for heuristic in heuristics:
        resultsTestDict[heuristic] = []

    instances = obtainFilenames(tapia_path, 'Pisinger')
    for instance in instances:
        capacity, lenItems, values_set, weight_set = load_data(instance)

        for method in solverMethods[:3]:
            kp = Knapsack(capacity)
            items = generateItemsList(values_set, weight_set)

            start = perf_counter()
            result = solver(method, kp, items)
            end = perf_counter()
            resultsTestDict[method].append(result)
            resultsTestDict[method+"_time"].append(end-start)
        
        kp = Knapsack(capacity)
        items = generateItemsList(values_set, weight_set)
        start = perf_counter()
        kp, mh = hyperheuristicSolverMH(kp, items)
        end = perf_counter()
        mhstats = mh.stats()
        resultsTestDict['hyperheuristic'].append(kp.getValue())
        resultsTestDict['hyperheuristic_time'].append(end-start)
        for heuristic in heuristics:
            resultsTestDict[heuristic].append(mhstats[heuristic])

    saveDictCSV("testPisinger-Test.csv", resultsTestDict)
