from typing import List
from knapsack import Item, Knapsack
from simpleHeuristic import SimpleHeuristic, heuristicComparison
from metaheuristic import solveMetaheuristic
from hyperheuristic import HyperheuristicNaive, hyperheuristicSolver
from exactSolvers import kpBacktracking, kpDP
from ortools.algorithms import pywrapknapsack_solver

def kpIP(C: int, items: List[Item]):
    solver = pywrapknapsack_solver.KnapsackSolver(
    pywrapknapsack_solver.KnapsackSolver.
    KNAPSACK_MULTIDIMENSION_CBC_MIP_SOLVER, 'KnapsackExample')
    
    profit = [item.getProfit() for item in items]
    weights = [[item.getWeight() for item in items]]
    capacities = [C]
    solver.Init(profit, weights, capacities)
    #solver.set_time_limit(20)
    computed_value = solver.Solve()

    kp = Knapsack(C)
    for i, item in enumerate(items):
        if solver.BestSolutionContains(i):
            kp.pack(item)
    return kp

def ConstructiveSolution(kp: Knapsack, items: List[Item], itemSelector):
    nextItem = itemSelector.nextItem(kp, items)
    while nextItem is not None:
        kp.pack(items[nextItem])
        items.pop(nextItem)
        nextItem = itemSelector.nextItem(kp, items)
    return kp


def solver(method: str, kp: Knapsack, items: List[Item], additionalArgs = None):
    if method == 'heuristic':
        simple_heuristic = SimpleHeuristic(additionalArgs)
        return ConstructiveSolution(kp, items, simple_heuristic).getValue()
    elif method == 'SimulatedAnnealing':
        return solveMetaheuristic(method, kp, items, additionalArgs)
    elif method == 'RandomSearch':
        return solveMetaheuristic(method, kp, items, additionalArgs)
    elif method == 'hyperheuristicNaive':
        hh = HyperheuristicNaive(additionalArgs)
        return ConstructiveSolution(kp, items, hh).getValue()
    elif method == 'hyperheuristic':
        return hyperheuristicSolver(kp, items, additionalArgs).getValue()
    elif method == 'recursive':
        return kpBacktracking(kp.getCapacity(), items).getValue()
    elif method == 'DP':
        return kpDP(kp.getCapacity(), items).getValue()
    elif method == 'IP':
        return kpIP(kp.getCapacity(), items).getValue()
    elif method in list(heuristicComparison.keys()):
        simple_heuristic = SimpleHeuristic(method)
        return ConstructiveSolution(kp, items, simple_heuristic).getValue()
    else:
        return 0
