from baseOnlineChecker import BaseOnlineChecker
from colorama import Fore
from testUtilities import assertActualIsSuperset, test_graph, test_s, test_t,\
    expected_solution
import time
from typing import List, Tuple

class PolynomialPathChecker(BaseOnlineChecker):
    """Path checker that returns a set for verification for online problem
    in time O(|V|.(|V|+|E|)))."""

    def __init__(self):
        super().__init__()
        self.noIdentity = True

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
            predecessorsForNode = self.getAllPredecessorsUnordered(
                sink, 
                memoize = True).intersection(predecessorSet)
            while len(predecessorsForNode) > 0:
                src = predecessorsForNode.pop()
                pathsToCheck += [(self.pathsToNewEdgeSource[src] +
                    self.pathsFromNewEdgeSink[sink],
                    self.pathsToNode[sink][src])]
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
def main():
    runAllTests()

if __name__=="__main__":
    main()