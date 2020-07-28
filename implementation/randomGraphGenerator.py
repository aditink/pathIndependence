"""Define a script that generates random graphs."""
import random
from typing import List, Tuple

NO_EDGE = -1
_EDGE = 1

class evaluationGraph:
    """Type for input to evaluation script."""

    def __init__(self, graph, newEdge):
        self.graph = graph
        self.newEdge = newEdge
        self.newEdgeSource = newEdge[0]
        self.newEdgeSink = newEdge[1]
        self.graphWithEdge = graph
        self.graphWithEdge[self.newEdgeSource][self.newEdgeSink] = _EDGE

def generateGraph(density: float, nodes: int) -> evaluationGraph:
    """generate a random graph of the given density, with a given number of 
    nodes along with a new edge to add to the graph.
    Density = number of edges / total possible number of edges, i.e. n^2.
    Assume graph can have at least one edge."""
    allPaths = [(src, snk) for src in range(nodes) for snk in range(nodes)]
    graph = [[NO_EDGE for col in range(nodes)] for row in range(nodes)]
    # TODO add graceful failure for edge case of 0 edges.
    randomList = random.sample(allPaths, max(int(density * nodes**2), 1))
    for edge in randomList[1:]:
        (src, snk) = edge
        graph[src][snk] = _EDGE
    return evaluationGraph(graph, randomList[0])

def generateAcyclicGraph(density: float, nodes: int) -> evaluationGraph:
    """Generate a random acyclic graph of the given density, with a given number 
    of nodes along with a new edge to add to the graph.
    Density = number of edges / total possible number of edges, i.e. n^2."""
    # Generate a graph that is a lower triangular matrix.
    # https://mathematica.stackexchange.com/questions/608/how-to-generate-random-directed-acyclic-graphs.
    allPaths = [(src, snk) for src in range(nodes) for snk in range(src)]
    graph = [[NO_EDGE for col in range(nodes)] for row in range(nodes)]
    #TODO handle density>0.5
    randomList = random.sample(allPaths, min(max(int(density * nodes**2), 1), len(allPaths)))
    #TODO factor out addition to graph.
    for edge in randomList[1:]:
        (src, snk) = edge
        graph[src][snk] = _EDGE
    return evaluationGraph(graph, randomList[0])