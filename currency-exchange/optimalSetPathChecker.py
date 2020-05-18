from baseOnlineChecker import BaseOnlineChecker
from colorama import Fore
import copy
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
        self.dependencyNodeMap = []
        self.pathsToNewEdgeSource = dict()
        self.pathsFromNewEdgeSink = dict()

    def getAllPredecessors(self, node) -> List[int]:
        """Returns a list of nodes that are predecessors of this one.
        Memoize if source of new edge."""
        visited = set()
        # To store visitedNodes in an ordered closest to new edge first.
        visitedList = []
        currentNode = node
        stack = [currentNode]
        path = []
        while (len(stack) > 0):
            currentNode = stack.pop()
            if currentNode == self._invalid_node:
                path = path[1:]
            elif currentNode not in visited:
                visited.add(currentNode)
                visitedList += [currentNode]
                path = [currentNode] + path
                if (node == self.newEdgeSource):
                    self.pathsToNewEdgeSource[currentNode] = copy.deepcopy(path)
                stack += [self._invalid_node] + self.compactBkdGraph[currentNode]
        if __debug__ and self._debug:
            print("getAllPredecessors: node: {} and visitedList: {}".format(
                node, visitedList))
        return visitedList

    def getAllSuccessors(self, node) -> List[int]:
        """Returns a list of nodes that are successors of this one.
        Memoize if sink of new edge."""
        visited = set()
        # maintain a separate list to get ordering where closest node is first.
        visitedList = []
        currentNode = node
        stack = [node]
        path = []
        # More or less DFS.
        while (len(stack) > 0):
            currentNode = stack.pop()
            if currentNode == self._invalid_node:
                path.pop()
            elif currentNode not in visited:
                visited.add(currentNode)
                visitedList += [currentNode]
                path += [currentNode]
                if (node == self.newEdgeSink):
                    self.pathsFromNewEdgeSink[currentNode] = copy.deepcopy(path)
                stack += [self._invalid_node] + self.compactFwdGraph[currentNode]
        if __debug__ and self._debug:
            print("getAllSuccessors: node = {} and visited list: {}".format(
                node, visitedList))
        return visitedList

    def findPath(self, source: int, sink: int) -> Tuple[bool, List[int]]:
        """Find path from source ot sink in old graph,
        without involving new edge."""
        # DFS.
        path = []
        visited = set()
        stack = [source]
        while (len(stack)>0):
            currentNode = stack.pop()
            if currentNode == self._invalid_node:
                path.pop()
            elif currentNode not in visited:
                path = path+[currentNode]
                if currentNode == sink:
                    return (True, path)
                visited.add(currentNode)
                stack += [self._invalid_node] + self.compactFwdGraph[currentNode]
        return (False, [])

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
        
    def findPair(self, source: int, sink: int) -> Tuple[List[int], List[int]]:
        """Finds a pair of paths from the given source to sink, the first 
        includes the new edge, and the second one doesn't.
        In case of a cycle the second path is just the single node,
        representing the identity on the node."""
        if not bool(self.pathsFromNewEdgeSink):
            self.getAllSuccessors(self.newEdgeSink)
        if not bool(self.pathsToNewEdgeSource):
            self.getAllPredecessors(self.newEdgeSource)
        firstSegment = self.pathsToNewEdgeSource[source]
        lastSegment = self.pathsFromNewEdgeSink[sink]
        (_, secondPath) = self.findPath(source, sink)
        return(firstSegment+lastSegment, secondPath)

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

NO_EDGE = -1

test_graph = [
    [NO_EDGE,       1, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE],
    [NO_EDGE, NO_EDGE,       1, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE],
    [NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE],
    [NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE,       1, NO_EDGE,       1, NO_EDGE],
    [NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE,       1, NO_EDGE, NO_EDGE],
    [NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE],
    [NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE,       1],
    [NO_EDGE, NO_EDGE,       1, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE]]
