from knapsackClass import Item, Knapsack
import numpy as np

def NormCorrelation(items: [Item]):
    x = [item.getValue() for item in items]
    y = [item.getWeight() for item in items]
    return (np.corrcoef(x/np.max(x), y/np.max(y))[0, 1])/2+0.5