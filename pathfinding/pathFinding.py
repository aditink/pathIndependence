"""Find all paths between two nodes in a directed graph."""
"""Graph is encoded as an adjacency matrix with i,j = 1 indicating that there is an edge from i to j"""

import random
from itertools import combinations

_GRAPH = \
[[0, 1, 1, 0],
 [0, 0, 1, 0],
 [1, 0, 0, 0],
 [0, 0, 0, 0]]

# _GRAPH = \
# [[0, 1, 1, 1, 0, 1],
#  [0, 0, 1, 1, 1, 1],
#  [0, 1, 0, 0, 0, 0],
#  [1, 1, 0, 0, 1, 0],
#  [1, 0, 0, 1, 0, 1],
#  [0, 1, 1, 1, 1, 0],]

# ----------- Fast functions -----------

# A list of all pairs of paths that both share a source and sink
#  and include 'edge' in the path
# Throws an error if 'edge' is not in the graph
def findEdgeConflicts(s, t, graph = _GRAPH):
    if graph[s][t] != 1:
        raise "Edge to check conflicts with does not exist"
    return findNewConflicts(s, t, graph)[0]

# A list of all pairs of paths that both share a source and sink
#  and include 'edge' in the path
# Adds 'edge' if it is not already part of the graph
def findNewConflicts(s, t, graph = _GRAPH):
    graph[s][t] = 0
    result = []
    for path,flips in findFlippingPoints(t, s, graph, flips_allowed=2):
        # It's a cycle, so find all cycle conflicts
        if len(flips) == 0:
            for i in range(len(path)):
                result.append(([path[i]] + path[i+1:] + path[:i+1], [path[i]]))
        # Common ancestor, so check two meeting paths
        if len(flips) == 1:
            new_res = [s]
            for i in range(len(path)):
                new_res.append(path[i])
                if path[i] == flips[0]:
                    rev_path = path[i:]
                    rev_path.reverse()
                    new_res = (new_res, rev_path)
                    break
            result.append(new_res)
        # Two-flip result, so compare paths between flip source and sink
        if len(flips) == 2:
            new_res = []
            next_path = []
            for i in range(len(path)):
                next_path.append(path[i])
                # Note that we assume the order of reported flips
                # Flips must be ordered to occur in the path _from_ s to t
                if path[i] == flips[0]:
                    new_res = next_path
                    next_path = [path[i]]
                if path[i] == flips[1]:
                    next_path.reverse()
                    new_res = (path[i:] + new_res, next_path)
                    break
            result.append(new_res)
    graph[s][t] = 1
    return (result, graph)

# -------- Reference functions ---------

# A list of _all_ pairs of paths that share a source and sink
def findAllConflictingPathsReference(graph = _GRAPH):
    result = []
    allPaths = findAllPaths(graph)
    for sources in allPaths:
        result += list(combinations(allPaths[sources], 2))
    return result

# A list of all pairs of paths that both share a source and sink
#  and include 'edge' in the path
# Throws an error if 'edge' is not in the graph
def findEdgeConflictsReference(s, t, graph = _GRAPH):
    if graph[s][t] != 1:
        raise "Edge to check conflicts with does not exist"
    result = []
    for path in findAllConflictingPathsReference(graph):
        for i in range(2):
            for j in range(len(path[i]) - 1):
                if path[i][j] == s and path[i][j + 1] == t:
                    result.append(path)
    return result

# A list of all pairs of paths that both share a source and sink
#  and include 'edge' in the path
# Adds 'edge' if it is not already part of the graph
def findNewConflictsReference(s, t, graph = _GRAPH):
    graph[s][t] = 1
    return (findEdgeConflictsReference(s, t, graph), graph)
    
# ---------- Testing functions ---------

# Returns a size x size adjacency matrix
#  with an average of 'density' 0/1 edge ratio
def generateGraph(size, density=.5):
    to_return = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if random.random() < density:
                to_return[i][j] = 1
    return to_return

# Returns a list of edges contained in the given graph
def graphEdges(graph):
    to_return = []
    for i in range(len(graph)):
        if len(graph[i]) != len(graph):
            raise "Graph must be a square matrix"
        for j in range(len(graph[i])):
            if graph[i][j] == 1:
                to_return.append([i, j])
    return to_return

# Find and return all paths from s to t in the given graph
def findPaths(s, t, graph = _GRAPH):
    return findDirectedPaths(s, t, graph)

# A dict of all paths in the graph
def findAllPaths(graph = _GRAPH):
    toReturn = {}
    for i in range(len(graph)):
        if len(graph[i]) != len(graph):
            raise "Graph must be a square matrix"
        for j in range(len(graph[i])):
            p = findPaths(i, j, graph)
            if len(p) > 0:
                toReturn["(" + str(i) + ", " + str(j) + ")"] = p
    return toReturn

# ---------- Helper functions ----------

# Returns a list of all directed paths from s to t
# Directed paths may include up to 'flips_allowed' direction flips
def findDirectedPaths(s, t, graph, flips_allowed = 0):
    return list(map(lambda x : x[0], findDirectedPathsRec(s, t, graph, set(), -1, True, flips_allowed)))

def findFlippingPoints(s, t, graph, flips_allowed = 0):
    return findDirectedPathsRec(s, t, graph, set(), -1, True, flips_allowed)

def findDirectedPathsRec(s, t, graph, visited, first_node, forward, flips_allowed):
    if s==t and not first_node == -1:
        return [([t], [])]
    if first_node == -1:
        first_node = s
    elif s == first_node:
        return []
    else:
        visited.add(s)
    neighbours = getNeighbours(s, graph, visited, forward)
    ans = []
    for neighbour in neighbours:
        res = findDirectedPathsRec(neighbour, t, graph, visited.copy(), first_node, forward, flips_allowed)
        ans += [([s]+lst[0], lst[1]) for lst in res]
    if flips_allowed > 0:
        flips_allowed -= 1
        forward = not forward
        flippedNeighbors = getNeighbours(s, graph, visited, forward)
        for neighbour in flippedNeighbors:
            res = findDirectedPathsRec(neighbour, t, graph, visited.copy(), first_node, forward, flips_allowed)
            ans += [([s]+lst[0], [s] + lst[1]) for lst in res]
    return ans + ([([t], [])] if s==t else [])

# Return a list of the neighbours of s that haven't been visited
def getNeighbours(s, graph, visited, forward):
    graph_check = (lambda x : graph[s][x]==1) if forward else (lambda x : graph[x][s]==1)
    lst = filter(lambda x : x not in visited and graph_check(x), range(len(graph[s])))
    return lst

# Print a dictionary line-by-line (not very pythonic, but whatever)
def printDict(d):
    for item in d:
        print(str(item) + ": " + str(d[item]))


def main():
    # --- Accuracy Test ---
    printDict(findAllPaths())
    print("-------------------")
    s, t = (0, 1)
    print(findEdgeConflictsReference(s, t))
    print("-------------------")
    print(findEdgeConflicts(s, t))

    # --- Speed Test ---
    # size = 11
    # edges = graphEdges(generateGraph(size))
    # g = generateGraph(size, 0)
    # for s,t in edges:
    #     g = findNewConflicts(s, t, g)[1]
    # print(g)

if __name__=="__main__":
    main()