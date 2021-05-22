from knapsack import Knapsack, Item
from simpleHeuristic import SimpleHeuristic
from features import getFeature

class HyperHeuristic(object):
    def __init__(self, heuristicNames: [str]):
        self.currentHeuristic = 0
        self.heuristics = [SimpleHeuristic(name) for name in heuristicNames]
    
    def getHeuristic(self, items: [Item]):
        pastHeuristic = self.currentHeuristic
        if getFeature("NORM_CORRELATION", items) > 0.5:
            self.currentHeuristic += 1
            self.currentHeuristic %= len(self.heuristics)
        return self.heuristics[pastHeuristic]
    
    def nextItem(self, kp: Knapsack, items: [Item]):
        return self.getHeuristic(items).nextItem(kp, items)