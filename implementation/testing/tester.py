from PathCheckers import NoIdentityOptimalSetPathChecker, NoIdentityPolynomialPathChecker, OptimalSetPathChecker, PolynomialPathChecker

graph = [[-1, -1, 1, 1, -1], 
         [-1, -1, 1, 1, -1], 
         [1, -1, -1, -1, -1],
         [-1, -1, -1, -1, -1],
         [-1, -1, -1, -1, -1]]

# graph = [[-1, -1, 1],
#          [-1, -1, 1],
#          [1, -1, -1]]

poly = PolynomialPathChecker()

poly.setGraph(graph)
poly.setEdge(0, 1)
print("polynomial:\n" + str(poly.getPathsToCheck()) + "\n\n")

opti = OptimalSetPathChecker()

opti.setGraph(graph)
opti.setEdge(0, 1)
print("optimal:\n" + str(opti.getPathsToCheck()) + "\n\n")

polyid = NoIdentityPolynomialPathChecker()

polyid.setGraph(graph)
polyid.setEdge(0, 1)
print("polynomial noid:\n" + str(polyid.getPathsToCheck()) + "\n\n")

optiid = NoIdentityOptimalSetPathChecker()

optiid.setGraph(graph)
optiid.setEdge(0, 1)
print("optimal noid:\n" + str(optiid.getPathsToCheck()))