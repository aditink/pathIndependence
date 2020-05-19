from baseOnlineChecker import BaseOnlineChecker
from typing import List, Tuple

class NonIdentityPathChecker(BaseOnlineChecker):

    def handleCycle(self, terminalNode: int) -> List[Tuple[List[int], List[int]]]:
        pathsToCheck = []
        cycle = self.pathsToNewEdgeSource[terminalNode] +\
            self.pathsFromNewEdgeSink[terminalNode] 
        pathsToCheck +=[(cycle, cycle + cycle[1:])]
        for cycleExit in self.getForwardEdges(terminalNode):
            pathsToCheck += [(cycle, cycle + [cycleExit])]
        for cycleEntry in self.getBackwardEdges(terminalNode):
            pathsToCheck += [(cycle, [cycleEntry] + cycle)]
        return pathsToCheck
    
    def getSinkCycles(self) -> List[Tuple[List[int], List[int]]]:
        (cycleExists, cycle) = self.findPath(self.newEdgeSink, self.newEdgeSink)
        if cycleExists:
            return [(cycle, [self.newEdgeSource] + cycle)]
        return []
    
    def getSourceCycles(self) -> List[Tuple[List[int], List[int]]]:
        (cycleExists, cycle) = self.findPath(
            self.newEdgeSource, self.newEdgeSource)
        if cycleExists:
            return [(cycle, cycle+[self.newEdgeSink])]
        return []