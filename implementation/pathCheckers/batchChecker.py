import setup
from colorama import Fore
import copy
from pathCheckers.naiveChecker import NaiveChecker
from pathCheckers.baseOnlineChecker import BaseOnlineChecker
from pathCheckers.batchTestCommonUtilities import addVectors
from pathCheckers.pathFinding import findEdgeConflicts
from testing.testUtilities import assertEqual, assertActualIsSuperset,\
    test_graph, test_s, test_t, expected_paths_to_s, expected_paths_from_t,\
    expected_fwd_graph, expected_bkd_graph, NO_EDGE, TestDefinition,\
    defaultTestSuite, batchTestSuite, BatchTestDefinition
import time
from typing import List, Set, Tuple, Union

_default_no_edge = -1
_source = 0
_sink = 1

class BatchChecker(NaiveChecker, BaseOnlineChecker):
    """Set of paths to check using two flip tolerant search."""

    _invalid_node = -1
    _debug = False

    def __init__(self):
        super().__init__()

    #### Utility functions ####

    def getIndex(self, src, snk):
        """Returns the index of that an edge from source to sink would take in
        the vector space of the edges of this graph."""
        return src*len(self.graph[0]) + snk

    def vectorize(self, path):
        """Get a vector corresponding to a path."""
        vector = [0 for i in range(len(self.graph)**2)]
        for i in range(len(path)-1):
            vector[self.getIndex(path[i], path[i+1])] = (vector[self.getIndex(i, i+1)] + 1) % 2
        return vector

    def vectorizePair(self, pair):
        """Return vector corresponding to a pair of paths."""
        vector1, vector2 = (self.vectorize(path) for path in pair)
        return addVectors(vector1, vector2)

    def findCoTreePairs(self, node):
        """Find co tree starting at node."""
        allNodes = self.getSuccessors(node)
        tree = self.getTree(node)
        coTree = {}
        for src in allNodes:
            for snk in allNodes:
                if self.graph[src][snk] != _invalid_node and (src, snk) not in tree:
                    pair = (
                        self.getTreePath(node, snk, tree),
                        self.getTreePath(node, src, tree) + [snk]
                    )
                    coTree.add(pair)
        return coTree
    
    def getTreePath(self, src, snk, tree):
        """Reconstruct path in tree from source to sink given tree edge set."""
        currentNode = snk
        path = [snk]
        while currentNode != snk:
            edge = self.getBackEdge(snk, tree)
            currentNode = edge[0]
            path += [currentNode]
        return path
    
    def getBackEdge(self, snk, st):
        """Get some edge (*, snk) from set st."""
        for edge in st:
            if edge[1] == snk:
                return edge

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

    def gaussianReduce(self, matrix):
        """Applies Gaussian reduction on matrix and returns true when last 
        column vector is linearly dependent on all others."""
        if len(matrix) == 0:
            return True
        pivot = 0
        for column in range(len(matrix[0])-1):
            if matrix[pivot][column] == 0:
                for row in range(pivot+1, len(matrix)):
                    if matrix[row][column] == 1:
                        matrix[pivot] = [(a+b)%2 for a, b in zip(matrix[pivot],
                            matrix[row])]
                        break
            if matrix[pivot][column] == 1:
                for row in list(range(pivot+1, len(matrix)))[::-1]:
                    if matrix[row][column] == 1:
                        matrix[row] = [(a-b)%2 for a, b in zip(matrix[row], 
                            matrix[pivot])]
                pivot += 1
        for row in range(pivot, len(matrix)):
            if matrix[row][-1] == 1:
                return False
        return True

    def sigma(self, subst: Set, allPairs: Set):
        return {
            pair for pair in allPairs if self.gaussianReduce(self.matrixify(
                self.smallerPiecesIntersection(subst,
                pair), pair)) }
    
    def smallerPiecesIntersection(self, subst, pair):
        """Get subset of subst such that the members are smaller than pair. 
        (<> function intersected with subset)."""
        sources = self.getSuccessors(pair[_source])
        sinks = self.getPredecessors(pair[_sink])
        return {bilinking for bilinking in subst if bilinking[_source] in sources 
            and bilinking[_sink] in sinks}
        
    def matrixify(self, pieces, lastPair):
        """Given a list of pairs and the last pair in the problem, create the
        corresponding matrix in order to Gaussian reduce."""
        matrix = []
        pieces = [self.vectorizePair(piece) for piece in pieces]
        pair = self.vectorizePair(lastPair)
        for row in range(len(self.graph)**2):
            rowEntries = [piece[row] for piece in pieces]
            rowEntries += [pair[row]]
            matrix += [rowEntries]
        return matrix

    def getSuccessors(self, node):
        return set(self.getAllSuccessors(node, False))

    def getPredecessors(self, node):
        return set(self.getAllPredecessors(node, False))

    #### Public interface ####

    def getPathsToCheck(self) ->  Set[Tuple[List[int], List[int]]]:
        """Return the pairs of path whose equality implies path independence of 
        the new graph."""
        startTime = time.time()
        Rs = set()
        for node in range(len(graph)):
            Rs = Rs.union(self.findCoTreePairs(node))
        
        spanningSet = Rs.copy()
        for pair in spanningSet:
            if spanningSet.issubset(self.sigma(Rs.copy.remove(pair), spanningSet)):
                Rs.remove(pair)
        
        endTime = time.time()
        self.timeTaken = endTime - startTime
        return Rs

#### Quick tests ####

def testGetPathsToCheck(testDefinition: Union[TestDefinition, BatchTestDefinition]):
    checker = BatchChecker()
    checker.setGraph(testDefinition.test_graph)
    paths = checker.getPathsToCheck()
    assertActualIsSuperset(testDefinition.expected_solution, checker.getPathsToCheck())
    assert(checker.timeTaken > 0)

def testVectorize(testDefinition: Union[TestDefinition, BatchTestDefinition]):
    checker = BatchChecker()
    checker.setGraph(testDefinition.test_graph)
    if hasattr(testDefinition, 'paths'):
        vectors = [checker.vectorize(v) for v in testDefinition.paths]
        for i in range(len(vectors)):
            assertEqual(testDefinition.expected_vectors[i], vectors[i])

def testMatrixify(testDefinition: Union[TestDefinition, BatchTestDefinition]):
    checker = BatchChecker()
    checker.setGraph(testDefinition.test_graph)
    if hasattr(testDefinition, 'pieces'):
        matrix = checker.matrixify(testDefinition.pieces, testDefinition.finalPair)
        assertEqual(testDefinition.expected_matrix, matrix)

def testGaussianReduce():
    checker = BatchChecker()
    checker.setGraph(test_graph)
    _testGraph1 = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]]
    assert(not checker.gaussianReduce(_testGraph1))
    _testGraph2 = [
        [1, 0, 0, 1],
        [0, 1, 0, 0],
        [0, 0, 1, 1]]
    assert(checker.gaussianReduce(_testGraph2))
    _testGraph3 = [
        [1, 0, 1],
        [0, 1, 1],
        [0, 1, 1]]
    assert(checker.gaussianReduce(_testGraph3))

def runAllTests(testSuite: List[Union[TestDefinition, BatchTestDefinition]] = defaultTestSuite):
    print('\033[0m' + "Running baseOnlinePathChecker Tests")
    testGaussianReduce()
    for testDefinition in testSuite:
        # testGetPathsToCheck(testDefinition)
        testVectorize(testDefinition)
        testMatrixify(testDefinition)
    print(Fore.GREEN + 'Run Completed')

#### Execute ####

def main():
    runAllTests(batchTestSuite)

if __name__=="__main__":
    main()