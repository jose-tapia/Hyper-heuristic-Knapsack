from heuristicsClass import HeuristicModel
from knapsackClass import Knapsack, Item
from IO import saveDataCSV
import features

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
            for featureName in features.listFeatures:
                featureDict[featureName] = features.getFeature(featureName, kp, items)
            featureDict['NextHeuristic'] = heuristicName
            featureDataFrame.append(featureDict)

            heuristic = HeuristicModel(heuristicName)
            nextItem = heuristic.nextItem(kp, items)
            if nextItem is not None:
                kp.pack(items[nextItem])
                items.pop(nextItem)
        saveDataCSV("traindata.csv", featureDataFrame, features.listFeatures+["NextHeuristic"])