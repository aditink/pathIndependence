from baseOnlineChecker import BaseOnlineChecker
from typing import List, Tuple

class NonIdentityPathChecker(BaseOnlineChecker):

    def handleCycle(self, terminalNode: int) -> List[Tuple[int, int]]:
        pathsToCheck = []
        cycle = self.pathsToNewEdgeSource[terminalNode] +\
            self.pathsFromNewEdgeSink[terminalNode] 
        pathsToCheck +=[(cycle, cycle + cycle[1:])]
        for cycleExit in self.getForwardEdges(terminalNode):
            pathsToCheck += [(cycle, cycle + [cycleExit])]
        for cycleEntry in self.getBackwardEdges(terminalNode):
            pathsToCheck += [(cycle, [cycleEntry] + cycle)]
        return pathsToCheck
    
    def getTerminalCycles(self, node: int) -> List[List[int]]:
        """Find all the cycles that include node (but not the new edge)."""
        # Modified DFS.
        path = []
        blocked = set()
        cycles = []
        stack = [node]
        while (len(stack)>0):
            currentNode = stack.pop()
            if currentNode == self._invalid_node:
                blocked.add(path.pop())
            elif currentNode not in blocked and currentNode not in path:
                path = path+[currentNode]
                if currentNode == node and len(path)>1:
                    cycles += [path]
                stack += [self._invalid_node] + self.compactFwdGraph[currentNode]
        return cycles
    
    def getSinkCycles(self) -> List[Tuple[int, int]]:
        sinkCycles = self.getTerminalCycles(self.newEdgeSink)
        sinkCyclePairs = [(cycle, [self.newEdgeSource] + cycle) 
            for cycle in sinkCycles]
        return sinkCyclePairs
    
    def getSourceCycles(self) -> List[Tuple[int, int]]:
        sourceCycles = self.getTerminalCycles(self.newEdgeSource)
        sourceCyclePairs = [(cycle, cycle+[self.newEdgeSink]) 
            for cycle in sourceCycles]
        return sourceCyclePairs