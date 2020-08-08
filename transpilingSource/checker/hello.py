import time

_default_no_edge = -1


class BaseOnlineChecker():
    """Implements base functionality common to all PathCheckers."""

    _invalid_node = -1
    _debug = False

    #### Utility functions ####

    def getForwardEdges(self, source: int) -> List[int]:
        return [i for i in range(len(self.graph)) \
            if self.graph[source][i] != self._no_edge]

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
    
    def getAllPredecessors(self, node, memoize = False) -> List[int]:
        """Returns a list of nodes that are predecessors of this one.
        Memoize if source of new edge."""
        if not self.compactBkdGraph:
            self.buildCompactBkdGraph()
        memoize = memoize or node == self.newEdgeSource
        if memoize:
            pathDict = dict()
        visited = set()
        # To store visitedNodes ordered closest to new edge first.
        visitedList = []
        currentNode = node
        stack = [currentNode]
        path = []
        while (len(stack) > 0):
            currentNode = stack.pop()
            if currentNode == self._invalid_node:
                path = path[1:]
            elif currentNode not in visited:
                visited.add(currentNode)
                visitedList += [currentNode]
                path = [currentNode] + path
                if (memoize):
                    pathDict[currentNode] = self.deepcopyList(path)
                stack += [self._invalid_node] + self.compactBkdGraph[currentNode]
        if self._debug:
            print("getAllPredecessors: node: {} and visitedList: {}".format(
                node, visitedList))
        if node == self.newEdgeSource:
            self.pathsToNewEdgeSource = pathDict
        if memoize:
            self.pathsToNode[node] = pathDict
        return visitedList
    
    def getAllPredecessorsUnordered(self, node, memoize = True) -> Set[int]:
        """Returns a list of nodes that are predecessors of this one.
        Memoize if source of new edge."""
        memoize = memoize or node == self.newEdgeSource
        if memoize:
            pathDict = dict()
        visited = set()
        currentNode = node
        stack = [currentNode]
        path = []
        while (len(stack) > 0):
            currentNode = stack.pop()
            if currentNode == self._invalid_node:
                path = path[1:]
            elif currentNode not in visited:
                visited.add(currentNode)
                path = [currentNode] + path
                if (memoize):
                    pathDict[currentNode] = self.deepcopyList(path)
                stack += [self._invalid_node] + self.compactBkdGraph[currentNode]
        if self._debug:
            print("getAllPredecessors: node: {} and visitedList: {}".format(
                node, visited))
        if node == self.newEdgeSource:
            self.pathsToNewEdgeSource = pathDict
        if memoize:
            self.pathsToNode[node] = pathDict
        return visited

    def getAllSuccessors(self, node) -> List[int]:
        """Returns a list of nodes that are successors of this one.
        Memoize if sink of new edge."""
        if not self.compactFwdGraph:
            self.buildCompactFwdGraph()
        visited = set()
        # maintain a separate list to get ordering where closest node is first.
        visitedList = []
        currentNode = node
        stack = [node]
        path = []
        # More or less DFS.
        while (len(stack) > 0):
            currentNode = stack.pop()
            if currentNode == self._invalid_node:
                path.pop()
            elif currentNode not in visited:
                visited.add(currentNode)
                visitedList += [currentNode]
                path += [currentNode]
                if (node == self.newEdgeSink):
                    self.pathsFromNewEdgeSink[currentNode] = self.deepcopyList(path)
                stack += [self._invalid_node] + self.compactFwdGraph[currentNode]
        if self._debug:
            print("getAllSuccessors: node = {} and visited list: {}".format(
                node, visitedList))
        return visitedList

    def deepcopyList(self, path):
        copy = []
        for entry in path:
            copy += [entry]
        return copy

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

    def findPair(self, source: int, sink: int) -> Tuple[List[int], List[int]]:
        """Finds a pair of paths from the given source to sink, the first 
        includes the new edge, and the second one doesn't.
        In case of a cycle the second path is just the single node,
        representing the identity on the node."""
        if not bool(self.pathsFromNewEdgeSink):
            self.getAllSuccessors(self.newEdgeSink)
        if not bool(self.pathsToNewEdgeSource):
            self.getAllPredecessors(self.newEdgeSource)
        firstSegment = self.pathsToNewEdgeSource[source]
        lastSegment = self.pathsFromNewEdgeSink[sink]
        (_, secondPath) = self.findPath(source, sink)
        # Special case of Identity.
        if source == sink:
            secondPath = self.identityFunction(source)    
        return(firstSegment + lastSegment, secondPath)

    #### Public interface ####

    def __init__(self):
        self.graph = [[]]
        self.identityFunction = lambda source : [source]
        self.newEdgeSource = self._invalid_node
        self.newEdgeSink = self._invalid_node
        self.timeTaken = 0
        self.compactFwdGraph = []
        self.compactBkdGraph = []
        self.pathsToNewEdgeSource = dict()
        self.pathsFromNewEdgeSink = dict()
        # sink node -> {source node -> path}
        self.pathsToNode = dict()
        self._no_edge = _default_no_edge
        self.noIdentity = False
        # Hack to make sub classes works
        self._invalid_node = -1
    
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
    
    def setIdFunction(self, idFunction):
        """Store the special representation of identity function."""
        self.identityFunction = idFunction


