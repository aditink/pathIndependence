from baseOnlineChecker import BaseOnlineChecker

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
        pass

    def getAllSuccessors(self, node) -> List[int]:
        """Returns a list of nodes that are successors of this one.
        Memoize if sink of new edge."""
        pass

    def findPath(self, source: int, sink: int) -> tuple(bool, List[int]):
        """Find path from source ot sink in old graph,
        without involving new edge."""
        pass

    def getSuccessors(self, source, sink):
        """Returns a set of pairs such that checking a path between given
        source and sink implies also that all the pairs in the returned set are
        equal."""
        pass

    def getRootPairs(self) -> List[List[int]]:
        """Returns a graph where each node represents a (source, sink) pair in
        self.graph. 
        Map from (source, sink) to node number in self.dependencyNodeMap.
        Node A succeeds node B if checking a pair of B implies that 
        the paths pairs of A must also be equal.""" 
        acceptedPairs = set()
        # Get set of all predecessors, successors.
        predecessors = getAllPredecessors(self.newEdgeSource)
        successors = getAllSuccessors(self.newEdgeSink)
        # Go through each element in predecessors X successors.
        # For efficiency, closest pairs to new edge should appear first.
        potentialPairs = {(source, sink) for source in predecessors \
            for sink in successors}
        while (len(potentialPairs) != 0):
            (source, sink) = potentialPairs.pop()
            (pathExists, path) = findPath(self, source, sink)
            if pathExists:
                currentPairSuccessors = getSuccessors(source, sink)
                acceptedPairs.add((source, sink))
                for redundantPair in acceptedPairs.intersection(
                    currentPairSuccessors):
                    acceptedPairs.remove(redundantPair)
                for redundantPair in potentialPairs.intersection(
                    currentPairSuccessors):
                    potentialPairs.remove(redundantPair)
        return acceptedPairs        
        
    def findPair(self, source, sink):
        """Finds a pair of paths from the given source to sink, the first 
        includes the new edge, and the second one doesn't.
        In case of a cycle the second path is empty,
        representing the identity."""
        pass

    def getPathsToCheck(self) -> List[int][int]:
        """Return the pairs of path whose equality implies path independence of 
        the new graph."""
        subset = getRootPairs(self)
        # Find paths for each pair in the subset
        pathPairs = []
        for node in subset:
            (source, sink) = dependencyNodeMap[node]
            pathPairs += [findPairs(self, source, sink)]
        return pathPairs

