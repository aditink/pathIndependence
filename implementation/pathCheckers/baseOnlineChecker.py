import setup
from colorama import Fore
import copy
from pathCheckers.iPathChecker import IPathChecker
from testing.testUtilities import assertEqual, test_graph, test_s, test_t,\
    expected_paths_to_s, expected_paths_from_t, expected_fwd_graph,\
        expected_bkd_graph, NO_EDGE, TestDefinition, defaultTestSuite
from typing import List, Set, Tuple

_default_no_edge = -1

class BaseOnlineChecker(IPathChecker):
    """Implements base functionality common to all PathCheckers."""

    _invalid_node = -1
    _debug = False

    #### Utility functions ####

    def getForwardEdges(self, source: int) -> List[int]:
        return [i for i in range(len(self.graph)) \
            if self.graph[source][i] != self._no_edge]

    def getBackwardEdges(self, sink: int) -> List[int]:
        return [i for i in range(len(self.graph)) \
            if self.graph[i][sink] != self._no_edge and i != sink]

    def getEmptyPathList(self):
        paths = []
        for _ in range(len(self.graph)):
            paths += [[]]
        return paths

    def buildCompactFwdGraph(self):
        self.compactFwdGraph = self.getEmptyPathList()
        for node in range(len(self.graph)):
            self.compactFwdGraph[node] = self.getForwardEdges(node)
    
    def buildCompactBkdGraph(self):
        self.compactBkdGraph = self.getEmptyPathList()
        for node in range(len(self.graph)):
            self.compactBkdGraph[node] = self.getBackwardEdges(node)
    
    def getAllPredecessors(self, node, memoize = False) -> List[int]:
        """Returns a list of nodes that are predecessors of this one.
        Memoize if source of new edge."""
        if not self.compactBkdGraph:
            self.buildCompactBkdGraph()
        memoize = memoize or node == self.newEdgeSource
        if memoize:
            pathDict = dict()
        visited = set()
        # To store visitedNodes ordered closest to new edge first.
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
                if (memoize):
                    pathDict[currentNode] = copy.deepcopy(path)
                stack += [self._invalid_node] + self.compactBkdGraph[currentNode]
        if __debug__ and self._debug:
            print("getAllPredecessors: node: {} and visitedList: {}".format(
                node, visitedList))
        if node == self.newEdgeSource:
            self.pathsToNewEdgeSource = pathDict
        if memoize:
            self.pathsToNode[node] = pathDict
        return visitedList
    
    def getAllPredecessorsUnordered(self, node, memoize = True) -> Set[int]:
        """Returns a list of nodes that are predecessors of this one.
        Memoize if source of new edge."""
        memoize = memoize or node == self.newEdgeSource
        if memoize:
            pathDict = dict()
        visited = set()
        currentNode = node
        stack = [currentNode]
        path = []
        while (len(stack) > 0):
            currentNode = stack.pop()
            if currentNode == self._invalid_node:
                path = path[1:]
            elif currentNode not in visited:
                visited.add(currentNode)
                path = [currentNode] + path
                if (memoize):
                    pathDict[currentNode] = copy.deepcopy(path)
                stack += [self._invalid_node] + self.compactBkdGraph[currentNode]
        if __debug__ and self._debug:
            print("getAllPredecessors: node: {} and visitedList: {}".format(
                node, visited))
        if node == self.newEdgeSource:
            self.pathsToNewEdgeSource = pathDict
        if memoize:
            self.pathsToNode[node] = pathDict
        return visited

    def getAllSuccessors(self, node) -> List[int]:
        """Returns a list of nodes that are successors of this one.
        Memoize if sink of new edge."""
        if not self.compactFwdGraph:
            self.buildCompactFwdGraph()
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
    
    def getTree(self, node: int):
        """Similar to get all successors, but returns a spanning tree in 
        the form of a set of edges."""
        # if not self.compactFwdGraph:
        #     self.buildCompactFwdGraph()
        self.buildCompactFwdGraph()
        visited = set()
        # maintain a separate list to get ordering where closest node is first.
        visitedList = []
        treeEdges = set()
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
                stack += [self._invalid_node] + self.compactFwdGraph[currentNode]
                if (len(path) > 1):
                    treeEdges.add((path[-2], currentNode))
        if __debug__ and self._debug:
            print("getAllSuccessors: node = {} and visited list: {}".format(
                node, visitedList))
        return treeEdges

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
        # Special case of Identity.
        if source == sink:
            secondPath = self.identityFunction(source)    
        return(firstSegment + lastSegment, secondPath)

    #### Public interface ####

    def __init__(self):
        self.graph = [[]]
        self.identityFunction = lambda source : [source]
        self.newEdgeSource = self._invalid_node
        self.newEdgeSink = self._invalid_node
        self.timeTaken = 0
        self.compactFwdGraph = []
        self.compactBkdGraph = []
        self.pathsToNewEdgeSource = dict()
        self.pathsFromNewEdgeSink = dict()
        # sink node -> {source node -> path}
        self.pathsToNode = dict()
        self._no_edge = _default_no_edge
        self.noIdentity = False
        # Hack to make sub classes work
        self._invalid_node = -1
    
    def setGraph(
        self,
        graph: List[List[int]],
        noEdge: int = _default_no_edge) -> None:
        """Set the graph to which an edge is to be added."""
        self.graph = graph
        self._no_edge = noEdge
        self.buildCompactBkdGraph()
        self.buildCompactFwdGraph()
    
    def setEdge(self, source: int, sink: int) -> None:
        """Set the edge that is to be added."""
        self.newEdgeSource = source
        self.newEdgeSink = sink

    def getPathsToCheck(self) ->  List[Tuple[List[int], List[int]]]:
        """Return the pairs of path whose equality implies path independence of 
        the new graph."""
        pass

    def getComputeTime(self) -> int:
        """Return time required to compute latest path check."""
        return self.timeTaken
    
    def setIdFunction(self, idFunction):
        """Store the special representation of identity function."""
        self.identityFunction = idFunction
        

