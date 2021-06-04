from typing import List
from Utils.knapsack import Item, Knapsack


# Comparison methods for each simple heuristic
heuristicComparison = {
    'default'   : lambda d, item: False, 
    'min_weight': lambda w, item: w.getWeight() > item.getWeight(), 
    'max_value' : lambda v, item: v.getProfit() < item.getProfit(),
    'max_ratio' : lambda r, item: r.getRatio()  < item.getRatio(),
    'max_weight': lambda w, item: w.getWeight() < item.getWeight(), 
    'min_value' : lambda v, item: v.getProfit() > item.getProfit(),
    'min_ratio' : lambda r, item: r.getRatio()  > item.getRatio()
}

class SimpleHeuristic(object):
    def __init__(self, name):
        self.name = name
        # Boolean variable if the heuristic applies for the packed items
        self.onKP = name in ['max_weight', 'min_value', 'min_ratio']

    def nextItem(self, kp: Knapsack, items: List[Item]):
        # Choice the next packable item
        if self.onKP:
            return None
        idx = None
        for i, item in enumerate(items):
            if kp.canPack(item):
                if idx == None or heuristicComparison[self.name](items[idx], item): 
                    idx = i
        return idx
    
    def apply(self, kp: Knapsack, items: List[Item]):
        if self.name == None:
            return None
        if self.onKP:
            # Choice the item that will be unpacked from the knapsack
            idx = None
            kp_packed = kp.getPackedItems()
            for i, item in enumerate(kp_packed):
                if idx == None or heuristicComparison[self.name](kp_packed[idx], item):
                    idx = i
            if idx != None:
                items.append(kp.unpack(idx))
            return idx
        else:
            # Choice the item that will be packed
            idx = None
            for i, item in enumerate(items):
                if kp.canPack(item):
                    if idx == None or heuristicComparison[self.name](items[idx], item):
                        idx = i
            if idx != None:
                kp.pack(items.pop(idx))
            return idx