from datetime import datetime
import functools
import matplotlib.pyplot as plt
import numpy as np
from pathCheckers.iPathChecker import IPathChecker
from pathCheckers.optimalSetPathChecker import OptimalSetPathChecker
from pathCheckers.polynomialPathChecker import PolynomialPathChecker
from randomGraphGenerator import generateGraph
from typing import List

NUM_TRIES = 1

densityStep = 0.1
sizeStep = 10
maxSize = 1000

densities = [i*densityStep for i in range(1, int(1.0/densityStep))] #[0.1, 0.5, 0.7, 0.8]
sizes = [i*sizeStep for i in range(1, int(maxSize/sizeStep))]

evaluationList = [(density, size) for size in sizes for density in densities]

checkers : List[IPathChecker] = [
    PolynomialPathChecker(),
    OptimalSetPathChecker()
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


def getEvaluateFunction(checker: IPathChecker, numTries: int):
    def evaluate(density, size):
        info = attemptInfo()
        for attempt in range(numTries):
            inp = generateGraph(density, size)
            checker.setGraph(inp.graph)
            checker.setEdge(inp.newEdgeSource, inp.newEdgeSink)
            paths = checker.getPathsToCheck()
            info.addSize(len(paths))
            info.addTime(checker.getComputeTime())
        return info
    return evaluate



def plot(checkerName, results):
    X, Y = np.meshgrid(densities, sizes)
    Z = [[results[(x, y)].getAvgTime() for x in densities] for y in sizes]

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.contour3D(X, Y, Z, 50, cmap='binary')
    ax.set_xlabel('Density')
    ax.set_ylabel('Size')
    ax.set_zlabel('time')

    plt.show()
    fig.savefig("results/result{}{}.png".format(checkerName, datetime.utcnow()))

# dictionary from (density, size) to attemptInfo
for checker in checkers:
    evaluate = getEvaluateFunction(checker, NUM_TRIES)
    results = { (density, size) : evaluate(density, size) for 
        density in densities for size in sizes }
    plot(checker.__class__.__name__, results)
