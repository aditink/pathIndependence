"""Find all paths between two nodes in a directed graph."""
"""Graph is encoded as an adjacency matrix with i,j = 1 indicating that there is an edge from i to j"""

from itertools import combinations

_GRAPH = \
[[0, 1, 0],
 [1, 0, 1],
 [0, 1, 0]]

# Find and return all paths from s to t in the given graph
def findPathsReference(s, t, graph = _GRAPH):
    return getList(s, t, graph)

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
def findConflictingPathsReference(graph = _GRAPH):
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
    for path in findConflictingPathsReference(graph):
        for i in range(2):
            for j in range(len(path[i]) - 1):
                if path[i][j] == edge[0] and path[i][j + 1] == edge[1]:
                    result.append(path)
    return result

# ---------- Helper functions ----------

def getList(s, t, graph):
    return getListRec(s, t, graph, set(), -1)

def getListRec(s, t, graph, visited, first_node):
    """Return a list of paths from s to t
       Note that first_node allows us to get loops"""
    if s==t and not first_node == -1:
        return [[t]]
    if first_node == -1:
        first_node = s
    neighbours = getNeighbours(s, graph, visited)
    ans = []
    for neighbour in neighbours:
        if not s == t:
            visited.add(s)
        ans += [[s]+lst for lst in getListRec(neighbour, t, graph, visited, first_node)]
        visited.discard(neighbour)
    return ans + ([[t]] if s==t else [])

# Return a list of the neighbours of s that haven't been visited
def getNeighbours(s, graph, visited):
    lst = filter(lambda x : x not in visited and graph[s][x]==1, range(len(graph[s])))
    return lst

# Print a dictionary line-by-line (not very pythonic, but whatever)
def printDict(d):
    for item in d:
        print(str(item) + ": " + str(d[item]))


def main():
    printDict(findAllPaths())
    print("-------------------")
    print(findConflictingPathsReference())
    print("-------------------")
    print(findNewConflictsReference((0, 2)))

if __name__=="__main__":
    main()