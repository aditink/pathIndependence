from pathCheckers.baseOnlineChecker import BaseOnlineChecker
from colorama import Fore
from testing.testUtilities import test_graph, test_s, test_t,\
    expected_solution_no_identity, TestDefinition, defaultTestSuite, assertEqual
from typing import List, Tuple

class NonIdentityPathChecker(BaseOnlineChecker):

    def __init__(self):
        super().__init__()
        self.noIdentity = True

    def handleCycle(self, terminalNode: int) -> List[Tuple[List[int], List[int]]]:
        pathsToCheck = []
        cycle = self.pathsToNewEdgeSource[terminalNode] +\
            self.pathsFromNewEdgeSink[terminalNode] 
        pathsToCheck +=[(cycle, cycle + cycle[1:])]
        return pathsToCheck
    
    def getSinkCycles(self) -> List[Tuple[List[int], List[int]]]:
        (cycleExists, cycle) = self.findCycle(self.newEdgeSink)
        if cycleExists:
            return [([self.newEdgeSource, self.newEdgeSink], [self.newEdgeSource] + cycle)]
        return []
    
    def getSourceCycles(self) -> List[Tuple[List[int], List[int]]]:
        (cycleExists, cycle) = self.findCycle(
            self.newEdgeSource)
        if cycleExists:
            return [([self.newEdgeSource, self.newEdgeSink], cycle+[self.newEdgeSink])]
        return []
    
    def findCycle(self, source: int) -> Tuple[bool, List[int]]:
        """Find cycle."""
        # DFS.
        path = []
        visited = set()
        stack = [source]
        firstRun = True
        while (len(stack)>0):
            currentNode = stack.pop()
            if currentNode == self._invalid_node:
                path.pop()
            elif currentNode not in visited:
                path = path+[currentNode]
                if not firstRun:
                    if currentNode == source:
                        return (True, path)
                    visited.add(currentNode)
                else:
                    firstRun = False
                stack += [self._invalid_node] + self.compactFwdGraph[currentNode]
        return (False, [])

#### Quick Tests ####

def testGetSourceCycles(testDefintion: TestDefinition):
    checker = NonIdentityPathChecker()
    checker.setGraph(testDefintion.test_graph)
    checker.setEdge(testDefintion.test_s, testDefintion.test_t)
    assertEqual(testDefintion.expected_source_cycles,\
        checker.getSourceCycles())

def testGetSinkCycles(testDefintion: TestDefinition):
    checker = NonIdentityPathChecker()
    checker.setGraph(testDefintion.test_graph)
    checker.setEdge(testDefintion.test_s, testDefintion.test_t)
    assertEqual(testDefintion.expected_sink_cycles,\
        checker.getSinkCycles())

def runAllTests(testSuite: List[TestDefinition]):
    print('\033[0m' + "Running NoIdentityPolynomialPathChecker Tests")
    for testDefinition in testSuite:
        testGetSourceCycles(testDefinition)
        testGetSinkCycles(testDefinition)
    print(Fore.GREEN + 'Run Completed')    

#### Execute ####
def main():
    runAllTests(defaultTestSuite)

if __name__=="__main__":
    main()