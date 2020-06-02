from nonIdentityUtilities import NonIdentityPathChecker
from colorama import Fore
from testUtilities import assertActualIsSuperset, test_graph, test_s, test_t,\
    expected_solution_no_identity, defaultTestSuite, TestDefinition
import time
from typing import List, Tuple

class NoIdentityPolynomialPathChecker(NonIdentityPathChecker):
    """Path checker that returns a set for verification for online problem
    in time O(|V|.(|V|+|E|)))."""

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
            predecessorsForNode = self.getAllPredecessorsUnordered(
                sink, 
                memoize = True).intersection(predecessorSet)
            # Handle cycles.
            if sink in predecessorsForNode:
                predecessorsForNode.remove(sink)
                pathsToCheck += self.handleCycle(sink)
            while len(predecessorsForNode) > 0:
                src = predecessorsForNode.pop()
                pathsToCheck += [(self.pathsToNewEdgeSource[src] +
                    self.pathsFromNewEdgeSink[sink],
                    self.pathsToNode[sink][src]) if src != sink 
                        else self.identityFunction]
        pathsToCheck += self.getSinkCycles() + self.getSourceCycles()
        endTime = time.time()
        self.timeTaken = endTime - startTime
        return pathsToCheck

#### Quick Tests ####

def testGetPathsToCheck(testDefinition: TestDefinition):
    checker = NoIdentityPolynomialPathChecker()
    checker.setGraph(testDefinition.test_graph)
    checker.setEdge(testDefinition.test_s, testDefinition.test_t)
    assertActualIsSuperset(testDefinition.expected_solution_no_identity,\
        checker.getPathsToCheck())
    assert(checker.timeTaken > 0)

def runAllTests(testSuite: List[TestDefinition]):
    print('\033[0m' + "Running NoIdentityPolynomialPathChecker Tests")
    for testDefinition in testSuite:
        testGetPathsToCheck(testDefinition)
    print(Fore.GREEN + 'Run Completed')    

#### Execute ####
def main():
    runAllTests(defaultTestSuite)

if __name__=="__main__":
    main()