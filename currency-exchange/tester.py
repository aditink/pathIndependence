from noIdentityOptimalSetPathChecker import NoIdentityOptimalSetPathChecker
from noIdentityPolynomialPathChecker import NoIdentityPolynomialPathChecker
from optimalSetPathChecker import OptimalSetPathChecker
from PolynomialPathChecker import PolynomialPathChecker

graph = [[-1, -1, -1], 
         [1, -1, -1], 
         [-1, -1, -1]]

poly = PolynomialPathChecker()

poly.setGraph(graph)
poly.setEdge(0, 1)
print("polynomial:\n" + str(poly.getPathsToCheck()))

opti = OptimalSetPathChecker()

opti.setGraph(graph)
opti.setEdge(0, 1)
print("optimal:\n" + str(opti.getPathsToCheck()))

polyid = NoIdentityPolynomialPathChecker()

polyid.setGraph(graph)
polyid.setEdge(0, 1)
print("polynomial noid:\n" + str(polyid.getPathsToCheck()))

optiid = NoIdentityOptimalSetPathChecker()

optiid.setGraph(graph)
optiid.setEdge(0, 1)
print("optimal noid:\n" + str(optiid.getPathsToCheck()))