test_s = 2
test_t = 3
test_new_edge = (2, 3)
expected_fwd_graph = [
    [1],
    [2],
    [],
    [4, 6],
    [5],
    [],
    [7],
    [2]
]
expected_bkd_graph = [
    [],
    [0],
    [1, 7],
    [],
    [3],
    [4],
    [3],
    [6]
]

expected_paths_to_s = {
    0 : [0, 1, 2],
    1 : [1, 2],
    2 : [2],
    3 : [3, 6, 7, 2],
    6 : [6, 7, 2],
    7 : [7, 2]
}

expected_paths_from_t = {
    2 : [3, 6, 7, 2],
    3 : [3],
    4 : [3, 4],
    5 : [3, 4, 5],
    6 : [3, 6],
    7 : [3, 6, 7]
}

expected_solution = [
    ([2, 3, 6, 7, 2], [2]),
    ([3, 6, 7, 2, 3], [3]),
    ([6, 7, 2, 3, 6], [6]),
    ([7, 2, 3, 6, 7], [7])
]

# This method is from stack overflow.
def compareLists(expected, actual):
    actual = list(actual)   # make a mutable copy
    try:
        for elem in expected:
            actual.remove(elem)
    except ValueError:
        return False
    return not actual

def assertEqual(expected, actual):
    try:
        if isinstance(expected, list):
            assert(compareLists(expected, actual))
        else:
            assert(expected == actual)
    except:
        print(Fore.RED + "Error")
        print("Expected: {}".format(expected))
        print("Actual: {}".format(actual))
        traceback.print_stack()

def testGetAllPredecessors():
    checker = OptimalSetPathChecker()
    checker.setGraph(test_graph)
    checker.setEdge(test_s, test_t)
    checker.getAllPredecessors(test_s)
    assertEqual(expected_paths_to_s, checker.pathsToNewEdgeSource)

def testGetAllSuccessors():
    checker = OptimalSetPathChecker()
    checker.setGraph(test_graph)
    checker.setEdge(test_s, test_t)
    checker.getAllSuccessors(test_t)
    assertEqual(expected_paths_from_t, checker.pathsFromNewEdgeSink)

def testFindPath():
    checker = OptimalSetPathChecker()
    checker.setGraph(test_graph)
    assertEqual((False, []), checker.findPath(0, 3))
    assertEqual((True, [3, 6, 7, 2]), checker.findPath(3, 2))

def testGetSuccessors():
    checker = OptimalSetPathChecker()
    checker.setGraph(test_graph)
    assertEqual({(0, 4), (1, 4), (0, 5), (1, 5)}, checker.getSuccessors(1, 4))

def testGetRootPairs():
    checker = OptimalSetPathChecker()
    checker.setGraph(test_graph)
    checker.setEdge(test_s, test_t)
    assertEqual({(2, 2), (3, 3), (6, 6), (7, 7)}, checker.getRootPairs())

def testFindPair():
    checker = OptimalSetPathChecker()
    test_graph[1][4] = 1
    checker.setGraph(test_graph)
    checker.setEdge(test_s, test_t)
    assertEqual(([3, 6, 7, 2, 3], [3]), checker.findPair(3, 3))
    assertEqual(([1, 2, 3, 4], [1, 4]), checker.findPair(1, 4))
    test_graph[1][4] = NO_EDGE
    
def testGetPathsToCheck():
    checker = OptimalSetPathChecker()
    checker.setGraph(test_graph)
    checker.setEdge(test_s, test_t)
    assertEqual(expected_solution, checker.getPathsToCheck())
    assert(checker.timeTaken > 0)

def runAllTests():
    print("Running optimalSetPathChecker Tests")
    testGetAllPredecessors()
    testGetAllSuccessors()
    testFindPath()
    testGetSuccessors()
    testGetRootPairs()
    testFindPair()
    testGetPathsToCheck()
    print(Fore.GREEN + 'Run Completed')    

#### Execute ####

runAllTests()