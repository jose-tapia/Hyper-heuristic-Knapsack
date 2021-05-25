from typing import List
from knapsack import Item, Knapsack
from simpleHeuristic import SimpleHeuristic
from metaheuristic import solveMetaheuristic
from hyperheuristic import HyperheuristicNaive, hyperheuristicSolver
from exactSolvers import kpBacktracking, kpDP

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
    else:
        return 0
