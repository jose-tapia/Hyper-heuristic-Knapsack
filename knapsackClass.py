class Item(object):
    def __init__(self, id, v: int, w: int):
        self.name = id
        self.value = v
        self.weight = w
    
    def getName(self):
        return self.name

    def getValue(self):
        return self.value

    def getWeight(self):
        return self.weight

    def getRatio(self):
        return self.getValue()/self.getWeight()

    def __str__(self):
        return f' Item: {self.name}, <Value: {str(self.value)}, Weight: {str(self.weight)}>'

class Knapsack(object):
    def __init__(self, c: int):
        self.capacity = c
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
        if item.getWeight() <= self.capacity:
            self.capacity -= item.getWeight()
            self.value += item.getValue()
            self.items.append(item)

    def unpack(self, idx: int):
        if 0 <= idx and idx < len(self.items):
            self.capacity += self.items[idx].getWeight()
            self.value -= self.items[idx].getValue()
            return self.items.pop(idx)
        else:
            return None
    
    def __str__(self):
        return f' Knapsack instance: <Capacity: {str(self.capacity)}, Value: {str(self.value)}, items: {str(len(self.items))}>'

def generateItemsList(vList: [int], wList: [int]):
    items = []
    if len(vList) == len(wList):
        for id, v, w in zip(range(1, len(vList)), vList, wList):
            items.append(Item(str(id), v, w)) 
    return items