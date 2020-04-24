import requests 
import numpy as np

DEBUG = False
GRAPH = []
# To get indices of currencies
CURRENCY_LIST = []

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
            row += [0]
        GRAPH += [row]


def addRates(base, target, rate):
    global GRAPH
    GRAPH[indexOf(base)][indexOf(target)] = rate    

def addRow(base, rates):
    global GRAPH
    for currency,rate in rates.iteritems():
        GRAPH[indexOf(base)][indexOf(currency)]=rate

###############################################

# pretty printing

np.set_printoptions(formatter={'float': lambda x: "{0:0.1f}".format(x)}, threshold=100000)

# api-endpoint 
URL = "https://api.exchangeratesapi.io/latest?"

base = 'USD'
baseEncodedName = 'u\'{}\''.format(base)
symbols = []

if base:
    URL += 'base='+base
if len(symbols) > 0:
    URL += '&symbols='+symbols[0]
    for currency in symbols[1:]:    
        URL += ','+currency

# sending get request and saving the response as response object 
r = requests.get(url = URL) 
  
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

constructGraph(rates.keys())
addRow(base, rates)
print(np.matrix(GRAPH))