from noIdentityOptimalSetPathChecker import NoIdentityOptimalSetPathChecker
from noIdentityPolynomialPathChecker import NoIdentityPolynomialPathChecker
from optimalSetPathChecker import OptimalSetPathChecker
from PolynomialPathChecker import PolynomialPathChecker

graph = [[-1, -1, -1], 
         [-1, -1, -1], 
         [-1, -1, -1]]

poly = PolynomialPathChecker()

poly.setGraph(graph)
poly.setEdge(0, 1)
print(poly.getPathsToCheck())