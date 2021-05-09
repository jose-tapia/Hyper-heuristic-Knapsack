from knapsackClass import Item, Knapsack, generateItemsList
from IO import load_data
from heuristicsClass import Heuristic
from hyperheuristic import hyperheuristic

def ConstructiveHeuristic(heuristic: str, kp: Knapsack, items: [Item]):
    simple_heuristic = Heuristic(heuristic)

    nextItem = simple_heuristic.nextItem(kp, items)
    while nextItem is not None:
        kp.pack(items[nextItem])
        items.pop(nextItem)
        nextItem = simple_heuristic.nextItem(kp, items)

    return kp.getValue()

if __name__ == '__main__':
    tapia_path = "C:/Users/Angel/Documents/Tec/1Semester/Fundamentos/Knapsack_project/Hyper-heuristic-Knapsack/Instances/test.txt"
    dany_path =  "/Volumes/GoogleDrive/My Drive/MCCNotes/Jlab projects/GITHUB_repositories/DANY_repositories/Hyper-heuristic-Knapsack/Instances/test.txt"
    capacity, lenItems, values_set, weight_set = load_data(tapia_path)
    
    heuristics = ['default',  'min_weight','max_value',  'max_ratio']

    for heuristic in heuristics:
        kp = Knapsack(capacity)
        items = generateItemsList(values_set, weight_set)
        print(heuristic+": ", ConstructiveHeuristic(heuristic, kp, items))

    kp = Knapsack(capacity)
    items = generateItemsList(values_set, weight_set)
    print("HyperHeuristics: ", hyperheuristic(heuristics, kp, items))

    
