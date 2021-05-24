

#%%
import numpy as np
import timeit
import random 


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

    def getValuePouch(self,avgW):
        return (self.getValue()*self.getWeight())/avgW
    


    def __str__(self):
        return f' Item: {self.name}, <Profit: {str(self.profit)}, Weight: {str(self.weight)}>'

class Knapsack(object):
    def __init__(self, C: int):
        self.capacity = C
        self.value = 0
        self.items = []

    def getCapacity(self):
        return self.capacity
      
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
 
 def __str__(self):
    return f' Knapsack instance: <Capacity: {str(self.capacity)}, Value: {str(self.value)}, items: {str(len(self.items))}>'

    def getValue(self):
        return self.value

    def getPackedItems(self):
        return self.items

    def canPack(self, item: Item):
        return item.getWeight() <= self.capacity
=======
    itemsCopy = sorted(items, key = strategy, reverse = True)
    taken = []
    totalVal, totalWeight = 0.0,0.0
    for i in range(len(itemsCopy)):
        if (totalWeight + itemsCopy[i].getWeight()) <= knapsackCap: #available resources
            taken.append(itemsCopy[i])
            totalVal += itemsCopy[i].getValue()
            totalWeight += itemsCopy[i].getWeight()
    return (totalVal, taken)

# A Greedy Approach: an approximate solution
def ksPouch(items, knapsackCap):
    avgW = sum([item.getWeight() for item in items])/len(items)
    items = [(item.getValuePouch(avgW),item.getWeight(),item.getValue(),idx) for idx,item in enumerate(items)]
    itemsCopy = sorted(items, reverse = True)
    res = []
    totalVal, totalWeight = 0.0,0.0
    for i in range(len(itemsCopy)):
        if (totalWeight + itemsCopy[i][1]) <= knapsackCap: #available resources
            res.append((itemsCopy[i][3],itemsCopy[i][2],itemsCopy[i][1]))
            totalVal += itemsCopy[i][2]
            totalWeight += itemsCopy[i][1]
    taken =[]
    for n,v,w in res :
        taken.append(Item(n,v,w))
    
    return totalVal, taken



#Brute Force - Optimal Solution - High Time Complexity
def ksRecursive(items,knapsackCap):
    '''
    Input: the list of items(objects with weight and value)  and the capacity of the knapsack
    Returns: a tuple with total value and solution to the problem
    '''
    if items == [] or knapsackCap == 0: #Base Cases
        result = (0, ())
    elif items[0].getWeight() > knapsackCap : #Capacity Constraint: if the weight of the
         #item is more than the capacity then it cannot be included
        result = ksRecursive(items[1:], knapsackCap) #consider the following items
        
    else: # available space
        checkItem = items[0] 
        #Case 1 : evaluate when item is excluded 
        withoutValue, withoutItem = ksRecursive(items[1:], 
                                            knapsackCap)
        #Case 2 : evaluate wjhen item is included 
        withValue, withItem = ksRecursive(items[1:],
                                      knapsackCap-checkItem.getWeight())
        withValue += checkItem.getValue()
        
        #take the decision that maximizes Value
        if withoutValue < withValue: # if the value by excluding the item is smaller 
        #than the value by including the value
            #include the item
            result = (withValue, withItem +(checkItem,))
        else: 
            #exclude the item
            result = (withoutValue, withoutItem)
    return result


# Dynamic Programming approach bottom-up Iterative 
def ksDP(items,knapsackCap):
    '''
    Input: the list of items(objects with weight and value)  and the capacity of the knapsack
    Returns: a tuple with total value and a solution to the problem
    '''
    # Build matrix in a bottom up-manner 
    A = np.zeros([len(items),knapsackCap+1])
    for item in range(len(items)):
        for weight in range(knapsackCap+1):
            if weight == 0:
                A[item,weight] = 0
            if item == 0 : 
                if items[item].getWeight() <= weight:
                    A[item,weight] = items[item].getValue()
            elif weight >= items[item].getWeight(): # if available space
                A[item,weight] = max(A[item-1,weight], 
                                     A[item-1,weight-items[item].getWeight()] +
                                     items[item].getValue())
            else: #no space available
                A[item, weight] = A[item-1, weight]
    #store results of knapsack
    total_value = A[-1][-1]
    cap = knapsackCap
    val = total_value
    taken = []
    for i in range(len(items), 0, -1):
        if val <= 0 : break
        elif val == A[i-1,cap]: continue
        else: 
            val = val - items[i].getValue()
            cap = cap - items[i].getWeight()
            taken.append(items[i])
    return total_value,taken

from ortools.algorithms import pywrapknapsack_solver

def ksBB(items, knapsackCap):
    solver = pywrapknapsack_solver.KnapsackSolver(
    pywrapknapsack_solver.KnapsackSolver.
    KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')
    
    values = list()
    weights1 = list()
    for item in range(len(items)):
        values.append(items[item].getValue())
        weights1.append(items[item].getWeight())

    weights = [weights1]
    capacities = [knapsackCap]
    solver.Init(values, weights, capacities)
    computed_value = solver.Solve()
    packed_items = []
    packed_weights = []
    total_weight = 0
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]
    taken =[]
    for j in packed_items :
        taken.append(Item(str(j),values[j],weights1[j]))
    return computed_value,taken

