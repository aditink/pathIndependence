"""Convenience script to call the runAllTests methods of all files we care about
at once."""

from currencyGraph.currencyGraph import runAllTests as currencyGraphTests
from pathCheckers.optimalSetPathChecker import runAllTests as optimalCheckerTests
from pathCheckers.polynomialPathChecker import runAllTests as polynomialCheckerTests
from pathCheckers.baseOnlineChecker import runAllTests as baseOnlineCheckerTests
from pathCheckers.naiveChecker import runAllTests as naiveCheckerTests
from pathCheckers.twoFlipChecker import runAllTests as twoFlipTests

objectsToRun = [baseOnlineCheckerTests,
                polynomialCheckerTests,
                optimalCheckerTests,
                currencyGraphTests,
                naiveCheckerTests,
                twoFlipTests]

for tests in objectsToRun:
    try:
        tests()
    except:
        continue
