"""Interface for path checkers"""
class IPathChecker:

    def setGraph(self, graph: List[List[int]]) -> None:
       """Set the graph to which an edge is to be added"""
       pass
    
    def setEdge(self, source: int, sink: int) -> None:
        """Set the edge that is to be added"""
        pass

    def getPathsToCheck(self) -> List[int][int]:
        """Return the pairs of path whose equality implies path independence of the new graph"""
        pass

    def getComputeTime(self) -> int:
        """Return time required to compute latest path check"""
        pass