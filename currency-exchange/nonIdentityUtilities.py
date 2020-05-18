from baseOnlineChecker import BaseOnlineChecker
from typing import List, Tuple

class NonIdentityPathChecker(BaseOnlineChecker):

    def handleCycle(self, terminalNode: int) -> List[Tuple[int, int]]:
        pathsToCheck = []
        cycle = self.pathsToNewEdgeSource[src] + self.pathsFromNewEdgeSink[sink] 
        pathsToCheck +=[(cycle, cycle + cycle[1:])]
        for cycleExit in self.getForwardEdges(sink):
            pathsToCheck += [(cycle, cycle + cycleExit)]
        for cycleEntry in self.getBackwardEdges(sink):
            pathsToCheck += [(cycle, cycleEntry + cycle)]
        return pathsToCheck
    
    def getTerminalCycles(self, node: int) -> List[List[int]]:
        """Find all the cycles that include node (but not the new edge)."""
        pass
    
    def getSinkCycles(self) -> List[Tuple[int, int]]:
        sinkCycles = self.getTerminalCycles(self.newEdgeSink)
        sinkCyclePairs = [(cycle, [self.newEdgeSource] + cycle) 
            for cycle in sinkCycles]
        return sinkCyclePairs
    
    def getSourceCycles(self) -> List[Tuple[int, int]]:
        sourceCycles = self.getTerminalCycles(self.newEdgeSource)
        sourceCyclePairs = [(cycle, cycle+[self.newEdgeSink]) 
            for cycle in sourceCycles]