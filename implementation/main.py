"""Currency graph evaluation."""

import copy
import time
import traceback
from typing import List

import numpy as np
import requests
from colorama import Fore

from currencyGraph.currencyGraph import CurrencyGraph
from pathCheckers.iPathChecker import IPathChecker
from pathCheckers.optimalSetPathChecker import OptimalSetPathChecker
from pathCheckers.polynomialPathChecker import PolynomialPathChecker

# Assume that a graph doesn't have more edges nodes than this
INFTY = 1000000
NO_EDGE = -1
DEBUG = False

ID = [-1]
ID_PATH = [ID]
ID_FUNCTION = lambda source : ID_PATH

# TODO add:
# 1. Commandline arguments.
# 2. Historic rate.

###############################################

epsilon = 1E-4 # allowed error multiplier

checkers = [
    OptimalSetPathChecker(),
    PolynomialPathChecker()
]

def getPathValue(path: List[int], graph: List[List[int]]):
    """Composition oracle defintion."""
    result = 1
    # Special case for identity function.
    if path == ID_PATH:
        return result
    # Special case for just new edge.
    if len(path) == 1:
        return graph[path[0]][path[0]]
    # Regular case.
    for i in range(len(path)-1):
        result *= graph[path[i]][path[i+1]]
    return result

def independenceFuncFactory(checker: IPathChecker, graph: CurrencyGraph):
    """Equality check oracle definition."""
    checker.setGraph(graph.graph)
    checker.setIdFunction(ID_FUNCTION)
    def IndependenceFunction(base, target, rate):
        checker.setEdge(graph.indexOf(base), graph.indexOf(target))
        pairsToCheck = checker.getPathsToCheck()
        newGraph = graph.getCopyWithNewEdge(base, target, rate)
        for (path1, path2) in pairsToCheck:
            path1Value = getPathValue(path1, newGraph)
            path2Value = getPathValue(path2, newGraph)
            if abs(path1Value - path2Value) > epsilon:
                return (False, "path 1: {}: {} \npath 2: {}: {} \n difference: {}, new edge: {} -> {}: rate: {}"
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
            
totalCheckerTimes = dict() # checker -> (total seconds, number of runs)

for day in range(1, 31):
    month = 1
    year = 2020
    if (DEBUG):
        print("{}-{}-{}".format(day, month, year))
    for checker in checkers:
        print("Working with {}".format(checker.__class__.__name__))
        startTime = time.time()
        graph = CurrencyGraph()
        graph.setupWithDay(day = day, month = month, year = year)
        graph.checkIndependenceFunc = independenceFuncFactory(checker, graph)
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
            endTime = time.time()
            timeTaken = endTime - startTime - graph.sleepTime
            print(Fore.GREEN + "Completed graph for {} in {} seconds."
            .format(checker.__class__.__name__, timeTaken))
            oldTime = totalCheckerTimes.get(checker, [])
            totalCheckerTimes[checker] = oldTime + [timeTaken]
        except Exception as e:
            print(Fore.RED + "Aborted building graph for {}"
            .format(checker.__class__.__name__))
            print(e)
        except:
            print(Fore.RED + "Aborted building graph for {}"
            .format(checker.__class__.__name__))
            traceback.print_exc()
        print('\033[0m')
        if DEBUG:        
            print('Resultant graph:')
            print(graph.currencyList)
            graph.printGraph()

for checker, timeList in totalCheckerTimes.items():
    mean = sum(timeList) / len(timeList) 
    variance = sum([((x - mean) ** 2) for x in timeList]) / len(timeList) 
    standardDeviation = variance ** 0.5
    print("Checker {} took {} seconds with standard deviation {} in {} runs"
        .format(
            checker.__class__.__name__,
            mean, 
            standardDeviation, 
            len(timeList)))
