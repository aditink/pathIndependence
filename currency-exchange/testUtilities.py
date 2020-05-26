from colorama import Fore
import traceback

NO_EDGE = -1

# Constants for default test.
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

expected_solution_no_identity = [
    ([2, 3, 6, 7, 2], [2, 3, 6, 7, 2, 3, 6, 7, 2]),
    ([3, 6, 7, 2, 3], [3, 6, 7, 2, 3, 6, 7, 2, 3]),
    ([6, 7, 2, 3, 6], [6, 7, 2, 3, 6, 7, 2, 3, 6]),
    ([7, 2, 3, 6, 7], [7, 2, 3, 6, 7, 2, 3, 6, 7]),
    ([1, 2, 3, 6, 7, 2], [1, 2]),
    ([3, 6, 7, 2, 3, 4], [3, 4]),
    ([7, 2, 3, 6, 7, 2], [7, 2]),
    ([3, 6, 7, 2, 3, 6], [3, 6]),
    ([6, 7, 2, 3, 6, 7], [6, 7])
]

# This method is from stack overflow.
def compareLists(expected, actual):
    actual = list(actual)   # make a mutable copy
    try:
        for elem in expected:
            actual.remove(elem)
    except ValueError:
        print(Fore.RED + "Missing element")
        traceback.print_stack()
        return False
    if actual:
        print(Fore.RED + "Extra element(s) {}".format(actual))
        traceback.print_stack()
        return False 
    return not actual

def actualListIsSuperset(expected, actual):
    actual = list(actual)   # make a mutable copy
    currentElem = None
    try:
        for elem in expected:
            currentElem = elem
            actual.remove(elem)
    except ValueError:
        print(Fore.RED + "Missing element {}".format(currentElem))
        traceback.print_stack()
        return False
    return True

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

def assertActualIsSuperset(expected, actual):
    try:
        if isinstance(expected, list):
            assert(actualListIsSuperset(expected, actual))
        else:
            raise Exception("no handling for checking superset for {}"
            .format(expected))
    except:
        print(Fore.RED + "Error")
        print("Expected: {}".format(expected))
        print("Actual: {}".format(actual))
        traceback.print_stack()

class TestDefinition():
    """Define all the constant necessary for a single test case."""

    def __init__(
        self, 
        test_graph, 
        test_s, 
        test_t, 
        expected_fwd_graph = [],
        expected_bkd_graph = [],
        expected_paths_to_s = [],
        expected_paths_from_t = [],
        expected_solution = [],
        expected_solution_no_identity = [],
        source_cycles = [],
        sink_cycles = []):
        self.NO_EDGE = NO_EDGE
        self.test_graph = test_graph
        self.test_s = test_s
        self.test_t = test_t
        self.test_new_edge = (test_s, test_t)
        self.expected_fwd_graph = expected_fwd_graph
        self.expected_bkd_graph = expected_bkd_graph
        self.expected_paths_to_s = expected_paths_to_s
        self.expected_paths_from_t = expected_paths_from_t
        self.expected_solution = expected_solution
        self.expected_solution_no_identity = expected_solution_no_identity
        self.expected_source_cycles = source_cycles
        self.expected_sink_cycles = sink_cycles

# Test Definitions

defaultTestDefinition = TestDefinition(
    test_graph = test_graph,
    test_s = test_s,
    test_t = test_t,
    expected_fwd_graph = expected_fwd_graph,
    expected_bkd_graph = expected_bkd_graph,
    expected_paths_to_s = expected_paths_to_s,
    expected_paths_from_t = expected_paths_from_t,
    expected_solution = expected_solution,
    expected_solution_no_identity = expected_solution_no_identity,
    source_cycles = [],
    sink_cycles = [])

testCaseOne = TestDefinition(
    test_graph = [
        [NO_EDGE, NO_EDGE,       1,       1],
        [NO_EDGE, NO_EDGE,       1,       1],
        [1,       NO_EDGE, NO_EDGE, NO_EDGE],
        [NO_EDGE, NO_EDGE, NO_EDGE, NO_EDGE]
    ],
    test_s = 0,
    test_t = 1,
    expected_fwd_graph = [
        [2, 3],
        [2, 3],
        [0],
        []
    ],
    expected_bkd_graph = [
        [2],
        [],
        [0, 1],
        [0, 1]
    ],
    expected_paths_to_s =  {
        0 : [0],
        1 : [1, 2, 0],
        2 : [2, 0],
    },
    expected_paths_from_t = {
        0 : [1, 2, 0],
        1 : [1],
        2 : [1, 2],
        3 : [1, 3]
    },
    # TODO write order insensitive comparison for tuples.
        # Note: 0 -> 3 implied by 0 -> 2. 
        # [0, 1, 2] = [0, 2] => [0, 1, 2, 0, 3] = [0, 2, 0, 3].
        # From existing graph [0, 2, 0, 3] = [0, 3] and [1, 2, 0, 3] = [1, 3].
        # Put together, [0, 1, 3] = [0, 3].
    expected_solution = [
        ([0, 1, 2], [0, 2]), # Actually any of 2 -> 2, 0 -> 2, 0 -> 0 or 2 -> 0.
        ([1, 2, 0, 1], [1])
    ],
    # TODO add missing entries.
    expected_solution_no_identity = [
        ([0, 1, 2], [0, 2]),
        ([1, 2, 0, 1], [1, 2, 0, 1, 2, 0, 1]),
        ([0, 1], [0, 2, 0, 1])
    ],
    source_cycles = [
        ([0, 1], [0, 2, 0, 1])
    ],
    sink_cycles = []
)

# Test suites

defaultTestSuite = [
    defaultTestDefinition,
    testCaseOne
    ]