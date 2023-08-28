#!/usr/bin/python3.11
import sys


class GenericInput:
    def __init__(self, files: list, stdin: bool):
        self.files = files
        self.stdin = stdin

    def get_input(self):
        """ This gets generic input first from files (if any) then stdin(if on)"""
        for i in self.files:
            try:
                with open(i, 'r') as f:
                    for line in f:
                        yield line.rstrip()
            except IOError:
                raise Exception("File {i} does not exist!".format(i=i))

        if self.stdin:
            for ln in sys.stdin:
                yield ln.rstrip()
