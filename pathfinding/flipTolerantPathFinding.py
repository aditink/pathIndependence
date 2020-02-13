"""Find all paths between two nodes in a directed graph."""

"""Graph is encoded as an adjacency matrix with i,j = 1 indicating that there is an edge from i to j"""
_GRAPH = [[ 0, 1, 1, 0],
	  [ 1, 0, 1, 1],
	  [ 0, 0, 0, 1],
	  [ 0, 0, 0, 0]]

def findPaths(s, t, flips=0, graph = _GRAPH):
	"""Print the paths from s to t in graph."""
	print(getList(s, t, graph, {}, flips))

def getList(s, t, graph, visited, flips=0):
	"""Return a {number of flips -> list of paths from s to t}."""
	if s==t:
            return {0 :[[t]]}
	neighbours = getNeighbours(s, graph, visited)
	sameflipsAns = {} 
	for neighbour in neighbours:
	    visited[s]=''
            sameflipsAns={ flip:sameflipsAns.get(flip, [])+[[s]+lst for lst in getList(neighbour, t, graph, visited, flip).get(flip, [])] for flip in range(flips+1) }
	    visited.pop(neighbour, '')
	print("{} has forward paths {}".format(s, str(sameflipsAns)))
        if flips==0:
            return sameflipsAns
	preds = getPredecessors(s, graph, visited)
	for neighbour in preds:
	    visited[s]=''
            sameflipsAns={ flip:sameflipsAns.get(flip, [])+[[s]+lst for lst in getList(neighbour, t, graph, visited, flip-1).get(flip-1, [])] for flip in range(flips+1) }
	    visited.pop(neighbour, '')
	print("{} has paths {}".format(s, str(sameflipsAns)))
        return sameflipsAns

def getNeighbours(s, graph, visited):
	"""return a list of the neighbours of s that haven't been visited"""
	lst = filter(lambda x : x not in visited and graph[s][x]==1, range(len(graph[s])))
	print("{} has neighbours {}".format(s, str(lst)))
	return lst

def getPredecessors(s, graph, visited):
        """return a list of the (immediate) predecessors of s that haven't been visited"""
        lst = [i for i in range(len(graph)) if i not in visited and graph[i][s]==1]
        print("{} has predecessors {}".format(s, str(lst)))
        return lst


findPaths(0, 3, 1)
