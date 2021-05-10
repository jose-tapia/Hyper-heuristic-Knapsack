from heuristicsClass import HeuristicModel
from hyperheuristicClass import HyperHeuristicModel
from knapsackClass import Item, Knapsack
import numpy as np

def ConstructiveSolution(items: [Item], kp: Knapsack, itemSelector):
    nextItem = itemSelector.nextItem(kp, items)
    while nextItem is not None:
        kp.pack(items[nextItem])
        items.pop(nextItem)
        nextItem = itemSelector.nextItem(kp, items)
    return kp.getValue()

def kpHeuristic(items: [Item], kp: Knapsack, heuristic: str):
    simple_heuristic = HeuristicModel(heuristic)
    return ConstructiveSolution(items, kp, simple_heuristic)


def kpHyperheuristic(items: [Item], kp: Knapsack, heuristics: [str]):
    hh = HyperHeuristicModel(heuristics)
    return ConstructiveSolution(items, kp, hh)

def kpBacktracking(items: [Item], capacity: int):
    '''
    Input: the list of items(objects with weight and value)  and the capacity of the knapsack
    Returns: a tuple with total value and solution to the problem
    '''
    if items == [] or capacity == 0:
        return Knapsack(capacity)
    
    if items[0].getWeight() > capacity: 
        return kpBacktracking(items[1:], capacity)
    else: 
        kpWithItem = kpBacktracking(items[1:], capacity - items[0].getWeight())
        kpWithItem.capacity += items[0].getWeight()
        kpWithItem.pack(items[0])

        kpWithoutItem = kpBacktracking(items[1:], capacity)
        
        if kpWithItem.getValue() < kpWithoutItem.getValue():
            return kpWithoutItem
        else:
            return kpWithItem

def kpDP(items: [Item], capacity: int):
    '''
    Input: the list of items(objects with weight and value)  and the capacity of the knapsack
    Returns: a tuple with total value and a solution to the problem
    '''
    # Build matrix in a bottom up-manner 
    A = np.zeros((len(items)+1, capacity+1))
    for idx, item in zip(range(1, 1+len(items)), items):
        for w in range(capacity+1):
            if w == 0:
                continue
            elif item.getWeight() <= w: 
                if idx == 0:
                    A[idx, w] = item.getValue()
                else:
                    A[idx, w] = max(A[idx-1, w], 
                                A[idx-1, w-item.getWeight()] +
                                           item.getValue())
            else:
                A[idx, w] = A[idx-1, w]
    #store results of knapsack
    val, cap = A[len(items), capacity], capacity
    kp = Knapsack(capacity)
    for idx in range(len(items), 0, -1):
        if val <= 0: break
        elif cap >= items[idx-1].getWeight() and val == A[idx-1, cap-items[idx-1].getWeight()]+items[idx-1].getValue():
            val -= items[idx-1].getValue()
            cap -= items[idx-1].getWeight()
            kp.pack(items[idx-1])
    return kp


def solver(method: str, kp: Knapsack, items: [Item], additionalArgs = None):
    if method == 'heuristic':
        return kpHeuristic(items, kp, additionalArgs)
    elif method == 'hyperheuristic':
        return kpHyperheuristic(items, kp, additionalArgs)
    elif method == 'recursive':
        return kpBacktracking(items, kp.getCapacity()).getValue()
    elif method == 'DP':
        return kpDP(items, kp.getCapacity()).getValue()
    else:
        return 0
