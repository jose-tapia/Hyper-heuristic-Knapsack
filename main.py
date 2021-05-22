from knapsackClass import Item, Knapsack, generateItemsList
from IO import load_data, saveDataCSV
from solvers import solver

if __name__ == '__main__':
    tapia_path = "C:/Users/Angel/Documents/Tec/1Semester/Fundamentos/Knapsack_project/Hyper-heuristic-Knapsack/Instances/test.txt"
    dany_path =  "/Volumes/GoogleDrive/My Drive/MCCNotes/Jlab projects/GITHUB_repositories/DANY_repositories/Hyper-heuristic-Knapsack/Instances/test.txt"
    capacity, lenItems, values_set, weight_set = load_data(tapia_path)
    
    heuristics = ['default',  'min_weight','max_value',  'max_ratio']

    for heuristic in heuristics:
        kp = Knapsack(capacity)
        items = generateItemsList(values_set, weight_set)
        print(heuristic+": ", solver('heuristic', kp, items, heuristic))

    kp = Knapsack(capacity)
    items = generateItemsList(values_set, weight_set)
    print("HyperHeuristics: ", solver('hyperheuristic', kp, items, heuristics))

    kp = Knapsack(capacity)
    items = generateItemsList(values_set, weight_set)
    print("DP: ", solver('DP', kp, items))

    kp = Knapsack(capacity)
    items = generateItemsList(values_set, weight_set)
    print("Recursive: ", solver('recursive', kp, items))

    #df = [{"NORM_Correlation":0.5, "NextHeuristic": "min_weight"}, {"NormCorrelation":0.1, "NextHeuristic": "max_ratio"}, {"NormCorrelation":0.8, "NextHeuristic": "max_value"}]
    #saveDataCSV("traindata.csv", df, ["NormCorrelation", "NextHeuristic"])
