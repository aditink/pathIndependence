NO_EDGE = -1

test_graph = [
    [NO_EDGE,       1, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE],
    [NO_EDGE, NO_EDGE,       1, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE],
    [NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE],
    [NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE,       1, NO_EDGE,       1, NO_EDGE],
    [NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE,       1, NO_EDGE, NO_EDGE],
    [NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE],
    [NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE,       1],
    [NO_EDGE, NO_EDGE,       1, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE]]
test_s = 2
test_t = 3
test_new_edge = (2, 3)

expected_fwd_graph = [
    [1],
    [2],
    [],
    [4, 6],
    [5],
    [],
    [7],
    [2]
]

expected_bkd_graph = [
    [],
    [0],
    [1, 7],
    [],
    [3],
    [4],
    [3],
    [6]
]

expected_paths_to_s = {
    0 : [0, 1, 2],
    1 : [1, 2],
    2 : [2],
    3 : [3, 6, 7, 2],
    6 : [6, 7, 2],
    7 : [7, 2]
}

expected_paths_from_t = {
    2 : [3, 6, 7, 2],
    3 : [3],
    4 : [3, 4],
    5 : [3, 4, 5],
    6 : [3, 6],
    7 : [3, 6, 7]
}

expected_solution = [
    ([2, 3, 6, 7, 2], [2]),
    ([3, 6, 7, 2, 3], [3]),
    ([6, 7, 2, 3, 6], [6]),
    ([7, 2, 3, 6, 7], [7])
]

# This method is from stack overflow.
def compareLists(expected, actual):
    actual = list(actual)   # make a mutable copy
    try:
        for elem in expected:
            actual.remove(elem)
    except ValueError:
        return False
    return not actual

def assertEqual(expected, actual):
    try:
        if isinstance(expected, list):
            assert(compareLists(expected, actual))
        else:
            assert(expected == actual)
    except:
        print(Fore.RED + "Error")
        print("Expected: {}".format(expected))
        print("Actual: {}".format(actual))
        traceback.print_stack()