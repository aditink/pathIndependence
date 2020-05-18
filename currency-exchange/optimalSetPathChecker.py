from baseOnlineChecker import BaseOnlineChecker
from colorama import Fore
import copy
from testUtilities import assertEqual, test_graph, test_s, test_t,\
    expected_solution
import time
import traceback
from typing import List
from typing import Set
from typing import Tuple

class OptimalSetPathChecker(BaseOnlineChecker):
    """Path checker that returns minimal set for verification 
    for online problem."""

    def __init__(self):
        super().__init__()

    def getSuccessors(self, source: int, sink: int) -> Set[int]:
        """Returns a set of pairs such that verifying a path between given
        source and sink implies also that all the pairs in the returned set are
        equal."""
        predecessors = self.getAllPredecessors(source)
        successors = self.getAllSuccessors(sink)
        return {(src, snk) for src in predecessors for snk in successors}

    def getRootPairs(self) -> List[List[int]]:
        """Returns a graph where each node represents a (source, sink) pair in
        self.graph. 
        Map from (source, sink) to node number in self.dependencyNodeMap.
        Node A succeeds node B if checking a pair of B implies that 
        the paths pairs of A must also be equal."""
        acceptedPairs = set()
        # Get set of all predecessors, successors.
        predecessors = self.getAllPredecessors(self.newEdgeSource)
        successors = self.getAllSuccessors(self.newEdgeSink)
        # Go through each element in predecessors X successors.
        # For efficiency, closest pairs to new edge should appear first.
        potentialPairs = {(source, sink) for source in predecessors \
            for sink in successors}
        orderedPotentialPairs = [(source, sink) for source in predecessors \
            for sink in successors]
        while (len(potentialPairs) != 0):
            # using ordering is a heuristic to (hopefully) improve performance,
            # so parent is usually checked before child.
            (source, sink) = orderedPotentialPairs.pop(0)
            if (source, sink) in potentialPairs:
                potentialPairs.remove((source, sink))
                (pathExists, path) = self.findPath(source, sink)
                if pathExists:
                    currentPairSuccessors = self.getSuccessors(source, sink)
                    for redundantPair in acceptedPairs.intersection(
                        currentPairSuccessors):
                        acceptedPairs.remove(redundantPair)
                    for redundantPair in potentialPairs.intersection(
                        currentPairSuccessors):
                        potentialPairs.remove(redundantPair)
                    acceptedPairs.add((source, sink))
        return acceptedPairs        

    def getPathsToCheck(self) ->  List[Tuple[List[int], List[int]]]:
        """Return the pairs of path whose equality implies path independence of 
        the new graph."""
        startTime = time.time()
        subset = self.getRootPairs()
        # Find paths for each pair in the subset
        pathPairs = []
        for node in subset:
            (source, sink) = node
            pathPairs += [self.findPair(source, sink)]
        endTime = time.time()
        self.timeTaken = endTime - startTime
        return pathPairs

#### Quick Tests ####

def testGetSuccessors():
    checker = OptimalSetPathChecker()
    checker.setGraph(test_graph)
    assertEqual({(0, 4), (1, 4), (0, 5), (1, 5)}, checker.getSuccessors(1, 4))

def testGetRootPairs():
    checker = OptimalSetPathChecker()
    checker.setGraph(test_graph)
    checker.setEdge(test_s, test_t)
    assertEqual({(2, 2), (3, 3), (6, 6), (7, 7)}, checker.getRootPairs())
    
def testGetPathsToCheck():
    checker = OptimalSetPathChecker()
    checker.setGraph(test_graph)
    checker.setEdge(test_s, test_t)
    assertEqual(expected_solution, checker.getPathsToCheck())
    assert(checker.timeTaken > 0)

def runAllTests():
    print('\033[0m' + "Running optimalSetPathChecker Tests")
    testGetSuccessors()
    testGetRootPairs()
    testGetPathsToCheck()
    print(Fore.GREEN + 'Run Completed')    

#### Execute ####

runAllTests()