#Print the solution
def printSolver(items, knapsackCap, algorithm, show = True):
    print('-------------------------------------')
    if algorithm == 'ksDP':
        print(f'Algorithm: DP')
        val,taken= ksDP(items, knapsackCap)
        if show : 
            print(f'Value obtained  = {val}')
            for item in taken:
                print('   ', item)
    elif algorithm == 'ksGreedy-MaxVal':
        print(f'Algorithm: max-profit')
        strategy = Item.getValue #max Value 
        val,taken= ksGreedy(items,knapsackCap,strategy)
        if show : 
            print(f'Value obtained  = {val}')
            for item in taken:
                print('   ', item)
    elif algorithm == 'ksGreedy-Pouch':
        print(f'Algorithm: Pouch')

        val,taken= ksPouch(items,knapsackCap)
        if show : 
            print(f'Value obtained  = {val}')
            for item in taken:
                print('   ', item)

    elif algorithm == 'ksGreedy-MinWeight':
        print(f'Algorithm: min-weight')
        strategy = lambda x: 1/Item.getWeight(x) #min weight
        val,taken= ksGreedy(items,knapsackCap,strategy)
        if show : 
            print(f'Value obtained  = {val}')
            for item in taken:
                print('   ', item)
    elif algorithm == 'ksGreedy-ValWeiRatio':
        print(f'Algorithm: max-profit/weight')
        strategy = Item.getRatio #ratio of value over size
        val,taken= ksGreedy(items,knapsackCap,strategy)
        if show : 
            print(f'Value obtained  = {val}')
            for item in taken:
                print('   ', item)
    elif algorithm == 'ksGreedy-Default':
        print(f'Algorithm: Default')
        val,taken= defaultGreedy(items,knapsackCap)
        if show : 
            print(f'Value obtained  = {val}')
            for item in taken:
                print('   ', item)
    elif algorithm == 'ksRecursive':
        print(f'Algorithm: Brute Force')
        val,taken= ksRecursive(items,knapsackCap)
        if show : 
            print(f'Value obtained  = {val}')
            for item in taken:
                print('   ', item)
    elif algorithm == 'ksBB':
        print(f'Algorithm: IP')
        val,taken= ksBB(items,knapsackCap)
        if show : 
            print(f'Value obtained  = {val}')
            for item in taken:
                print('   ', item)

        
    print('-------------------------------------')
    return int(val)

    def copy(self):
        kp = Knapsack(self.capacity)
        kp.value = self.value
        kp.items = self.items
        return kp
            
    def printKnapsack(self):
        print(self)
        for item in self.items:
            print('\t', item)

    knapsackCap,numItems, values_set, weight_set = load_data("/Volumes/GoogleDrive/My Drive/MCCNotes/Jlab projects/GITHUB_repositories/DANY_repositories/Hyper-heuristic-Knapsack/Instances/test.txt")
    items = buildOptions(values_set,weight_set)

    #examples = [5,10,20,30,40,50,100,150,180,200]
    #examples = [60]
    #knapsackCap = 100
    #maxVal = 100
    #maxWei = 250
    #for j in examples:
        #numItems, numItems, weight_set  = buildInstance(j,maxVal,maxWei)
        
    print('-------------------------------------')
    print(f'Number of Items: {len(items)}')
    print(f'Knapsack Capacity: {knapsackCap}')
    print(f'Values List: {values_set}')
    print(f'Weights List: {weight_set}')
    val1 = printSolver(items, knapsackCap,'ksGreedy-MaxVal', True)
    time1 = timeit.timeit("ksGreedy(items,knapsackCap,Item.getValue)", number = 1 , globals = globals())
    print('Time: ', time1, 'seconds.')

    val2 = printSolver(items, knapsackCap,'ksGreedy-MinWeight', True)
    time2 = timeit.timeit("ksGreedy(items,knapsackCap,lambda x: 1/Item.getWeight(x))", number = 1 , globals = globals())
    print('Time: ', time2, 'seconds.')

    val3 = printSolver(items, knapsackCap,'ksGreedy-ValWeiRatio', True)
    time3 = timeit.timeit("ksGreedy(items,knapsackCap,Item.getRatio)", number = 1 , globals = globals())
    print('Time: ', time3, 'seconds.')
    
    val4 = printSolver(items, knapsackCap,'ksGreedy-Default', True)
    time4 = timeit.timeit("defaultGreedy(items,knapsackCap)", number = 1 , globals = globals())
    print('Time: ', time4, 'seconds.')


def generateItemsList(vList: [int], wList: [int]):
    items = []
    if len(vList) == len(wList):
        for id, v, w in zip(range(1, len(vList)+1), vList, wList):
            items.append(Item(str(id), v, w)) 
    return items
=======
    val5 =printSolver(items, knapsackCap, 'ksDP', True)
    time5 = timeit.timeit('ksDP(items,knapsackCap)', number = 1 , globals = globals())
    print('Time: ',time5,'seconds.')
    
    val6 =printSolver(items, knapsackCap, 'ksGreedy-Pouch', True)
    time6 = timeit.timeit('ksPouch(items,knapsackCap)', number = 1 , globals = globals())
    print('Time: ',time6,'seconds.')
    
    val7 =printSolver(items, knapsackCap, 'ksBB', True)
    time7 = timeit.timeit('ksBB(items,knapsackCap)', number = 1 , globals = globals())
    print('Time: ',time7,'seconds.')
    
    methods = ['max-profit','min-weight','max-profit/weight','greedy-default','DP','Pouch','Heuristic']
    vals = [val1, val2,val3,val4,val5,val6,val7]
    times =[time1,time2,time3,time4,time5,time6,time7]
    best_t = min(times)
    best_v = max(vals)
    ix_t = times.index(best_t)
    ix_v = vals.index(best_v)
    print('-------------------------------------')
    print('Best Solution')
    print('-------------------------------------')
    print(f'Best time: {best_t}, Method: {methods[ix_t]}.')
    print(f'Best value: {best_v}, Method: {methods[ix_v]}.')
# %%
