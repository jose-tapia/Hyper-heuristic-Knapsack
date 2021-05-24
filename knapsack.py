class Item(object):
    def __init__(self, id, p: int, w: int):
        self.name = id
        self.profit = p
        self.weight = w
    
    def getName(self):
        return self.name

    def getProfit(self):
        return self.profit

    def getWeight(self):
        return self.weight

    def getRatio(self):
        return self.profit/self.weight

    def __str__(self):
        return f' Item: {self.name}, <Profit: {str(self.profit)}, Weight: {str(self.weight)}>'

class Knapsack(object):
    def __init__(self, C: int):
        self.capacity = C
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
            self.value += item.getProfit()
            self.items.append(item)

    def unpack(self, idx: int):
        if 0 <= idx and idx < len(self.items):
            self.capacity += self.items[idx].getWeight()
            self.value -= self.items[idx].getProfit()
            return self.items.pop(idx)
        else:
            return None
    
    def copy(self):
        kp = Knapsack(self.capacity)
        kp.value = self.value
        kp.items = self.items
        return kp
            
    def printKnapsack(self):
        print(self)
        for item in self.items:
            print('\t', item)

    def __str__(self):
        return f' Knapsack instance: <Capacity: {str(self.capacity)}, Value: {str(self.value)}, items: {str(len(self.items))}>'

def generateItemsList(vList: [int], wList: [int]):
    items = []
    if len(vList) == len(wList):
        for id, v, w in zip(range(1, len(vList)+1), vList, wList):
            items.append(Item(str(id), v, w)) 
    return items