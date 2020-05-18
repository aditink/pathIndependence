from colorama import Fore
from iPathChecker import IPathChecker
from typing import List
from typing import Tuple

_default_no_edge = -1

class BaseOnlineChecker(IPathChecker):
    """Implements base functionality common to all PathCheckers."""

    _invalid_node = -1
    _debug = False

    #### Utility functions ####

    def getForwardEdges(self, source: int) -> List[int]:
        return [i for i in range(len(self.graph)) \
            if self.graph[source][i] != self._no_edge and i != source]

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

    #### Public interface ####

    def __init__(self):
        self.graph = [[]]
        self.newEdgeSource = self._invalid_node
        self.newEdgeSink = self._invalid_node
        self.timeTaken = 0
        self.compactFwdGraph = []
        self.compactBkdGraph = []
        self._no_edge = -1
    
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

#### Quick tests ####

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


def testBuildCompactBkdGraph():
    checker = BaseOnlineChecker()
    checker.graph = test_graph
    checker.buildCompactBkdGraph()
    assert(checker.graph == test_graph)
    if __debug__ and checker._debug:
        # Assumption: lists ordered from smallest to largest element.
        print("expected: {}".format(str(expected_bkd_graph)))
        print("got: {}".format(str(checker.compactBkdGraph)))
    assert(str(checker.compactBkdGraph) == str(expected_bkd_graph))

def testBuildCompactFwdGraph():
    checker = BaseOnlineChecker()
    checker.graph = test_graph
    checker.buildCompactFwdGraph()
    assert(checker.graph == test_graph)
    # Assumption: lists ordered from smallest to largest element.
    assert(str(checker.compactFwdGraph) == str(expected_fwd_graph))

def testSetGraph():
    checker = BaseOnlineChecker()
    checker.setGraph(test_graph)
    assert(checker.graph == test_graph)
    # Assumption: lists ordered from smallest to largest element.
    assert(str(checker.compactFwdGraph) == str(expected_fwd_graph))
    assert(str(checker.compactBkdGraph) == str(expected_bkd_graph))
    
def testSetEdge():
    checker = BaseOnlineChecker()
    checker.setEdge(0, 1)
    assert(checker.newEdgeSource == 0)
    assert(checker.newEdgeSink == 1)

def testComputeTime():
    checker = BaseOnlineChecker()
    checker.timeTaken = 123
    assert(checker.getComputeTime() == 123)

def runAllTests():
    print("Running baseOnlinePathChecker Tests")
    testBuildCompactBkdGraph()
    testBuildCompactFwdGraph()
    testSetGraph()
    testSetEdge()
    testComputeTime()
    print(Fore.GREEN + 'OK')

#### Execute ####

# runAllTests()