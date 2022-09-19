import os
import sys

class GenericInput:
    def __init__(self, files: list, stdin:bool ):
        self.files = files
        self.stdin = stdin

    def get_input(self):
        """ This gets generic input first from files(if any) then stdin(if on)"""
        for i in self.files:
            try:
                # with os.open(i,'r')as f:
                with open(i, 'r')as f:
                    for line in f:
                        yield line.rstrip()
            except IOError:
                assert False, "File {i} does not exist!".format(i)

        if self.stdin:
            for ln in sys.stdin:
                yield ln.rstrip()
