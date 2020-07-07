import setup
from colorama import Fore
import copy
from pathCheckers.iPathChecker import IPathChecker
from pathCheckers.pathFinding import findEdgeConflictsReference 
from testing.testUtilities import assertEqual, assertActualIsSuperset,\
    test_graph, test_s, test_t, expected_paths_to_s, expected_paths_from_t,\
    expected_fwd_graph, expected_bkd_graph, NO_EDGE, TestDefinition,\
    defaultTestSuite
import time
from typing import List, Set, Tuple

_default_no_edge = -1

class NaiveChecker(IPathChecker):
    """Set of paths to check using two flip tolerant search."""

    _invalid_node = -1
    _debug = False

    #### Utility functions ####
    #### Public interface ####

    def __init__(self):
        self.graph = [[]]
        self.identityFunction = lambda source : [source]
        self.newEdgeSource = self._invalid_node
        self.newEdgeSink = self._invalid_node
        self.timeTaken = 0
    
    def setGraph(
        self,
        graph: List[List[int]],
        noEdge: int = _default_no_edge) -> None:
        """Set the graph to which an edge is to be added."""
        self.graph = graph
        self._no_edge = noEdge
    
    def setEdge(self, source: int, sink: int, value=1) -> None:
        """Set the edge that is to be added."""
        self.newEdgeSource = source
        self.newEdgeSink = sink
        self.graph[source][sink] = value

    def getPathsToCheck(self) ->  List[Tuple[List[int], List[int]]]:
        """Return the pairs of path whose equality implies path independence of 
        the new graph."""
        startTime = time.time()
        pathPair = findEdgeConflictsReference(
            self.newEdgeSource,
            self.newEdgeSink,
            self.graph
        )
        endTime = time.time()
        self.timeTaken = endTime - startTime
        return pathPair

    def getComputeTime(self) -> int:
        """Return time required to compute latest path check."""
        return self.timeTaken
    
    def setIdFunction(self, idFunction):
        """Store the special representation of identity function."""
        self.identityFunction = idFunction
        

#### Quick tests ####

def testSetGraph(testDefinition: TestDefinition):
    checker = NaiveChecker()
    checker.setGraph(testDefinition.test_graph)
    assertEqual(checker.graph, testDefinition.test_graph)
    
def testSetEdge(testDefinition: TestDefinition):
    checker = NaiveChecker()
    checker.setGraph(testDefinition.test_graph)
    checker.setEdge(testDefinition.test_s, testDefinition.test_t)
    assertEqual(testDefinition.test_s, checker.newEdgeSource)
    assertEqual(testDefinition.test_t, checker.newEdgeSink)
    assertEqual(checker.graph[testDefinition.test_s][testDefinition.test_t], 1)

def testComputeTime():
    checker = NaiveChecker()
    checker.timeTaken = 123
    assert(checker.getComputeTime() == 123)

def testGetPathsToCheck(testDefinition: TestDefinition):
    checker = NaiveChecker()
    checker.setGraph(testDefinition.test_graph)
    checker.setEdge(testDefinition.test_s, testDefinition.test_t)
    paths = checker.getPathsToCheck()
    assertActualIsSuperset(testDefinition.expected_solution, checker.getPathsToCheck())
    assert(checker.timeTaken > 0)

def runAllTests(testSuite: List[TestDefinition] = defaultTestSuite):
    print('\033[0m' + "Running baseOnlinePathChecker Tests")
    testComputeTime()
    for testDefinition in testSuite:
        testGetPathsToCheck(testDefinition)
        testSetGraph(testDefinition)
        testSetEdge(testDefinition)
    print(Fore.GREEN + 'Run Completed')

#### Execute ####

def main():
    runAllTests(defaultTestSuite)

if __name__=="__main__":
    main()