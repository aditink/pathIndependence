"""Convenience script to call the runAllTests methods of all files we care about
at once."""

from currencyGraph.currencyGraph import runAllTests as currencyGraphTests
from pathCheckers.optimalSetPathChecker import runAllTests as optimalCheckerTests
from pathCheckers.polynomialPathChecker import runAllTests as polynomialCheckerTests
from pathCheckers.baseOnlineChecker import runAllTests as baseOnlineCheckerTests

objectsToRun = [baseOnlineCheckerTests,
                polynomialCheckerTests,
                optimalCheckerTests,
                currencyGraphTests]

for tests in objectsToRun:
    try:
        tests()
    except:
        continue
