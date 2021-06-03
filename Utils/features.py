from typing import List
import numpy as np
from Utils.knapsack import Item

featuresCalculation = {
    'NORM_MEAN_WEIGHT'  : lambda w, p: np.mean(w)/np.max(w),
    'NORM_MEDIAN_WEIGHT': lambda w, p: np.median(w)/np.max(w),
    'NORM_STD_WEIGHT'   : lambda w, p: np.std(w)/np.max(w),
    'NORM_MEAN_PROFIT'  : lambda w, p: np.mean(p)/np.max(p), 
    'NORM_MEDIAN_PROFIT': lambda w, p: np.median(p)/np.max(p), 
    'NORM_STD_PROFIT'   : lambda w, p: np.std(p)/np.max(p),
    'NORM_CORRELATION'  : lambda w, p: np.corrcoef(w/np.max(w), p/np.max(p))[0, 1]/2+0.5 if len(w) > 1 else 0
}

def getFeature(featureName: str, items: List[Item]):
    w = [item.getWeight() for item in items]
    p = [item.getProfit() for item in items]
    if featureName in featuresCalculation:
        return featuresCalculation[featureName](w, p)
    else:
        print('Invalid feature: ', featureName)
        return None

def getAllFeatures(items: List[Item]):
    w = [item.getWeight() for item in items]
    p = [item.getProfit() for item in items]
    return [featureFunction(w, p) for featureFunction in featuresCalculation.values()]
