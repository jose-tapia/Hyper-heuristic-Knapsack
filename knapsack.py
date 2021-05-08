import numpy as np
import timeit
import random 

class Item(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = int(v)
        self.weight = int(w)
    def getValue(self):
        return self.value
    def getWeight(self):
        return self.weight
    def getRatio(self):
        return self.getValue()/self.getWeight()
    def __str__(self):
        return f' Item: {self.name}, <Value: {str(self.value)}, Weight: {str(self.weight)}>'
    
def buildOptions( values, weights):
    items = []
    numItems = len(values)
    for i in range(numItems):
        items.append(Item(str(i), values[i],
                          weights[i]))
    return items


# A Greedy Approach: an approximate solution
def ksGreedy(items, knapsackCap, strategy):
        
    itemsCopy = sorted(items, key = strategy, reverse = True)
    taken = []
    totalVal, totalWeight = 0.0,0.0
    for i in range(len(itemsCopy)):
        if (totalWeight + itemsCopy[i].getWeight()) <= knapsackCap: #available resources
            taken.append(itemsCopy[i])
            totalVal += itemsCopy[i].getValue()
            totalWeight += itemsCopy[i].getWeight()
    return (totalVal, taken)

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
            if item == 0 or weight == 0:
                A[item,weight] = 0 
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
    elif algorithm == 'ksBruteForce':
        print(f'Algorithm: BruteForce')
        val,taken= ksRecursive(items,knapsackCap)
        if show : 
            print(f'Value obtained  = {val}')
            for item in taken:
                print('   ', item)
        
    print('-------------------------------------')
    return int(val)

def buildInstance(num_items, max_V, max_W):
    '''
    Returns: examples of random items with weights and values
    '''
    random_items = []
    for item in range(num_items):
        random_items.append(Item(str(item),random.randint(1,max_V),
                          random.randint(1,max_W)))
    values = []
    weights = []
    for i in random_items:
        values.append(i.getValue())
        weights.append(i.getWeight())
    return random_items , values, weights

#load instances
def load_data(path):
    file = open(path, "r")
    data = file.readlines()
    values_set =[]
    weight_set = []
    for i,line in enumerate(data):
        items = line.split(',')
        if i == 0: numItems,knapsackCap = int(items[0]),int(items[1])  #Number of items, Knapsack capacity
        else:
            weight_set.append(int(items[0]))# For each bin: weight, profit
            values_set.append(float(items[1]))
    return knapsackCap,numItems, values_set, weight_set

if __name__ == '__main__':
    
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


    val4 =printSolver(items, knapsackCap, 'ksDP', True)
    time4 = timeit.timeit('ksDP(items,knapsackCap)', number = 1 , globals = globals())
    print('Time: ',time4,'seconds.')
    
    val5 =printSolver(items, knapsackCap, 'ksBruteForce', True)
    time5 = timeit.timeit('ksRecursive(items,knapsackCap)', number = 1 , globals = globals())
    print('Time: ',time5,'seconds.')

    methods = ['max-profit','min-weight','max-profit/weight','DP','BruteForce']
    vals = [val1, val2,val3,val4,val5]
    times =[time1,time2,time3,time4,time5]
    best_t = min(times)
    best_v = max(vals)
    ix_t = times.index(best_t)
    ix_v = vals.index(best_v)
    print('-------------------------------------')
    print('Best Solution')
    print('-------------------------------------')
    print(f'Best time: {best_t}, Method: {methods[ix_t]}.')
    print(f'Best value: {best_v}, Method: {methods[ix_v]}.')