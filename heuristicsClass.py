from knapsackClass import Item, Knapsack

class Heuristic(object):
    comparisons = {
        'default': lambda d, item: False, 
        'min_weight': lambda w, item: w.getWeight() > item.getWeight(), 
        'max_value': lambda v, item: v.getValue() < item.getValue(),
        'max_ratio': lambda r, item: r.getRatio() < item.getRatio()
    }
    
    def __init__(self, heuristicName):
        self.name = heuristicName

    def nextItem(self, knapsack: Knapsack, items: [Item]):
        idx = None 
        for i in range(len(items)):
            if knapsack.canPack(items[i]):
                if idx == None or self.comparisons[self.name](items[idx], items[i]): 
                    idx = i
        return idx
