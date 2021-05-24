from knapsackClass import Knapsack, Item
from heuristicsClass import HeuristicModel
from features import NormCorrelation

class HyperHeuristicModel(object):
    def __init__(self, heuristics: [str]):
        self.currentHeuristic = 0
        self.simple_heuristics = [HeuristicModel(heuristic) for heuristic in heuristics]
    
    def getHeuristic(self, items: [Item]):
        pastHeuristic = self.currentHeuristic
        if NormCorrelation(items) > 0.5:
            self.currentHeuristic = (self.currentHeuristic+1)%len(self.simple_heuristics)
        return pastHeuristic
    
    def nextItem(self, kp: Knapsack, items: [Item]):
        return self.simple_heuristics[self.getHeuristic(items)].nextItem(kp, items)