from knapsackClass import Item, Knapsack
import numpy as np

listFeatures = ["NormCorrelation"]

def getFeature(featureName: str, kp: Knapsack, items: [Item]):
    if featureName == "NormCorrelation":
        return NormCorrelation(items)
    else:
        return None

def getAllFeatures(kp: Knapsack, items: [Item]):
    featuresValues = []
    for featureName in listFeatures:
        featuresValues.append(getFeature(featureName, kp, items))
    return featuresValues

def NormCorrelation(items: [Item]):
    x = [item.getValue() for item in items]
    y = [item.getWeight() for item in items]
    return (np.corrcoef(x/np.max(x), y/np.max(y))[0, 1])/2+0.5