from knapsack import Item, Knapsack
import numpy as np

features = {
    "NORM_MEAN_WEIGHT"  : lambda w, p: np.mean(w)/np.max(w),
    "NORM_MEDIAN_WEIGHT": lambda w, p: np.median(w)/np.max(w), 
    "NORM_STD_WEIGHT"   : lambda w, p: np.std(w)/np.max(w),
    "NORM_MEAN_PROFIT"  : lambda w, p: np.mean(p)/np.max(p), 
    "NORM_MEDIAN_PROFIT": lambda w, p: np.median(p)/np.max(p), 
    "NORM_STD_PROFIT"   : lambda w, p: np.std(p)/np.max(p),
    "NORM_CORRELATION"  : lambda w, p: np.corrcoef(w/np.max(w), p/np.max(p))[0, 1]/2+0.5
}

def getFeature(featureName: str, items: [Item]):
    w = [item.getWeight() for item in items]
    p = [item.getProfit() for item in items]
    if featureName in features:
        return features[featureName](w, p)
    else:
        print("Invalid feature: ", featureName)
        return None

def getAllFeatures(items: [Item]):
    w = [item.getWeight() for item in items]
    p = [item.getProfit() for item in items]
    return [featureFunction(w, p) for featureFunction in features.values()]