class OptimalSetPathChecker(BaseOnlineChecker):
    """Path checker that returns minimal set for verification 
    for online problem."""

    def __init__(self):
        super().__init__()

    def getSuccessors(self, source: int, sink: int) -> Set[int]:
        """Returns a set of pairs such that verifying a path between given
        source and sink implies also that all the pairs in the returned set are
        equal."""
        predecessors = self.getAllPredecessors(source)
        successors = self.getAllSuccessors(sink)
        if (self.noIdentity and source == sink):
            return {(src, snk) for src in predecessors for snk in successors 
            if src == snk}
        return {(src, snk) for src in predecessors for snk in successors}

    def getRootPairs(self) -> List[List[int]]:
        """Returns a graph where each node represents a (source, sink) pair in
        self.graph. 
        Map from (source, sink) to node number in self.dependencyNodeMap.
        Node A succeeds node B if checking a pair of B implies that 
        the paths pairs of A must also be equal."""
        acceptedPairs = set()
        # Get set of all predecessors, successors.
        predecessors = self.getAllPredecessors(self.newEdgeSource)
        successors = self.getAllSuccessors(self.newEdgeSink)
        # Go through each element in predecessors X successors.
        # For efficiency, closest pairs to new edge should appear first.
        potentialPairs = {(source, sink) for source in predecessors \
            for sink in successors}
        orderedPotentialPairs = [(source, sink) for source in predecessors \
            for sink in successors]
        while (len(potentialPairs) != 0):
            # using ordering is a heuristic to (hopefully) improve performance,
            # so parent is usually checked before child.
            (source, sink) = orderedPotentialPairs.pop(0)
            if (source, sink) in potentialPairs:
                potentialPairs.remove((source, sink))
                (pathExists, _) = self.findPath(source, sink)
                if pathExists:
                    currentPairSuccessors = self.getSuccessors(source, sink)
                    for redundantPair in acceptedPairs.intersection(
                        currentPairSuccessors):
                        acceptedPairs.remove(redundantPair)
                    for redundantPair in potentialPairs.intersection(
                        currentPairSuccessors):
                        potentialPairs.remove(redundantPair)
                    acceptedPairs.add((source, sink))
        return acceptedPairs        

    def getPathsToCheck(self) ->  List[Tuple[List[int], List[int]]]:
        """Return the pairs of path whose equality implies path independence of 
        the new graph."""
        startTime = time.time()
        subset = self.getRootPairs()
        # Find paths for each pair in the subset
        pathPairs = []
        for node in subset:
            (source, sink) = node
            pathPairs += [self.findPair(source, sink)]
        endTime = time.time()
        self.timeTaken = endTime - startTime
        return pathPairs


