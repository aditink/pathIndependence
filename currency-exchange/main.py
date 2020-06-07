from colorama import Fore
import copy
from currencyGraph import CurrencyGraph
import numpy as np
from optimalSetPathChecker import OptimalSetPathChecker
from iPathChecker import IPathChecker
from polynomialPathChecker import PolynomialPathChecker
import requests 
from typing import List

# Assume that a graph doesn't have more edges nodes than this
INFTY = 1000000
NO_EDGE = -1
DEBUG = False
ID_FUNCTION = [-1]

# TODO add:
# 1. Commandline arguments.
# 2. Historic rate.
# 3. Connection to path checking algorithm.

###############################################

epsilon = 0.000000001 # allowed error multiplier

checkers = [
    OptimalSetPathChecker(),
    PolynomialPathChecker()
]

def getPathValue(path: List[int], graph: List[List[int]]):
    """Composition oracle defintion."""
    result = 1
    # Special case for identity function.
    if path == ID_FUNCTION:
        return result
    # Special case for just new edge.
    if len(path) == 1:
        return graph[path[0]][path[0]]
    # Regular case.
    for i in range(len(path)-1):
        result *= graph[path[i]][path[i+1]]
    return result

def getIndependenceFromChecker(checker: IPathChecker, graph: CurrencyGraph):
    """Equality check oracle definition."""
    checker.setGraph(graph.graph)
    checker.setIdFunction(ID_FUNCTION)
    def IndependenceFunction(base, target, rate, newGraph):
        checker.setEdge(graph.indexOf(base), graph.indexOf(target))
        pairsToCheck = checker.getPathsToCheck()
        for (path1, path2) in pairsToCheck:
            path1Value = getPathValue(path1, newGraph)
            path2Value = getPathValue(path2, newGraph)
            if abs(path1Value - path2Value) > epsilon * path2Value:
                return (False, "path 1: {}: {} \n path 2: {}: {} \n difference: {}, new edge: {} -> {}: {}"
                .format(
                path1Value,
                path1,
                path2Value,
                path2,
                path1Value - path2Value,
                base,
                target,
                rate))
        return (True, "Success for base {} target {}".format(base, target))
    return IndependenceFunction
            

for checker in checkers:
    print("Working with {}".format(checker.__class__.__name__))
    graph = CurrencyGraph()
    graph.setup()
    graph.checkIndependenceFunc = getIndependenceFromChecker(checker, graph)
    try:    
        for baseCurrency in graph.currencyList:
            if baseCurrency == graph.base:
                continue
            for targetCurrency in graph.currencyList:
                if (DEBUG):
                    print("Adding edge from {} to {}"
                        .format(baseCurrency, targetCurrency))
                (success, info) = graph.addEntry(baseCurrency, targetCurrency, True)
                if not success:
                    print(Fore.RED + "Adding edge from {} to {} failed for checker {}."
                        .format(
                            baseCurrency,
                            targetCurrency,
                            checker.__class__.__name__))
                    print(info)
                    raise StopIteration
    except:
        pass    
    print(Fore.GREEN + "Completed graph for {}"
        .format(checker.__class__.__name__))
    print('\033[0m')
    graph.printGraph()