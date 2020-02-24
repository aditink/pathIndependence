"""Find all paths between two nodes in a directed graph."""
"""Graph is encoded as an adjacency matrix with i,j = 1 indicating that there is an edge from i to j"""

from itertools import combinations

_GRAPH = \
[[0, 1],
 [0, 0]]

# _GRAPH = \
# [[0, 1, 1, 1, 0, 1],
#  [0, 0, 1, 1, 1, 1],
#  [0, 1, 0, 0, 0, 0],
#  [1, 1, 0, 0, 1, 0],
#  [1, 0, 0, 1, 0, 1],
#  [0, 1, 1, 1, 1, 0],]

# ----------- Fast functions -----------

def findPaths(s, t, graph = _GRAPH):
    return [[0]]

def findAllConflictingPaths(graph = _GRAPH):
    return [[(0, 0)]]

def findNewConflicts(edge, graph = _GRAPH):
    result = [(0, 0)]
    graph[edge[0]][edge[1]] = 1
    return result

# -------- Reference functions ---------

# Find and return all paths from s to t in the given graph
def findPathsReference(s, t, graph = _GRAPH):
    return getDirectedPaths(s, t, graph)

# A dict of all paths in the graph
def findAllPaths(graph = _GRAPH):
    toReturn = {}
    for i in range(len(graph)):
        if len(graph[i]) != len(graph):
            raise "Graph must be a square matrix"
        for j in range(len(graph[i])):
            p = findPathsReference(i, j, graph)
            if len(p) > 0:
                toReturn["(" + str(i) + ", " + str(j) + ")"] = p
    return toReturn

# A list of _all_ pairs of paths that share a source and sink
def findAllConflictingPathsReference(graph = _GRAPH):
    result = []
    allPaths = findAllPaths(graph)
    for sources in allPaths:
        result += list(combinations(allPaths[sources], 2))
    return result

# A list of all pairs of paths that both share a source and sink
#  and include 'edge' in the path
def findNewConflictsReference(edge, graph = _GRAPH):
    result = []
    graph[edge[0]][edge[1]] = 1
    for path in findAllConflictingPathsReference(graph):
        for i in range(2):
            for j in range(len(path[i]) - 1):
                if path[i][j] == edge[0] and path[i][j + 1] == edge[1]:
                    result.append(path)
    return result

# ---------- Helper functions ----------

# Returns a list of all directed paths from s to t
# Directed paths may include up to 'flips_allowed' direction flips
def getDirectedPaths(s, t, graph, flips_allowed = 0):
    return getDirectedPathsRec(s, t, graph, set(), -1, True, flips_allowed)

def getDirectedPathsRec(s, t, graph, visited, first_node, forward, flips_allowed):
    if s==t and not first_node == -1:
        return [[t]]
    if first_node == -1:
        first_node = s
    elif s == first_node:
        return []
    else:
        visited.add(s)
    neighbours = getNeighbours(s, graph, visited, forward)
    ans = []
    forwardVisited = visited.copy()
    for neighbour in neighbours:
        ans += [[s]+lst for lst in \
            getDirectedPathsRec(neighbour, t, graph, visited.copy(), first_node, forward, flips_allowed)]
        forwardVisited.add(neighbour)
    if flips_allowed > 0:
        flips_allowed -= 1
        forward = not forward
        flippedNeighbors = getNeighbours(s, graph, forwardVisited, forward)
        for neighbour in flippedNeighbors:
            ans += [[s]+lst for lst in \
                getDirectedPathsRec(neighbour, t, graph, visited.copy(), first_node, forward, flips_allowed)]
    return ans + ([[t]] if s==t else [])

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
    printDict(findAllPaths())
    print("-------------------")
    print(findAllConflictingPathsReference())
    print("-------------------")
    print(findNewConflictsReference((1, 0)))

if __name__=="__main__":
    main()