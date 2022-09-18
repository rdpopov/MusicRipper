import os
import sys

class GenericInput:
    def __init__(self, files: list, stdin:bool , socket_object: SocketInput):
        self.files = files
        self.stdin = stdin

    def get_input(self):
        # Handle the files
        for i in self.files:
            try:
                with os.open(i,'r') as f:
                    # Generator expression ??
                    yield (l for l in f)
                input
            except IOError:
                assert False, "File {i} does not exist!".format(i)

        if self.stdin:
            for ln in sys.stdin:
                yield ln.rstrip()
