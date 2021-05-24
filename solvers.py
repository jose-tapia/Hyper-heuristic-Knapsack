from simpleHeuristic import SimpleHeuristic
from hyperheuristic import HyperHeuristic
from knapsack import Item, Knapsack
import numpy as np

def ConstructiveSolution(items: [Item], kp: Knapsack, itemSelector):
    nextItem = itemSelector.nextItem(kp, items)
    while nextItem is not None:
        kp.pack(items[nextItem])
        items.pop(nextItem)
        nextItem = itemSelector.nextItem(kp, items)
    return kp

def kpBacktracking(items: [Item], capacity: int):
    if items == [] or capacity == 0:
        return Knapsack(capacity)
    item = items[0]
    if item.getWeight() > capacity: 
        return kpBacktracking(items[1:], capacity)
    else: 
        kpWithItem = kpBacktracking(items[1:], capacity - item.getWeight())
        kpWithItem.capacity += item.getWeight()
        kpWithItem.pack(item)

        kpWithoutItem = kpBacktracking(items[1:], capacity)
        
        if kpWithItem.getValue() < kpWithoutItem.getValue():
            return kpWithoutItem
        else:
            return kpWithItem

def kpDP(items: [Item], capacity: int):
    A = np.zeros((len(items)+1, capacity+1))
    for idx, item in enumerate(items, start = 1):
        w, p = item.getWeight(), item.getProfit()
        for W in range(capacity+1):
            if W == 0:
                continue
            elif idx == 0:
                A[idx, W] = p if w <= W else 0
            elif w <= W:
                A[idx, W] = max(A[idx-1, W], A[idx-1, W-w]+p)
            else:
                A[idx, W] = A[idx-1, W]
                
    kp, idx = Knapsack(capacity), len(items)
    while idx >= 1 and kp.getCapacity() > 0:
        if A[idx-1, kp.getCapacity()] != A[idx, kp.getCapacity()]:
            kp.pack(items[idx-1])
        idx -= 1            
    return kp

def solver(method: str, kp: Knapsack, items: [Item], additionalArgs = None):
    if method == 'heuristic':
        simple_heuristic = SimpleHeuristic(additionalArgs)
        return ConstructiveSolution(items, kp, simple_heuristic).getValue()
    elif method == 'hyperheuristic':
        hh = HyperHeuristic(additionalArgs)
        return ConstructiveSolution(items, kp, hh).getValue()
    elif method == 'recursive':
        return kpBacktracking(items, kp.getCapacity()).getValue()
    elif method == 'DP':
        return kpDP(items, kp.getCapacity()).getValue()
    else:
        return 0
