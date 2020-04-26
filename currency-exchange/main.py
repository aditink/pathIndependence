import requests 
import numpy as np
import copy

# Assume that a graph doesn't have more edges nodes than this
INFTY = 1000000
NO_EDGE = -1
DEBUG = False
DEV_DEBUG = True
GRAPH = []
# To get indices of currencies
CURRENCY_LIST = []
# api-endpoint 
endPoint = "https://api.exchangeratesapi.io/latest?"

# TODO add:
# 1. Commandline arguments.
# 2. Historic rate.
# 3. Connection to path checking algorithm.

###############################################

# Helpers
def indexOf(currency):
    global CURRENCY_LIST
    return CURRENCY_LIST.index(currency)

def constructGraph(currencies):
    global CURRENCY_LIST
    global GRAPH
    CURRENCY_LIST = currencies
    # GRAPH = [[0]*len(CURRENCY_LIST)]*len(CURRENCY_LIST)
    for _ in range(len(CURRENCY_LIST)):
        row = []
        for _ in range(len(CURRENCY_LIST)):
            row += [NO_EDGE]
        GRAPH += [row]


def addRates(base, target, rate, checkIndependence=False):
    global GRAPH
    isValid = True
    if (checkIndependence):
        isValid = checkIndependenceFunc((base, target, rate))
    if (isValid):
        GRAPH[indexOf(base)][indexOf(target)] = rate    
    return isValid

# Does not call addRates for efficiency.
def addRow(base, rates, checkIndependence=False):
    global GRAPH
    for currency,rate in rates.iteritems():
        isValid = True
        if (checkIndependence):
            isValid = checkIndependenceFunc((base, currency, rate))
        if (isValid):
            GRAPH[indexOf(base)][indexOf(currency)]=rate
        else:
            return False
    return True

def makeUrl(base, symbols):
    URL = endPoint
    if base:
        URL += 'base='+base
    if len(symbols) > 0:
        URL += '&symbols='+symbols[0]
        for currency in symbols[1:]:    
            URL += ','+currency
    return URL

def makeRequest(base, symbols=[]):
    # sending get request and saving the response as response object 
    r = requests.get(url = makeUrl(base, symbols))   
    # extracting data in json format 
    data = r.json() 
    if (DEBUG): 
        print(data)  
    # Extract graph
    rates = data['rates']
    if DEBUG:
        for currency,rate in rates.iteritems():
            print(currency)
            print(rate)
    return rates

# New edge is (source, target, rate)
def checkIndependenceFunc(newEdge):
    return True

###############################################

# Path Independence checking.

# Test case for path finding
test_graph = [
    [NO_EDGE,       1, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE],
    [NO_EDGE, NO_EDGE,       1, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE],
    [NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE],
    [NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE,       1, NO_EDGE,       1, NO_EDGE],
    [NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE,       1, NO_EDGE, NO_EDGE],
    [NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE],
    [NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE,       1],
    [NO_EDGE, NO_EDGE,       1, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE]]
test_s = 2
test_t = 3
test_new_edge = (2, 3)

# Version for *a* path as opposed to shortest path

# graphPathsToS[v] = path from v to s.
graphPathsToS = []
graphPathsFromT = []

# Get an empty path list
def getEmptyPathList():
    paths = []
    for _ in range(len(GRAPH)):
        paths += [[]]
    return paths

def getForwardEdges(source):
    return [i for i in range(len(GRAPH)) if GRAPH[source][i] != NO_EDGE]

def getBackwardEdges(sink):
    return [i for i in range(len(GRAPH)) if GRAPH[i][source] != NO_EDGE]

def populatePathsFromT(t):
    global graphPathsFromT
    graphPathsFromT = getEmptyPathList()
    visited = set()
    currentNode = t
    stack = [t]
    path = []
    while (len(stack) > 0):
        currentNode = stack[-1]
        stack.pop()
        if (currentNode in visited):
            path.pop()
        else:
            visited.add(currentNode)
            path += [currentNode]
            graphPathsFromT[currentNode] = copy.deepcopy(path)
            stack += [currentNode]+[edge for edge in getForwardEdges(currentNode) if edge not in visited]
    if DEBUG or DEV_DEBUG:
        print("graphPathsFromT: {}".format(graphPathsFromT))


##############################################

# Path Independence checking

# Version for shortest path

# This is a dictionary implemented as a 2d array
# to store the paths in the Graph, Bellman-Ford style.
# {Node v -> {Node u -> (distance, path_as_a_list)}}
oldGraphPaths = []
newGraphPaths = []

# initialize graphPaths to 2d array of (dist, path)
def initPathDict(graphPaths, s):
    # global oldGraphPaths
    for u in range(len(GRAPH)):
        pathDict = []
        for v in range(len(GRAPH)):
            pathDict += [(0 if u==v else INFTY, [])]
        oldGraphPaths += [pathDict]
    if (DEBUG or DEV_DEBUG):
        print('oldGraphPaths: {}'.format(oldGraphPaths))

# Assumption: in graph, -1 means no edge.
def buildEdgeList():
    global edges
    for source in range(len(GRAPH)):
        for sink in range(len(GRAPH)):
            if (GRAPH[source][sink] != -1):
                edges += [(source, sink)]
    if (DEBUG or DEV_DEBUG):
        print('Edges: {}'.format(edges))

def buildOldPathDictionary():
    global oldGraphPaths
    initPathDict()
    buildEdgeList()
    for node in range(len(GRAPH)):
        for (source, sink) in edges:
            (old_dist, old_path) = oldGraphPaths[node][sink]
            (new_dist, new_path) = oldGraphPaths[node][source]
            if (new_dist+1 < old_dist):
                oldGraphPaths[node][sink] = (new_dist+1, old_path + [sink])
    if DEBUG or DEV_DEBUG:
        print('oldPathGraphs: {}'.format(oldGraphPaths))

def updateGlobalsForEdgeAccepted(newEdge):
    edges += [newEdge]
    oldGraphPaths = newGraphPaths

def updateNewGraphPaths(newEdge):
    # TODO update newGraphPaths dictionary
    pass

###############################################

# Pretty printing

np.set_printoptions(formatter={'float': lambda x: "{0:0.4f}".format(x)}, threshold=10000)

Setting up graph
base = 'USD'
# Eventually want to be able to parse this from commandline.
symbols = []

rates = makeRequest(base=base)
constructGraph(rates.keys())
addRow(base, rates)
if DEBUG:
    print(np.matrix(GRAPH))

for currency in CURRENCY_LIST:
    rates = makeRequest(base=currency)
    addRow(base=currency, rates=rates, checkIndependence=True)

print(np.matrix(GRAPH))
print()


# GRAPH = test_graph
# populatePathsFromT(test_t)
