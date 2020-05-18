from nonIdentityUtilities import NonIdentityPathChecker
from optimalSetPathChecker import OptimalSetPathChecker

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
        pathPairs += self.getSourceCycles + self.getSinkCycles
        endTime = time.time()
        self.timeTaken = endTime - startTime
        return pathPairs