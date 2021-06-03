from typing import List
from ortools.algorithms import pywrapknapsack_solver
from Utils.knapsack import Item, Knapsack
from Solvers.classicSolutions import kpBacktracking, kpDP
from Solvers.Heuristics.hyperheuristic import (HyperheuristicNaive,
                                               hyperheuristicSolver)
from Solvers.Heuristics.metaheuristic import solveMetaheuristic
from Solvers.Heuristics.simpleHeuristic import (SimpleHeuristic,
                                                heuristicComparison)


def kpMILP(W: int, items: List[Item]):
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_CBC_MIP_SOLVER, 'Knapsack BC-MILP')
    
    profit = [item.getProfit() for item in items]
    weights = [[item.getWeight() for item in items]]
    capacities = [W]
    solver.Init(profit, weights, capacities)
    solver.Solve()

    kp = Knapsack(W)
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
    if method == 'Heuristic':
        simple_heuristic = SimpleHeuristic(additionalArgs)
        return ConstructiveSolution(kp, items, simple_heuristic).getValue()
    elif method == 'SimulatedAnnealing':
        return solveMetaheuristic(method, kp, items, additionalArgs)
    elif method == 'RandomSearch':
        return solveMetaheuristic(method, kp, items, additionalArgs)
    elif method == 'HyperheuristicNaive':
        hh = HyperheuristicNaive(additionalArgs)
        return ConstructiveSolution(kp, items, hh).getValue()
    elif method == 'Hyperheuristic':
        return hyperheuristicSolver(kp, items, additionalArgs).getValue()
    elif method == 'Backtracking':
        return kpBacktracking(kp.getCapacity(), items).getValue()
    elif method == 'DP':
        return kpDP(kp.getCapacity(), items).getValue()
    elif method == 'MILP':
        return kpMILP(kp.getCapacity(), items).getValue()
    elif method in list(heuristicComparison.keys()):
        simple_heuristic = SimpleHeuristic(method)
        return ConstructiveSolution(kp, items, simple_heuristic).getValue()
    else:
        return 0
