from knapsack import Item, Knapsack

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
        self.onKP = name in ['max_weight', 'min_value', 'min_ratio']

    def nextItem(self, kp: Knapsack, items: [Item]):
        if self.onKP:
            return None
        idx = None
        for i, item in enumerate(items):
            if kp.canPack(item):
                if idx == None or heuristicComparison[self.name](items[idx], item): 
                    idx = i
        return idx
    
    def apply(self, kp: Knapsack, items: [Item]):
        if self.onKP:
            idx = None
            kp_packed = kp.getPackedItems()
            for i, item in enumerate(kp_packed):
                if idx == None or heuristicComparison[self.name](kp_packed[idx], item):
                    idx = i
            if idx != None:
                items.append(kp.unpack(idx))
            return idx
        else:
            idx = None
            for i, item in enumerate(items):
                if kp.canPack(item):
                    if idx == None or heuristicComparison[self.name](items[idx], item):
                        idx = i
            if idx != None:
                kp.pack(items.pop(idx))
            return idx