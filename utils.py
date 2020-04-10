class Utils:
    def __init__(self, verbosity):
        self.verbosity = verbosity

    def printv(self, verbosity, output):
        if (verbosity <= self.verbosity):
            print(output)
