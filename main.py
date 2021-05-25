from LSTMModel import generateTrainDataset
from numpy.lib.npyio import save
from knapsack import Item, Knapsack, generateItemsList
from IO import load_data, saveDataCSV
from solvers import solver
from metaheuristic import solveMetaheuristic
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

#    generateTrainDataset()
        
#    capacity, lenItems, values_set, weight_set = load_data(tapia_path+"test.txt")
#    kp = Knapsack(capacity)
#    items = generateItemsList(values_set, weight_set)
#    print(solver('hyperheuristic', kp, items, True))


    
    for i in range(1, 31):
        capacity, lenItems, values_set, weight_set = load_data(tapia_path+"Pisinger/pisinger_"+str(i)+".kp")

        ans = []
        for method in solverMethods:
            kp = Knapsack(capacity)
            items = generateItemsList(values_set, weight_set)
            ans.append(solver(method, kp, items))
        print(ans)
        maxObtained[solverMethods[np.argmax(ans)]] += 1
    print(maxObtained)

#        kp = Knapsack(capacity)
#        items = generateItemsList(values_set, weight_set)
#        B = solveMetaheuristic("RandomSearch", kp, items, saveMetaheuristic = True)
#    print("SA < RS", AB)
#    print("RS < SA", BA)
 
    



    #for heuristic in heuristics:
    #    kp = Knapsack(capacity)
    #    items = generateItemsList(values_set, weight_set)
    #    print(heuristic+": ", solver('heuristic', kp, items, heuristic))

    #kp = Knapsack(capacity)
    #items = generateItemsList(values_set, weight_set)
    #print("HyperHeuristics: ", solver('hyperheuristic', kp, items, heuristics))

    #kp = Knapsack(capacity)
    #items = generateItemsList(values_set, weight_set)
    #print("DP: ", solver('DP', kp, items))

    #kp = Knapsack(capacity)
    #items = generateItemsList(values_set, weight_set)
    #print("Recursive: ", solver('recursive', kp, items))

    #print("\n\n")

    #kp = Knapsack(capacity)
    #items = generateItemsList(values_set, weight_set)
#    print("Simulated Annealing: ", solveMetaheuristic("SimulatedAnnealing", kp, items, saveMetaheuristic = True, fileName = 'traindata.csv', backTime = 0, overwrite = True))
    
    #kp = Knapsack(capacity)
    #items = generateItemsList(values_set, weight_set)
    #print("Random Search: ", solveMetaheuristic("RandomSearch", kp, items))
    
#    kp = Knapsack(capacity)
#    items = generateItemsList(values_set, weight_set)
#    print(solver('hyperheuristic', kp, items))
#    solveMetaheuristic("RandomSearch", kp, items, saveMetaheuristic = True, fileName = 'traindata.csv', backTime = 0, overwrite = False)
    
    #df = [{"NORM_CORRELATION":0.5, "NextHeuristic": "min_weight"}, 
    #    {"NORM_CORRELATION":0.1, "NextHeuristic": "max_ratio"}, 
    #    {"NORM_CORRELATION":0.8, "NextHeuristic": "max_value"}]
    #saveDataCSV("traindata.csv", df, ["NORM_CORRELATION", "NextHeuristic"])
