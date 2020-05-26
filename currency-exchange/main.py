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

# TODO add:
# 1. Commandline arguments.
# 2. Historic rate.
# 3. Connection to path checking algorithm.

###############################################

epsilon = 0.001 # allowed error percent

checkers = [
    OptimalSetPathChecker(),
    PolynomialPathChecker()
]

def getPathValue(path: List[int], graph: CurrencyGraph):
    """Composition oracle defintion."""
    result = 1
    for i in range(len(path)-1):
        result *= graph.graph[path[i]][path[i+1]]
    return result

def getIndependenceFromChecker(checker: IPathChecker, graph: CurrencyGraph):
    """Equality check oracle definition."""
    checker.setGraph(graph.graph)
    def IndependenceFunction(base, target, rate):
        checker.setEdge(graph.indexOf(base), graph.indexOf(target))
        pairsToCheck = checker.getPathsToCheck()
        for (path1, path2) in pairsToCheck:
            path1Value = getPathValue(path1, graph)
            path2Value = getPathValue(path2, graph)
            if (path1Value - path2Value) > epsilon * path2Value:
                return False
        return True
    return IndependenceFunction
            

for checker in checkers:
    print("Working with {}".format(checker.__class__.__name__))
    graph = CurrencyGraph()
    graph.setup()
    graph.checkIndependenceFunc = getIndependenceFromChecker(checker, graph)
    for baseCurrency in graph.currencyList:
        if baseCurrency == graph.base:
            continue
        for targetCurrency in graph.currencyList:
            print("Adding edge from {} to {}"
                .format(baseCurrency, targetCurrency))
            success = graph.addEntry(baseCurrency, targetCurrency, True)
            print(success)
    print("Completed graph for {}".format(checker.__class__.__name__))
    graph.printGraph()