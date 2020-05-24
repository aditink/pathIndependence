import requests 
import numpy as np
import copy
from optimalSetPathChecker import OptimalSetPathChecker

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

# Pretty printing

np.set_printoptions(formatter={'float': lambda x: "{0:0.4f}".format(x)}, threshold=10000)

# Setting up graph
base = 'USD'
# # Eventually want to be able to parse this from commandline.
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

checker = OptimalSetPathChecker()