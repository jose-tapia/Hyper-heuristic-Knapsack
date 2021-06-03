from typing import List
import numpy as np
from Utils.knapsack import Item, Knapsack


def kpBacktracking(W: int, items: List[Item]):
    if items == [] or W == 0:
        return Knapsack(W)
    item = items[0]
    if item.getWeight() > W: 
        return kpBacktracking(items[1:], W)
    else: 
        kpWithItem = kpBacktracking(items[1:], W - item.getWeight())
        kpWithItem.capacity += item.getWeight()
        kpWithItem.pack(item)

        kpWithoutItem = kpBacktracking(items[1:], W)
        
        if kpWithItem.getValue() < kpWithoutItem.getValue():
            return kpWithoutItem
        else:
            return kpWithItem

def kpDP(W: int, items: List[Item]):
    n = len(items)
    A = np.zeros((n+1, W+1))
    for idx, item in enumerate(items, start = 1):
        w, p = item.getWeight(), item.getProfit()
        for Wi in range(W+1):
            if Wi == 0:
                continue
            elif idx == 0:
                A[idx, Wi] = p if w <= Wi else 0
            elif w <= Wi:
                A[idx, Wi] = max(A[idx-1, Wi], A[idx-1, Wi-w]+p)
            else:
                A[idx, Wi] = A[idx-1, Wi]
                
    kp, idx = Knapsack(W), n
    while idx >= 1 and kp.getCapacity() > 0:
        if A[idx-1, kp.getCapacity()] != A[idx, kp.getCapacity()]:
            kp.pack(items[idx-1])
        idx -= 1            
    return kp
