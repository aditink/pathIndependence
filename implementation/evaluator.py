from datetime import datetime
import functools
import matplotlib.pyplot as plt
import numpy as np
from pathCheckers.batchChecker import BatchChecker
from pathCheckers.iPathChecker import IPathChecker
from pathCheckers.optimalSetPathChecker import OptimalSetPathChecker
from pathCheckers.polynomialPathChecker import PolynomialPathChecker
from pathCheckers.naiveChecker import NaiveChecker
from pathCheckers.twoFlipChecker import TwoFlipPathChecker
from randomGraphGenerator import generateGraph, generateAcyclicGraph
import traceback
from typing import List

NUM_TRIES = 1

densityStep = 0.5
sizeStep = 2
maxSize = 10

# densities = [i*densityStep for i in range(1, int(1.0/densityStep))] 
densities = [0.1, 0.4]
sizes = [i*sizeStep for i in range(1, int(maxSize/sizeStep))]
# sizes = [10, 50, 100]

evaluationList = [(density, size) for size in sizes for density in densities]

checkers : List[IPathChecker] = [
    #PolynomialPathChecker(),
    OptimalSetPathChecker(),
    # NaiveChecker(),
    #TwoFlipPathChecker(),
    BatchChecker()
]

class attemptInfo:
    """Stores information for a given density, size"""

    def __init__(self):
        self.times = []
        self.sizes = []
    
    def addTime(self,time):
        self.times += [time]
    
    def addSize(self, sze):
        self.sizes += [sze]
    
    def avgList(self, lst):
        return functools.reduce(lambda  acc, n: acc + n, lst, 0)/len(lst)
    
    def getAvgTime(self):
        return self.avgList(self.times)

    def getAvgSizes(self):
        return self.avgList(self.sizes)


def getEvaluateFunction(checker: IPathChecker, numTries: int, acyclic=False):
    if isinstance(checker, BatchChecker):
        def evaluate(density, size):
            info = attemptInfo()
            for attempt in range(numTries):
                inp = generateAcyclicGraph(density, size)
                checker.setGraph(inp.graph)
                paths = checker.getPathsToCheck()
                info.addSize(len(paths))
                info.addTime(checker.getComputeTime())
            return info
        return evaluate
    def evaluate(density, size):
        info = attemptInfo()
        for attempt in range(numTries):
            if (acyclic):
                inp = generateAcyclicGraph(density, size)
            else:
                inp = generateGraph(density, size)
            checker.setGraph(inp.graph)
            checker.setEdge(inp.newEdgeSource, inp.newEdgeSink)
            paths = checker.getPathsToCheck()
            info.addSize(len(paths))
            info.addTime(checker.getComputeTime())
        return info
    return evaluate

def plot3d(checkerName, results):
    plt.clf()
    X, Y = np.meshgrid(densities, sizes)
    Z = [[results[(x, y)].getAvgTime() for x in densities] for y in sizes]

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.contour3D(X, Y, Z, 50, zdir='z')
    ax.set_xlabel('Density')
    ax.set_ylabel('Size')
    ax.set_zlabel('time')

    # plt.show()
    fig.savefig("results/result3d{}{}.png".format(checkerName, datetime.utcnow()))
    plt.clf()

def plotTimeVsSize(checkerName, results, densities):
    plt.clf()
    handles = []

    X = sizes
    for density in densities:
        try:
            Y = [results[(density, size)].getAvgTime() for size in sizes]
            handles += plt.plot(X, Y, label="density {}".format(density))
        except:
            print("No results for density {}".format(density))
            print(traceback.print_stack())
    plt.legend(handles=handles)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Execution Time (seconds)')
    plt.savefig("results/timeVsSize_{}_{}{}.png".format(NUM_TRIES, checkerName, datetime.utcnow()))
    plt.clf()

def plotTimeVsSizeForChecker(checkerNames, results, density):
    plt.clf()
    handles = []

    X = sizes
    for checkerName in checkerNames:
        try:
            Y = [results[checkerName][(density, size)].getAvgTime() for size in sizes]
            handles += plt.plot(X, Y, label=checkerName)
        except:
            print("Error for {}".format(checkerName))
            print(traceback.print_stack())
    plt.legend(handles=handles)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Execution Time (seconds)')
    plt.savefig("results/timeVsSizeForChecker_{}_{}.png".format(NUM_TRIES, datetime.utcnow()))
    plt.clf()

def plot(checkerName, results):
    # plot3d(checkerName, results)
    # Modify densities to plot only a subset of those computed.
    plotTimeVsSize(checkerName, results, densities)

checkerToResults = dict()
for checker in checkers:
    evaluate = getEvaluateFunction(checker, NUM_TRIES)
    # dictionary from (density, size) to attemptInfo
    results = { (density, size) : evaluate(density, size) for 
        density in densities for size in sizes }
    checkerToResults[checker.__class__.__name__] = results
    plot(checker.__class__.__name__, results)
