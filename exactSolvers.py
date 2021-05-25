from typing import List
from knapsack import Item, Knapsack
import numpy as np

def kpBacktracking(capacity: int, items: List[Item]):
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

def kpDP(capacity: int, items: List[Item]):
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