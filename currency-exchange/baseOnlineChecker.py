from iPathChecker import IPathChecker

class BaseOnlineChecker(IPathChecker):
    """Implements base functionality common to all PathCheckers."""

    _invalid_node = -1
    _default_no_edge = -1

    #### Utility functions ####

    def getForwardEdges(self, source: int) -> List[int]:
        return [i for i in range(len(self.graph)) \
            if self.graph[source][i] != self._no_edge and i != source]

    def getBackwardEdges(self, sink: int) -> List[int]:
        return [i for i in range(len(self.graph)) \
            if self.graph[i][sink] != self._no_edge and i != sink]

    #### Public interface ####

    def __init__(self):
        self.graph = [[]]
        self.newEdgeSource = _invalid_node
        self.newEdgeSink = _invalid_node
        self.timeTaken = 0
        self.numberOfNodes = 0
        self._no_edge = _default_no_edge
    
    def setGraph(
        self,
        graph: List[List[int]],
        noEdge = _default_no_edge) -> None:
        """Set the graph to which an edge is to be added."""
        self.graph = graph
        self.numberOfNodes = len(graph)
        self._no_edge = noEdge
    
    def setEdge(self, source: int, sink: int) -> None:
        """Set the edge that is to be added."""
        self.newEdgeSource = source
        self.newEdgeSink = sink

    def getPathsToCheck(self) -> List[int][int]:
        """Return the pairs of path whose equality implies path independence of 
        the new graph."""
        pass

    def getComputeTime(self) -> int:
        """Return time required to compute latest path check."""
        return self.timeTaken