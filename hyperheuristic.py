from knapsackClass import Knapsack, Item
from heuristicsClass import Heuristic
import numpy as np
import pandas as pd

def NormCorrelation(items: [Item]):
    x = [item.getValue() for item in items]
    y = [item.getWeight() for item in items]
    return pd.Series(x).corr(pd.Series(y), method = 'pearson')/2+0.5
    #return (np.corrcoef(x, y)[0, 1])/2+0.5

class HyperHeuristicModel(object):
    def __init__(self, heuristics: [str]):
        self.currentHeuristic = 0
        self.simple_heuristics = [Heuristic(heuristic) for heuristic in heuristics]
    
    def getHeuristic(self, items: [Item]):
        print(NormCorrelation(items))
        if NormCorrelation(items) > 0.5:
            self.currentHeuristic = (self.currentHeuristic+1)%len(self.simple_heuristics)
        return self.currentHeuristic
    
    def nextItem(self, kp: Knapsack, items: [Item]):
        return self.simple_heuristics[self.getHeuristic(items)].nextItem(kp, items)

def hyperheuristic(heuristics: [str], kp: Knapsack, items: [Item]):
    hh = HyperHeuristicModel(heuristics)

    nextItem = hh.nextItem(kp, items)
    while nextItem is not None:
        kp.pack(items[nextItem])
        items.pop(nextItem)
        nextItem = hh.nextItem(kp, items)
    
    return kp.getValue()


