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
    # Prepare the solver
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_CBC_MIP_SOLVER, 'Knapsack BC-MILP')
    
    # Prepare the data
    profit = [item.getProfit() for item in items]
    weights = [[item.getWeight() for item in items]]
    capacities = [W]

    # Execute the solver
    solver.Init(profit, weights, capacities)
    solver.Solve()

    # Find the best solution
    kp = Knapsack(W)
    for i, item in enumerate(items):
        if solver.BestSolutionContains(i):
            kp.pack(item)
    return kp

def ConstructiveSolution(kp: Knapsack, items: List[Item], itemSelector):
    # Find the first item to pack to the knapsack
    nextItem = itemSelector.nextItem(kp, items)

    while nextItem is not None:
        # Pack the items until no other item can be packed
        kp.pack(items[nextItem])
        items.pop(nextItem)
        nextItem = itemSelector.nextItem(kp, items)
    
    # Return the solution reached
    return kp

def solver(method: str, kp: Knapsack, items: List[Item], additionalArgs = None):
    if method == 'Heuristic':
        # Execute the heuristic method
        simple_heuristic = SimpleHeuristic(additionalArgs)
        return ConstructiveSolution(kp, items, simple_heuristic).getValue()
    elif method == 'SimulatedAnnealing':
        # Execute the Simulated Annealing metaheuristic
        return solveMetaheuristic(method, kp, items, additionalArgs)
    elif method == 'RandomSearch':
        # Execute the Random Search metaheuristic
        return solveMetaheuristic(method, kp, items, additionalArgs)
    elif method == 'HyperheuristicNaive':
        # Execute the Hyper-heuristic naive model
        hh = HyperheuristicNaive(additionalArgs)
        return ConstructiveSolution(kp, items, hh).getValue()
    elif method == 'Hyperheuristic':
        # Execute the Hyper-heuristic based on LSTM model
        return hyperheuristicSolver(kp, items, additionalArgs).getValue()
    elif method == 'Backtracking':
        # Execute the recursive backtracking method 
        return kpBacktracking(kp.getCapacity(), items).getValue()
    elif method == 'DP':
        # Execute the dynamic programming method
        return kpDP(kp.getCapacity(), items).getValue()
    elif method == 'MILP':
        # Execute the mixed integer linear programming method
        return kpMILP(kp.getCapacity(), items).getValue()
    elif method in list(heuristicComparison.keys()):
        # Given the heuristic as method parameter, execute the constructive heuristic method
        simple_heuristic = SimpleHeuristic(method)
        return ConstructiveSolution(kp, items, simple_heuristic).getValue()
    else:
        return 0
