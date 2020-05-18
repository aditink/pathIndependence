from baseOnlineChecker import BaseOnlineChecker

class PolynomialPathChecker(BaseOnlineChecker):
    """Path checker that returns a set for verification for online problem
    in time O(|V|.(|V|+|E|)))."""

    def __init__(self):
        super().__init__()

    def getPathsToCheck(self) ->  List[Tuple[List[int], List[int]]]:
        """Return the pairs of path whose equality implies path independence of 
        the new graph."""
        pass