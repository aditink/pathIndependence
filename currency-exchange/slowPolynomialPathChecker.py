from baseOnlineChecker import BaseOnlineChecker
from colorama import Fore
from testUtilities import assertActualIsSuperset, test_graph, test_s, test_t,\
    expected_solution
import time
from typing import List, Tuple

class PolynomialPathChecker(BaseOnlineChecker):
    """Path checker that returns a set for verification for online problem
    without memoization in time O(|V|^2.(|V|+|E|)))."""

    def __init__(self):
        super().__init__()

    def getPathsToCheck(self) ->  List[Tuple[List[int], List[int]]]:
        """Return the pairs of path whose equality implies path independence of 
        the new graph."""
        # First find set of all predecessors and successors.
        startTime = time.time()
        pathsToCheck = []
        predecessors = self.getAllPredecessors(self.newEdgeSource)
        successors = self.getAllSuccessors(self.newEdgeSink)
        predecessorSet = set(predecessors)
        # For each successor, find paths to all valid predecessors.
        for sink in successors:
            for source in predecessors:
                (isPath, path) = self.findPath(source, sink)
                if isPath:
                    pathsToCheck += [(self.pathsToNewEdgeSource[source] +
                        self.pathsFromNewEdgeSink[sink],
                        path)]
        endTime = time.time()
        self.timeTaken = endTime - startTime
        return pathsToCheck

#### Quick Tests ####

def testGetPathsToCheck():
    checker = PolynomialPathChecker()
    checker.setGraph(test_graph)
    checker.setEdge(test_s, test_t)
    assertActualIsSuperset(expected_solution, checker.getPathsToCheck())
    assert(checker.timeTaken > 0)

def runAllTests():
    print('\033[0m' + "Running optimalSetPathChecker Tests")
    testGetPathsToCheck()
    print(Fore.GREEN + 'Run Completed')    

#### Execute ####

runAllTests()