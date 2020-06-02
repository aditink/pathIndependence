The code in this folder is intended to apply the path independence algorithm to currency exchange data in order to find discrepancies (up to a set error
tolerance).

### API Used
First google result for free currency exchange rate api:
https://exchangeratesapi.io/

## Main Components:
Interface that defines contract for path checkers: iPathChecker.py
Various implementations of path checkers.
testUtilities to define test functionality and constants.
Currency graph and related functionality: currencyGraph.py.
Main.py creates a currency graph and does checks.
Have stopped maintaining the noIdentity version of path Checkers so they may not
work correctly in the latest commits.

### Data extraction and graph building
Can be found in currencyGraph.py.

### Comparable Path finding algorithm implementation
The interface is defined in iPathChecker.
OptimalSetPathChecker and PolynomialPathChecker are the two relevant 
implementations, with most common functionality written in baseOnlineChecker.

### Equality checking
The oracle is defined in main.py, constructed using the checkers.

### Testing
For quick one-time check and printout of results use tester.py.
While checking edge cases add a TestDefinition defining input and expected 
results in testUtils.py, add the new testDefinition to the list of tests 
("test suite") that is currently being run, and then call the main method of the
checker that you are testing. This way the case can be made a part of the 
repeatable testing suite for future modifications.

# Dependencies
written for python 3.
The things I needed to install:
Requests library: pip install requests
numpy
colorama