###### Front end code ######

_EMPTY = 0
checker = OptimalSetPathChecker()
# placeholder oracle
oracle = lambda matrix1, matrix2 : matrix1==matrix2

def getTime():
    document.getElementById('time').innerHTML = (
            checker.getComputeTime()
        )

def getPathsToCheck():
    if (len(checker.graph)!=_EMPTY and len(checker.graph[0])!=_EMPTY) \
        and checker.newEdgeSource!=checker._invalid_node \
        and checker.newEdgeSink!=checker._invalid_node:
        document.getElementById('paths').innerHTML = (
            checker.getPathsToCheck()
        )
    else:
        document.getElementById('paths').innerHTML = (
            "Graph or new edge not yet set."
        )

def setGraph():
    graphString = document.getElementById('graph').value
    rows = graphString.split(';')
    graph = [] 
    for rowString in rows:
        row = []
        splitRow = rowString.split()
        for edge in splitRow:
            #must replace with parseInt after transcrypt applies.
            row.append(int(edge))
        graph.append(row)
    # cells = [[int(edge) for edge in row.split()] for row in rows]
    checker.setGraph(graph)

def setNewEdge():
    pass


##### To integrate with gator #####

def scalarMultiply(scalar, matrix):
    ans = []
    for row in matrix:
        ansRow = []
        for elem in row:
            ansRow.append(scalar*elem)
        ans.append(ansRow)
    return ans

def metrixMultiple(mat1, mat2):
    """Takes scalars and metrices as parameters. Returns product."""
    if isinstance(mat1, list):
        if isinstance(mat2, list):
            # number of cols matrix1 must be equal to rows of matrix2
            assert(len(mat2) == len(mat1[0]))
            ans = []
            for row in len(mat1):
                ansRow = []
                vector1 = mat1[row]
                for col in len(mat2[0]):
                    vector2 = [mat2[i][row] for i in range(len(mat2))]
                    sumOfEntries = 0
                    for i in range(len(vector2)):
                        sumOfEntries += vector1[i]*vector2[i]
                    ansRow.append(sumOfEntries)
                ans.append(ansRow)
            return ans
        else:
            return scalarMultiply(scalar=mat2, matrix=mat1)
    else:
        if isinstance(mat2, list):
            return scalarMultiply(scalar=mat1, matrix=mat2)
        else:
            # Both scalar.
            return mat1*mat2

def getMatrixOfPaths(path, graphValues):
    """Given a path get the matrix that is the product of all matrices along the path."""
    productMatrix = 1
    if (len(path) < 2):
        return productMatrix
    for i in range(1, len(path)):
        edgeMatrix = graphValues()
        matrixMultiply(productMatrix, edgeMatrix)

def checkPaths(pathsToCheck, graphValues, oracle):
    """Given a list of paths to check, return true if all pairs are equal per oracle."""
    for pathPair in pathsToCheck:
        (path1, path2) = pathPair
        matrix1 = getMatrixOfPaths(path1, graphValues)
        matrix2 = getMatrixOfPaths(path2, graphValues)
        if not oracle(matrix1, matrix2):
            return False
    return True

def verify(graph, graphValues, newEdge, oracle):
    """Params:
    -- graph: adjacency matrix of ints. -1 is no edge.
    -- graphValues: adjacency matrix of values of each edge. In this case, each edge is a matrix.
    -- newEdge: tuple or list where first entry is source nad second is sink.
    -- oracle: function of type matrix, matrix -> are these matrices equal."""
    checker.setGraph(graph)
    checker.setEdge(newEdge[0], newEdge[1])
    pathsToCheck = checker.getPathsToCheck()
    return checkPaths(pathsToCheck, graphValues, newEdge, oracle)