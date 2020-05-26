from colorama import Fore
import requests 
import numpy as np
import copy
from optimalSetPathChecker import OptimalSetPathChecker
from testUtilities import TestDefinition, defaultTestSuite
from typing import List

class CurrencyGraph():
    """Class that holds, builds and manipulates the graph with currency 
    conversion rates"""

    INFTY = 1000000
    NO_EDGE = -1
    DEBUG = False
    endPoint = "https://api.exchangeratesapi.io/latest?"
    
    def __init__(self):
        self.graph = []
        self.currencyList = []
        self.base = 'USD' # Default but can change
        np.set_printoptions(formatter={
            'float': lambda x: "{0:0.4f}".format(x)}, threshold=10000)
    
    def setup(self):
        """Setup graph with initial row of data from base currency"""
        rates = self.makeRequest(self.base)
        self.initialize(list(rates))
        self.addRow(self.base, rates)
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
        if (checkIndependence):
            isValid = self.checkIndependenceFunc(base, target, rate)
        if (isValid):
            self.graph[self.indexOf(base)][self.indexOf(target)] = rate    
        return isValid
    
    # Does not call addRates for efficiency.
    def addRow(self, base, rates, checkIndependence=False):
        for currency, rate in rates.items():
            isValid = True
            if (checkIndependence):
                isValid = self.checkIndependenceFunc(base, currency, rate)
            if (isValid):
                self.graph[self.indexOf(base)][self.indexOf(currency)] = rate
            else:
                return False
        return True

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
        # sending get request and saving the response as response object 
        r = requests.get(url = self.makeUrl(base, symbols))   
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
    
    def addEntry(self, base, target, check = False):
        rates = self.makeRequest(base, [target])
        return self.saveEntry(base, target, rates[target], check)        

    # New edge is (source, target, rate)
    def checkIndependenceFunc(self, source, target):
        """This should be set by caller, much like an observer."""
        raise NotImplementedError

    def printGraph(self):
        print(self.graph)

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
    testSetup()
    testAddEntry()
    print(Fore.GREEN + 'Run Completed')    

#### Execute ####
def main():
    runAllTests(defaultTestSuite)

if __name__=="__main__":
    main()