import sys, os

dirsToAdd = [
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))), '..'),
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    os.path.join(
        os.path.dirname(
            os.path.dirname(os.path.realpath(__file__))), '..', 'testing')
]

for directory in dirsToAdd:
    if directory not in sys.path:
        sys.path.insert(0, directory)