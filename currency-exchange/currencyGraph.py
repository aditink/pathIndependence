import requests 
import numpy as np
import copy
from optimalSetPathChecker import OptimalSetPathChecker

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
        np.set_printoptions(formatter={
            'float': lambda x: "{0:0.4f}".format(x)}, threshold=10000)
    
    def indexOf(self, currency):
        """Gets node in graph that a currency corresponds to."""
        return self.currencyList.index(currency)
    
