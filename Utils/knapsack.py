from typing import List

class Item(object):
    def __init__(self, id, w: int, p: int):
        self.name = id
        self.weight = w
        self.profit = p
    
    def getName(self):
        return self.name

    def getProfit(self):
        return self.profit

    def getWeight(self):
        return self.weight

    def getRatio(self):
        return self.profit/self.weight

    def __str__(self):
        return f' Item: {self.name}, <Weight: {str(self.weight)}, Profit: {str(self.profit)}>'

class Knapsack(object):
    def __init__(self, W: int):
        self.capacity = W
        self.value = 0
        self.items = []

    def getCapacity(self):
        return self.capacity
    
    def getValue(self):
        return self.value

    def getPackedItems(self):
        return self.items

    def canPack(self, item: Item):
        return item.getWeight() <= self.capacity

    def pack(self, item: Item):
        # Insert the item only if it has the capacity
        if item.getWeight() <= self.capacity:
            self.capacity -= item.getWeight()
            self.value += item.getProfit()
            self.items.append(item)

    def unpack(self, idx: int):
        # Unpack the item 
        if 0 <= idx and idx < len(self.items):
            self.capacity += self.items[idx].getWeight()
            self.value -= self.items[idx].getProfit()
            return self.items.pop(idx)
        else:
            return None
            
    def printKnapsack(self):
        print(self)
        for item in self.items:
            print('\t', item)
    
    def copy(self):
        # Deep copy of the class
        kp_copy = Knapsack(self.capacity)
        kp_copy.value = self.value
        kp_copy.items = self.items.copy()
        return kp_copy

    def __str__(self):
        return f' Knapsack: <Capacity: {str(self.capacity)}, Value: {str(self.value)}, items: {str(len(self.items))}>'

def generateItemList(weights: List[int], profits: List[int]):
    # Convert the list of weights and profits to a list of items
    return [Item(id, w, p) for id, (w, p) in enumerate(zip(weights, profits))]