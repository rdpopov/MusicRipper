#!/usr/bin/env python
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from cmd_line_util import GenericInput

class TestInputWrapper(unittest.TestCase):
    def setUp(self):
        self.test_contents = [str(a) for a in range(10)]
        self.test_input_file = "test_input"
        with open(self.test_input_file, "w") as f:
            for i in self.test_contents:
                f.write(i+"\n")

    def test_file_input(self):
        inputter = GenericInput([self.test_input_file], False)
        for contr, test in zip(self.test_contents, inputter.get_input()):
            # print(contr, test)
            self.assertEqual(contr, test, "Read incorrect value contr{} != test{}\n".format(contr, test))

    def test_multiple_file_input(self):
        pass

    def test_multiple_file_input_stdin(self):
        pass

    def test_stdin(self):
        pass

    def tear_stdin_input_stdin_false(self):
        pass

if __name__ == '__main__':
    unittest.main()