#### Quick tests ####

def testBuildCompactBkdGraph(testDefinition: TestDefinition):
    checker = BaseOnlineChecker()
    checker.graph = testDefinition.test_graph
    checker.buildCompactBkdGraph()
    assertEqual(testDefinition.test_graph, checker.graph)
    if __debug__ and checker._debug:
        # Assumption: lists ordered from smallest to largest element.
        print("expected: {}".format(str(expected_bkd_graph)))
        print("got: {}".format(str(checker.compactBkdGraph)))
    assertEqual(testDefinition.expected_bkd_graph, checker.compactBkdGraph)

def testBuildCompactFwdGraph(testDefinition: TestDefinition):
    checker = BaseOnlineChecker()
    checker.graph = testDefinition.test_graph
    checker.buildCompactFwdGraph()
    assert(checker.graph == testDefinition.test_graph)
    assertEqual(testDefinition.expected_fwd_graph, checker.compactFwdGraph)

def testSetGraph(testDefinition: TestDefinition):
    checker = BaseOnlineChecker()
    checker.setGraph(testDefinition.test_graph)
    assertEqual(checker.graph, testDefinition.test_graph)
    # Assumption: lists ordered from smallest to largest element.
    assertEqual(testDefinition.expected_fwd_graph, checker.compactFwdGraph)
    assertEqual(testDefinition.expected_bkd_graph, checker.compactBkdGraph)
    
def testSetEdge(testDefinition: TestDefinition):
    checker = BaseOnlineChecker()
    checker.setEdge(testDefinition.test_s, testDefinition.test_t)
    assertEqual(testDefinition.test_s, checker.newEdgeSource)
    assertEqual(testDefinition.test_t, checker.newEdgeSink)

def testGetAllPredecessors(testDefinition: TestDefinition):
    checker = BaseOnlineChecker()
    checker.setGraph(testDefinition.test_graph)
    checker.setEdge(testDefinition.test_s, testDefinition.test_t)
    checker.getAllPredecessors(testDefinition.test_s)
    assertEqual(testDefinition.expected_paths_to_s, checker.pathsToNewEdgeSource)

def testGetAllPredecessorsUnordered():
    checker = BaseOnlineChecker()
    checker.setGraph(test_graph)
    checker.setEdge(test_s, test_t)
    assertEqual({0, 1, 2, 3, 6, 7}, checker.getAllPredecessorsUnordered(test_s))
    assertEqual(expected_paths_to_s, checker.pathsToNewEdgeSource)
    assertEqual(expected_paths_to_s, checker.pathsToNode[test_s])

def testGetAllSuccessors():
    checker = BaseOnlineChecker()
    checker.setGraph(test_graph)
    checker.setEdge(test_s, test_t)
    checker.getAllSuccessors(test_t)
    assertEqual(expected_paths_from_t, checker.pathsFromNewEdgeSink)

def testFindPath():
    checker = BaseOnlineChecker()
    checker.setGraph(test_graph)
    assertEqual((False, []), checker.findPath(0, 3))
    assertEqual((True, [3, 6, 7, 2]), checker.findPath(3, 2))

def testFindPair():
    checker = BaseOnlineChecker()
    test_graph[1][4] = 1
    checker.setGraph(test_graph)
    checker.setEdge(test_s, test_t)
    assertEqual(([3, 6, 7, 2, 3], [3]), checker.findPair(3, 3))
    assertEqual(([1, 2, 3, 4], [1, 4]), checker.findPair(1, 4))
    test_graph[1][4] = NO_EDGE

def testComputeTime():
    checker = BaseOnlineChecker()
    checker.timeTaken = 123
    assert(checker.getComputeTime() == 123)

def runAllTests(testSuite: List[TestDefinition] = defaultTestSuite):
    print('\033[0m' + "Running baseOnlinePathChecker Tests")
    testGetAllPredecessorsUnordered()
    testGetAllSuccessors()
    testFindPath()
    testFindPair()
    testComputeTime()
    for testDefinition in testSuite:
        testSetGraph(testDefinition)
        testBuildCompactBkdGraph(testDefinition)
        testBuildCompactFwdGraph(testDefinition)
        testGetAllPredecessors(testDefinition)
        testSetEdge(testDefinition)
    print(Fore.GREEN + 'Run Completed')

#### Execute ####

def main():
    runAllTests(defaultTestSuite)

if __name__=="__main__":
    main()