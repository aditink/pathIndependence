def addVectors(v1, v2):
    """Add vectors in GF_2."""
    return [(a+b)%2 for a, b in zip(v1, v2)]
