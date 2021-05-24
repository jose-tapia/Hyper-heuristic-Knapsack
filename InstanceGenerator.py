import numpy as np
from knapsackClass import generateItemsList 

def buildInstance(num_items, max_V, max_W):
    '''
    Returns: examples of random items with weights and values
    '''
    values = np.random.randint(1, max_V, size = num_items)
    weights = np.random.randint(1, max_W, size = num_items)
    return generateItemsList(values, weights), values, weights
