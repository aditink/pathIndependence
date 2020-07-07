import setup
from colorama import Fore
import copy
from pathCheckers.naiveChecker import NaiveChecker
from pathCheckers.pathFinding import findEdgeConflicts
from testing.testUtilities import assertEqual, assertActualIsSuperset,\
    test_graph, test_s, test_t, expected_paths_to_s, expected_paths_from_t,\
    expected_fwd_graph, expected_bkd_graph, NO_EDGE, TestDefinition,\
    defaultTestSuite
import time
from typing import List, Set, Tuple

_default_no_edge = -1

class TwoFlipPathChecker(NaiveChecker):
    """Set of paths to check using two flip tolerant search."""

    _invalid_node = -1
    _debug = False

    #### Utility functions ####
    #### Public interface ####

    def getPathsToCheck(self) ->  List[Tuple[List[int], List[int]]]:
        """Return the pairs of path whose equality implies path independence of 
        the new graph."""
        startTime = time.time()
        pathPair = findEdgeConflicts(
            self.newEdgeSource,
            self.newEdgeSink,
            self.graph
        )
        endTime = time.time()
        self.timeTaken = endTime - startTime
        return pathPair

#### Quick tests ####

def testGetPathsToCheck(testDefinition: TestDefinition):
    checker = TwoFlipPathChecker()
    checker.setGraph(testDefinition.test_graph)
    checker.setEdge(testDefinition.test_s, testDefinition.test_t)
    paths = checker.getPathsToCheck()
    assertActualIsSuperset(testDefinition.expected_solution, checker.getPathsToCheck())
    assert(checker.timeTaken > 0)

def runAllTests(testSuite: List[TestDefinition] = defaultTestSuite):
    print('\033[0m' + "Running baseOnlinePathChecker Tests")
    for testDefinition in testSuite:
        testGetPathsToCheck(testDefinition)
    print(Fore.GREEN + 'Run Completed')

#### Execute ####

def main():
    runAllTests(defaultTestSuite)

if __name__=="__main__":
    main()