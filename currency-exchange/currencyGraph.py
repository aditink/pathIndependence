from colorama import Fore
import requests 
import numpy as np
import copy
from datetime import datetime
from optimalSetPathChecker import OptimalSetPathChecker
from testUtilities import TestDefinition, defaultTestSuite
import time
import traceback
from typing import List

class CurrencyGraph():
    """Class that holds, builds and manipulates the graph with currency 
    conversion rates"""

    INFTY = 1000000
    NO_EDGE = -1
    DEBUG = False
    baseEndPoint = "https://api.exchangeratesapi.io/"
    endPoint = baseEndPoint + "latest?"
    
    def __init__(self):
        self.graph = []
        self.currencyList = []
        self.base = 'USD' # Default but can change
        self.sleepTime = 0
        np.set_printoptions(formatter={
            'float': lambda x: "{0:0.4f}".format(x)}, threshold=10000)
    
    def setupWithDay(self, year, month, day):
        date = datetime(year, month, day)
        self.endPoint = self.baseEndPoint + date.strftime("%Y-%m-%d") + "?"
        self.setup()
    
    def setup(self):
        """Setup graph with initial row of data from base currency"""
        rates = self.makeRequest(self.base)
        self.initialize(list(rates))
        self.saveRow(self.base, rates)
        if self.DEBUG:
            print("Initialized Graph:")
            print(np.matrix(self.currencyList))
            print(np.matrix(self.graph))

    def initialize(self, currencies):
        """Initialize graph and currency list."""
        self.currencyList = currencies
        self.constructGraph()
    
    def indexOf(self, currency):
        """Gets node in graph that a currency corresponds to."""
        return self.currencyList.index(currency)
    
    def constructGraph(self):
        """Initialize empty graph."""
        for _ in range(len(self.currencyList)):
            row = []
            for _ in range(len(self.currencyList)):
                row += [self.NO_EDGE]
            self.graph += [row]
    
    def saveEntry(self, base, target, rate, checkIndependence=False):
        isValid = True
        extraData = ''
        if (checkIndependence):
            (isValid, extraData) = self.checkIndependenceFunc(base, target, rate)
        if (isValid):
            self.graph[self.indexOf(base)][self.indexOf(target)] = rate
        return (isValid, extraData)

    def getCopyWithNewEdge(self, base, target, rate):
        """Get a copy of this graph with a new edge from base to target added"""
        newGraph = copy.deepcopy(self.graph)
        newGraph[self.indexOf(base)][self.indexOf(target)] = rate
        return newGraph
    
    def saveRow(self, base, rates, checkIndependence=False):
        for currency, rate in rates.items():
            isValid = True
            (isValid, extraInfo) = self.saveEntry(base, currency, rate)
            if not isValid:
                return (isValid, extraInfo)
        return (True, 'Succeeded')

    def makeUrl(self, base, symbols):
        URL = self.endPoint
        if base:
            URL += 'base='+base
        if len(symbols) > 0:
            URL += '&symbols='+symbols[0]
            for currency in symbols[1:]:    
                URL += ','+currency
        return URL

    def makeRequest(self, base, symbols=[]):
        # Failing on Euro to Euro for some reason, so mocking response for now.
        if base == 'EUR' and symbols == ['EUR']:
            return { 'EUR' : 1 }
        # sending get request and saving the response as response object 
        r = requests.get(url = self.makeUrl(base, symbols), timeout = 1)
        # extracting data in json format 
        data = r.json() 
        if (self.DEBUG): 
            print(data)  
        # Extract graph
        rates = data['rates']
        if self.DEBUG:
            for currency,rate in rates.items():
                print(currency)
                print(rate)
        return rates
    
    def addEntry(self, base, target, check = False, retries = 10):
        try:
            rates = self.makeRequest(base, [target])
        except Exception as e:
            if (self.DEBUG):
                print(e)
            if retries > 0:
                self.sleepTime += 2 # 1 second because of the request timeout.
                time.sleep(1)
                return self.addEntry(base, target, check, retries-1)
            else:
                raise Exception("api call failed")
        return self.saveEntry(base, target, rates[target], check)        

    # New edge is (source, target, rate)
    def checkIndependenceFunc(self, source, target):
        """This should be set by caller, much like an observer."""
        raise NotImplementedError

    def printGraph(self):
        for i in range(len(self.graph)):
            print("row {}:".format(i))
            print(self.graph[i])

#### Quick Tests ####

# Just to check output.
def testMakeRequest():
    graph = CurrencyGraph()
    rates = graph.makeRequest(graph.base)
    assert(rates)

def testAddEntry():
    graph = CurrencyGraph()
    graph.setup()
    graph.addEntry(graph.currencyList[0], graph.currencyList[0])
    assert(graph.graph[0][0] == 1)

def testSetup():
    graph = CurrencyGraph()
    graph.setup()
    assert(len(graph.currencyList) > 0)
    assert(len(graph.graph) == len(graph.currencyList))

def runAllTests(testSuite: List[TestDefinition]):
    print('\033[0m' + "Running NoIdentityPolynomialPathChecker Tests")
    # testMakeRequest() # Only test when necessary to reduce number of requests
    testSetup()
    testAddEntry()
    print(Fore.GREEN + 'Run Completed')    

#### Execute ####
def main():
    runAllTests(defaultTestSuite)

if __name__=="__main__":
    main()