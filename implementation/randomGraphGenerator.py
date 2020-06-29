"""Define a script that generates random graphs."""
import random

NO_EDGE = -1

class evaluationGraph:
    """Type for input to evaluation script."""

    def __init__(self, graph, newEdge):
        self.graph = graph
        self.newEdge = newEdge
        self.newEdgeSource = newEdge[0]
        self.newEdgeSink = newEdge[1]

def generateGraph(density: float, nodes: int) -> evaluationGraph:
    """generate a random graph of the given density, with a given number of 
    nodes along with a new edge to add to the graph.
    Density = number of edges / total possible number of edges, i.e. n^2."""
    allPaths = [(src, snk) for src in range(nodes) for snk in range(nodes)]
    graph = [[NO_EDGE for col in range(nodes)] for row in range(nodes)]
    randomList = random.sample(allPaths, int(density * nodes**2))
    for edge in randomList[1:]:
        (src, snk) = edge
        graph[src][snk] = 1
    return evaluationGraph(graph, randomList[0])