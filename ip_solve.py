import numpy as np
import timeit
import random 

from ortools.algorithms import pywrapknapsack_solver

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
    def getValuePouch(self,avgW):
        return (self.getValue()*self.getWeight())/avgW
    

    def __str__(self):
        return f' Item: {self.name}, <Value: {str(self.value)}, Weight: {str(self.weight)}>'

def ksBB(items, knapsackCap):
    solver = pywrapknapsack_solver.KnapsackSolver(
    pywrapknapsack_solver.KnapsackSolver.
    KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')
    
    values = list()
    weights1 = list()
    for item in range(len(items)):
        values.append(items[item].getProfit())
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

def IPSolve(items, knapsackCap, show = True):
        
        val,taken= ksBB(items,knapsackCap)
        if show : 
            print(f'IP profit = {val}')
            for item in taken:
                print('   ', item)
                print('-------------------------------------')
        return int(val)

