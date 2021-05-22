from knapsack import Item, Knapsack, generateItemsList
from IO import load_data, saveDataCSV
from solvers import solver
from metaheuristic import solveMetaheuristic

if __name__ == '__main__':
    tapia_path = "C:/Users/Angel/Documents/Tec/1Semester/Fundamentos/Knapsack_project/Hyper-heuristic-Knapsack/Instances/"
    dany_path =  "/Volumes/GoogleDrive/My Drive/MCCNotes/Jlab projects/GITHUB_repositories/DANY_repositories/Hyper-heuristic-Knapsack/Instances/"

    heuristics = ['default',  'min_weight','max_value',  'max_ratio']
    """
    for i in range(1, 21):
        capacity, lenItems, values_set, weight_set = load_data(tapia_path+"Pisinger/pisinger_"+str(i)+".kp")

        kp = Knapsack(capacity)
        items = generateItemsList(values_set, weight_set)
        A = solveMetaheuristic("SimulatedAnnealing", kp, items)

        kp = Knapsack(capacity)
        items = generateItemsList(values_set, weight_set)
        B = solveMetaheuristic("RandomSearch", kp, items)
        if A != B:
            print(i, "wowow\n", A, B)
    """
    capacity, lenItems, values_set, weight_set = load_data(tapia_path+"test.txt")
    




    for heuristic in heuristics:
        kp = Knapsack(capacity)
        items = generateItemsList(values_set, weight_set)
        print(heuristic+": ", solver('heuristic', kp, items, heuristic))

    kp = Knapsack(capacity)
    items = generateItemsList(values_set, weight_set)
    print("HyperHeuristics: ", solver('hyperheuristic', kp, items, heuristics))

    #kp = Knapsack(capacity)
    #items = generateItemsList(values_set, weight_set)
    #print("DP: ", solver('DP', kp, items))

    #kp = Knapsack(capacity)
    #items = generateItemsList(values_set, weight_set)
    #print("Recursive: ", solver('recursive', kp, items))

    print("\n\n")

    kp = Knapsack(capacity)
    items = generateItemsList(values_set, weight_set)
    print("Simulated Annealing: ", solveMetaheuristic("SimulatedAnnealing", kp, items, saveMetaheuristic = True, backTime = 2, overwrite = True))
    
    kp = Knapsack(capacity)
    items = generateItemsList(values_set, weight_set)
    print("Random Search: ", solveMetaheuristic("RandomSearch", kp, items))
    
    kp = Knapsack(capacity)
    items = generateItemsList(values_set, weight_set)
    solveMetaheuristic("RandomSearch", kp, items, saveMetaheuristic = True, backTime = 2, overwrite = False)
    
    #df = [{"NORM_CORRELATION":0.5, "NextHeuristic": "min_weight"}, 
    #    {"NORM_CORRELATION":0.1, "NextHeuristic": "max_ratio"}, 
    #    {"NORM_CORRELATION":0.8, "NextHeuristic": "max_value"}]
    #saveDataCSV("traindata.csv", df, ["NORM_CORRELATION", "NextHeuristic"])
