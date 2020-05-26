from colorama import Fore
from nonIdentityUtilities import NonIdentityPathChecker
from optimalSetPathChecker import OptimalSetPathChecker
from testUtilities import assertActualIsSuperset, test_graph, test_s, test_t,\
    expected_solution_no_identity, TestDefinition, defaultTestSuite, assertEqual
import time
from typing import List, Tuple

class NoIdentityOptimalSetPathChecker(OptimalSetPathChecker, NonIdentityPathChecker):

    def __init__(self):
        super().__init__()
        self.noIdentity = True

    def getPathsToCheck(self) ->  List[Tuple[List[int], List[int]]]:
        """Return the pairs of path whose equality implies path independence of 
        the new graph."""
        startTime = time.time()
        subset = self.getRootPairs()
        # Find paths for each pair in the subset
        pathPairs = []
        for node in subset:
            (source, sink) = node
            if (source == sink):
                pathPairs += self.handleCycle(source)
            else:
                pathPairs += [self.findPair(source, sink)]
        pathPairs += self.getSourceCycles() + self.getSinkCycles()
        endTime = time.time()
        self.timeTaken = endTime - startTime
        return pathPairs

def testGetPathsToCheck(testDefinition: TestDefinition):
    checker = NoIdentityOptimalSetPathChecker()
    checker.setGraph(testDefinition.test_graph)
    checker.setEdge(testDefinition.test_s, testDefinition.test_t)
    assertEqual(testDefinition.expected_solution_no_identity,\
        checker.getPathsToCheck())
    assert(checker.timeTaken > 0)

def runAllTests(testSuite: List[TestDefinition]):
    print('\033[0m' + "Running NoIdentityOptimalSetPathChecker Tests")
    for testDefinition in testSuite:
        testGetPathsToCheck(testDefinition)
    print(Fore.GREEN + 'Run Completed')

def main():
    runAllTests(defaultTestSuite)

if __name__=="__main__":
    main()