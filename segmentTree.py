from typing import List
from knapsack import Item 

class SegmentTree(object):
    def __init__(self, items: List[int], comparison):
        self.items = items 
        self.comparison = comparison
        self.st = [0]*4*len(items)
        self._initialize(1, 0, len(items))

    def erase(self, idx):
        self._update(1, 0, len(self.items), idx, None)

    def add(self, idx):
        self._update(1, 0, len(self.items), idx, idx)

    def update(self, idx, value):
        self._update(1, 0, len(self.items), idx, value)
    
    def query(self):
        return self.st[1]
    
#    def query(self, l, r):
#        return self._query(self, 1, 0, len(self.items), l, r+1)

    def _initialize(self, n, l, r):
        if l+1 == r:
            self.st[n] = l 
            return 
        self._initialize(2*n,   l, (l+r)//2)
        self._initialize(2*n+1, (l+r)//2, r)
        self._updateNode(n)
    
    def _comparison(self, a, b):
        if a == None:
            return b 
        elif b == None:
            return a 
        elif self.comparison(self.items[a], self.items[b]):
            return a
        else:
            return b

    def _updateNode(self, n):
        self.st[n] = self._comparison(self.st[2*n], self.st[2*n+1])
    
    def _update(self, n, l, r, idx, value):
        if l+1 == r:
            self.st[n] = value
            return
        if idx < (l+r)//2:
            self._update(2*n, l, (l+r)//2, idx, value)
        else:
            self._update(2*n+1, (l+r)//2, r, idx, value)
        self._updateNode(n)    
    
    def _query(self, n, l, r, L, R):
        if r <= L or R <= l:
            return None
        if L <= l and r <= R:
            return self.st[n]
        a = self._query(2*n,   l, (l+r)//2, L, R)
        b = self._query(2*n+1, (l+r)//2, r, L, R)
        return self._comparison(a, b)

    def __str__(self):
        return str(self.st)

class STItems(object):
    def __init__(self, items: List[Item]):
        self.st = dict()
        self.items = items.copy()
        self.st['default']    = SegmentTree([0]*len(items), lambda a, b: True)
        self.st['max_value']  = SegmentTree([item.getProfit() for item in items], max)
        self.st['min_weight'] = SegmentTree([item.getWeight() for item in items], min)
        self.st['max_ratio']  = SegmentTree([item.getRatio()  for item in items], max)
    
    def nextItem(self, heuristic: str, C: int):
        idx = self.st[heuristic].query()
        while idx != None and self.items[idx].getWeight() > C:
            for st in self.st.values():
                st.erase(idx)
            idx = self.st[heuristic].query()
        if idx != None:
            return self.items[idx], idx
        return None, None
    
    def addItem(self, idx: int):
        if 0 <= idx and idx < len(self.items):
            for st in self.st.values():
                st.add(idx)

    def eraseItem(self, idx: int):
        if 0 <= idx and idx < len(self.items):
            for st in self.st.values():
                st.erase(idx)