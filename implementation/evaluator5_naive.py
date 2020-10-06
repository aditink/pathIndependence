from datetime import datetime
import cProfile
import functools
import json
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

NUM_TRIES = 10
DO_ACYCLIC = False
OUTFILE = ''

densityStep = 0.5
sizeStep = 1
maxSize = 10

# densities = [i*densityStep for i in range(1, int(1.0/densityStep))] 
densities = [0.1, 0.5, 0.9]
sizes = [i*sizeStep for i in range(1, int(maxSize/sizeStep))]
# sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

evaluationList = [(density, size) for size in sizes for density in densities]

# First three colors look good in black and white.
colors = ["black", "purple", "orange", "blue", "green", "red"]

checkers : List[IPathChecker] = [
    # PolynomialPathChecker(),
    # OptimalSetPathChecker(),
    NaiveChecker()
    # TwoFlipPathChecker()
    # BatchChecker()
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
        self.avg = functools.reduce(lambda  acc, n: acc + n, lst, 0)/len(lst)
        return self.avg
    
    def getAvgTime(self, median=False): 
        if median:
            return self.getMedianTime()
        return self.avgList(self.times)

    def getAvgSizes(self):
        return self.avgList(self.sizes)
    
    def getTimes(self):
        return self.times

    def getMedianTime(self):
        copy = self.times
        copy.sort()
        if len(copy)%2 == 1:
            self.median = copy[int(len(copy)/2)+1]
        else:
            floor = int(len(copy)/2)
            self.median = (copy[floor] + copy[floor+1])/2
        return self.median

    def getSD(self):
        mean = sum(self.times) / len(self.times) 
        variance = sum([((x - mean) ** 2) for x in self.times]) / len(self.times) 
        standardDeviation = variance ** 0.5
        return standardDeviation

class runDetails:
    """Stores details of this evaluation run."""
     
    def __init__(self):
        self.size = -1
        self.density = -1
        self.checkerName = "not specified"
        self.numberOfTries = NUM_TRIES
        self.graphs = []
    
def generateGraphs(size, density, count=NUM_TRIES, acyclic=False):
    """Generate a list of graphs with the specifications"""
    if acyclic:
        return [generateAcyclicGraph(density, size) for i in range(count)]
    
    return [generateGraph(density, size) for i in range(count)]

def getEvaluateFunction(checker: IPathChecker, numTries: int, acyclic=False):
    """Evaluate function factory"""
    # Need to change this if. BatchChecker evaluate should take in only acyclic graphs.
    if isinstance(checker, BatchChecker):
        def evaluate(density, size, graphs=[]):
            if len(graphs)==0:
                graphs = generateGraphs(size, density, numTries, acyclic=True)
            info = attemptInfo()
            for attempt in range(numTries):
                inp = graphs[attempt]
                checker.setGraph(inp.graph)
                paths = checker.getPathsToCheck()
                info.addSize(len(paths))
                info.addTime(checker.getComputeTime())
            return info
        return evaluate
    def evaluate(density, size, graphs=[]):
        info = attemptInfo()
        if len(graphs)==0:
                graphs = generateGraphs(size, density, numTries, acyclic=acyclic)
        for attempt in range(numTries):
            inp = graphs[attempt]
            checker.setGraph(inp.graph)
            checker.setEdge(inp.newEdgeSource, inp.newEdgeSink)
            paths = checker.getPathsToCheck()
            info.addSize(len(paths))
            info.addTime(checker.getComputeTime())
        return info
    return evaluate

def plot3d(checkerName, results):
    """Plot mesh for density, size and time."""
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
    fig.savefig("results/result3d{}{}.pdf".format(checkerName, datetime.utcnow()))
    plt.clf()

def plotTimeVsSize(checkerName, results, densities, scatterPoints=False,
errorBars=False, median=False):
    plt.clf()
    handles = []
    fig,(ax1)=plt.subplots(1,1)

    X = sizes
    for i in range(len(densities)):
        density = densities[i]
        try:
            Y = [results[(density, size)].getAvgTime(median) for size in sizes]
            if errorBars:
                yerr = [results[(density, size)].getSD() for size in sizes]
                ax1.errorbar(X, Y, yerr=yerr, label="density {}".format(density),
                    color=colors[i])
            else:
                ax1.plot(X, Y, label="density {}".format(density), color=colors[i])
            if scatterPoints:
                for x in sizes:
                    result = results[(density, x)]
                    points = result.getTimes()
                    ax1.plot([x for point in points], points, '.', color=colors[i]) 
                    # ax1.plot([x for point in points], points, '.', color="grey") 
        except:
            print("Exception while plotting for density {}".format(density))
            print(traceback.print_stack())
    handles, labels = ax1.get_legend_handles_labels()
    ax1.legend(handles, labels, loc='upper left',numpoints=1)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Execution Time (seconds)')
    plt.savefig("results/timeVsSize_{}_{}{}.pdf".format(NUM_TRIES, checkerName, datetime.utcnow()))
    plt.clf()

def plotTimeVsSizeForChecker(checkerNames, results, density, scatterPoints=False,
errorBars=False):
    plt.clf()
    handles = []

    X = sizes
    for checkerName in checkerNames:
        try:
            Y = []
            yerr = []
            for size in sizes:
                result = results[checkerName][(density, size)]
                Y += [result.getAvgTime()]
                yerr += [result.getSD()]
            if (errorBars):
                handles += plt.errorbar(X, Y, yerr=yerr, label=checkerName)
            else:
                handles += plt.plot(X, Y, label=checkerName) 
        except:
            print("Error for {}".format(checkerName))
            print(traceback.print_stack())
    plt.legend(handles=handles)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Execution Time (seconds)')
    if scatterPoints:
        for x in X:
            points = result.getTimes()
            plt.plot([x for point in points], points, '.')
    if errorBars:
        #TODO plot standard deviation.
        pass
    plt.savefig("results/timeVsSizeForChecker_{}_{}.pdf".format(NUM_TRIES, datetime.utcnow()))
    plt.clf()

def plot(checkerName, results):
    # plot3d(checkerName, results)
    # Modify densities to plot only a subset of those computed.
    # plotTimeVsSize(checkerName, results, densities, True, True)
    plotTimeVsSize(checkerName, results, densities, False, False)

def dumpResult(results: dict, runDetails: runDetails):
    """Write results to file."""
    resultStringDict = {
        "{}_{}".format(k[0], k[1]) : v.__dict__ for k, v in results.items()
    }
    with open('results/data{}.json'.format(getFileEndString()), 'w') as outfile:
        obj = {runDetails.checkerName : resultStringDict}
        json.dump(obj, outfile)

def getFileEndString():
    return "_{}_{}".format(NUM_TRIES, datetime.utcnow())

def main():
    graphs = { (density, size) : generateGraphs(size, density, acyclic=DO_ACYCLIC) for
        density in densities for size in sizes }
    for checker in checkers:
        evaluateForChecker(checker, graphs)

def evaluateForChecker(checker, graphs):
    evaluate = getEvaluateFunction(checker, NUM_TRIES)
    # dictionary from (density, size) to attemptInfo
    results = { (density, size) : evaluate(density, size, graphs = graphs[(density, size)]) for 
        density in densities for size in sizes }
    details = runDetails()
    details.checkerName = checker.__class__.__name__
    plot(checker.__class__.__name__, results)
    dumpResult(results, details)

def profileBatchChecker():
    """Profile the batch checker!"""
    checker = BatchChecker()
    graphs = { (density, size) : generateGraphs(size, density, acyclic=True) for
        density in densities for size in sizes }
    evaluateForChecker(checker, graphs) 

if __name__=="__main__":
    main()
    # pr = cProfile.Profile()
    # pr.enable()
    # profileBatchChecker()
    # pr.disable()
    # pr.print_stats(sort='cumtime')