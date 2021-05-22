from heuristicsClass import HeuristicModel
from knapsackClass import Knapsack, Item
from IO import saveDataCSV
from features import features, getAllFeatures

class MetaheuristicModel(object):
    def __init__(self):
        self.sequenceHeuristics = []

    def addHeuristic(self, heuristicName: str):
        self.sequenceHeuristics.append(heuristicName)
    
    def solveInstance(self, C, items = [Item]):
        kp = Knapsack(C)
        for heuristicName in self.sequenceHeuristics:
            heuristic = HeuristicModel(heuristicName)
            nextItem = heuristic.nextItem(kp, items)
            if nextItem is not None:
                kp.pack(items[nextItem])
                items.pop(nextItem)
        return kp, items
    
    def convertToDict(self, C, items = [Item]):
        kp = Knapsack(C)
        featureDataFrame = []
        for heuristicName in self.sequenceHeuristics:
            featureDict = dict()
            featureValues = getAllFeatures(items)
            for name, value in zip(features.keys(), featureValues):
                featureDict[name] = value
            featureDict['NextHeuristic'] = heuristicName
            featureDataFrame.append(featureDict)

            heuristic = HeuristicModel(heuristicName)
            nextItem = heuristic.nextItem(kp, items)
            if nextItem is not None:
                kp.pack(items[nextItem])
                items.pop(nextItem)
        saveDataCSV("traindata.csv", featureDataFrame, features.keys()+["NextHeuristic"])