from knapsack import Item, Knapsack, generateItemsList
from IO import load_data, saveDataCSV
from solvers import solver
from metaheuristic import SimulatedAnnealing, RandomSearch

if __name__ == '__main__':
    tapia_path = "C:/Users/Angel/Documents/Tec/1Semester/Fundamentos/Knapsack_project/Hyper-heuristic-Knapsack/Instances/"
    dany_path =  "/Volumes/GoogleDrive/My Drive/MCCNotes/Jlab projects/GITHUB_repositories/DANY_repositories/Hyper-heuristic-Knapsack/Instances/"

    heuristics = ['default',  'min_weight','max_value',  'max_ratio']
    for i in range(1, 31):
        capacity, lenItems, values_set, weight_set = load_data(tapia_path+"Pisinger/pisinger_"+str(i)+".kp")

        kp = Knapsack(capacity)
        items = generateItemsList(values_set, weight_set)
        A = SimulatedAnnealing(kp, items)

        kp = Knapsack(capacity)
        items = generateItemsList(values_set, weight_set)
        B = RandomSearch(kp, items)
        if A != B:
            print(i, "wowow\n")

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
    print("Simulated Annealing: ", SimulatedAnnealing(kp, items))
    
    kp = Knapsack(capacity)
    items = generateItemsList(values_set, weight_set)
    print("Random Search: ", RandomSearch(kp, items))
    #df = [{"NORM_Correlation":0.5, "NextHeuristic": "min_weight"}, {"NormCorrelation":0.1, "NextHeuristic": "max_ratio"}, {"NormCorrelation":0.8, "NextHeuristic": "max_value"}]
    #saveDataCSV("traindata.csv", df, ["NormCorrelation", "NextHeuristic"])
