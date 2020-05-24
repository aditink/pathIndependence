from colorama import Fore
from nonIdentityUtilities import NonIdentityPathChecker
from optimalSetPathChecker import OptimalSetPathChecker
from testUtilities import assertActualIsSuperset, test_graph, test_s, test_t,\
    expected_solution_no_identity
import time
from typing import List, Tuple

class NoIdentityOptimalSetPathChecker(OptimalSetPathChecker, NonIdentityPathChecker):

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

def testGetPathsToCheck():
    checker = NoIdentityOptimalSetPathChecker()
    checker.setGraph(test_graph)
    checker.setEdge(test_s, test_t)
    assertActualIsSuperset(expected_solution_no_identity,\
        checker.getPathsToCheck())
    assert(checker.timeTaken > 0)

def runAllTests():
    print('\033[0m' + "Running NoIdentityOptimalSetPathChecker Tests")
    testGetPathsToCheck()
    print(Fore.GREEN + 'Run Completed')

def main():
    runAllTests()

if __name__=="__main__":
    main()