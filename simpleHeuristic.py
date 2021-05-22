from knapsack import Item, Knapsack

heuristicComparison = {
    'default'   : lambda d, item: False, 
    'min_weight': lambda w, item: w.getWeight() > item.getWeight(), 
    'max_value' : lambda v, item: v.getProfit() < item.getProfit(),
    'max_ratio' : lambda r, item: r.getRatio()  < item.getRatio()
}

class SimpleHeuristic(object):
    def __init__(self, name):
        self.name = name

    def nextItem(self, kp: Knapsack, items: [Item]):
        idx = None
        for i, item in enumerate(items):
            if kp.canPack(item):
                if idx == None or heuristicComparison[self.name](items[idx], item): 
                    idx = i
        return idx