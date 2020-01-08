"""Find all paths between two nodes in a directed graph."""

"""Graph is encoded as an adjacency matrix with i,j = 1 indicating that there is an edge from i to j"""
_GRAPH = [[ 0, 1, 1, 0],
	  [ 1, 0, 1, 1],
	  [ 0, 0, 0, 1],
	  [ 0, 0, 0, 0]]

def findPaths(s, t, graph = _GRAPH):
	"""Print the paths from s to t in graph."""
	print(getList(s, t, graph, {}))

def getList(s, t, graph, visited):
	"""Return a list of paths from s to t."""
	if s==t:
		return [[t]]
	neighbours = getNeighbours(s, graph, visited)
	ans = []
	for neighbour in neighbours:
		visited[s]=''
		ans+=[[s]+lst for lst in getList(neighbour, t, graph, visited)]
		visited.pop(neighbour, '')
	print("{} has paths {}".format(s, str(ans)))
	return ans

def getNeighbours(s, graph, visited):
	"""return a list of the neighbours of s that haven't been visited"""
	lst = filter(lambda x : x not in visited and graph[s][x]==1, range(len(graph[s])))
	print("{} has neighbours {}".format(s, str(lst)))
	return lst

findPaths(0, 3)
