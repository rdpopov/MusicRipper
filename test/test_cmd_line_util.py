#!/usr/bin/env python
import unittest
from unittest.mock import patch
import sys
import os
from io import StringIO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from cmd_line_util import GenericInput

mock_input = StringIO(initial_value='1\n2\n3\n4\n5\n6\n7\n8\n9\n10')

class TestInputWrapper(unittest.TestCase):
    def setUp(self):
        self.test_contents = [str(a) for a in range(1,11)]
        self.test_input_file = "./test_input"
        with open(self.test_input_file, "w") as f:
            for i in self.test_contents:
                f.write(i+"\n")

    def test_file_input(self):
        inputter = GenericInput([self.test_input_file], False)
        for contr, test in zip(self.test_contents, inputter.get_input()):
            self.assertEqual(contr, test, "Read incorrect value contr{} != test{}\n".format(contr, test))

    def test_multiple_file_input(self):
        inputter = GenericInput([self.test_input_file, self.test_input_file], False)
        for contr, test in zip(self.test_contents * 2, inputter.get_input()):
            self.assertEqual(contr, test, "Read incorrect value contr{} != test{}\n".format(contr, test))

    @patch('sys.stdin', mock_input)
    def test_stdin(self):
        inputter = GenericInput([], True)
        for contr, test in zip(self.test_contents, inputter.get_input()):
            self.assertEqual(contr, test, "Read incorrect value contr{} != test{}\n".format(contr, test))

    @patch('sys.stdin', mock_input)
    def test_multiple_file_input_stdin(self):
        inputter = GenericInput([self.test_input_file, self.test_input_file], True)
        for contr, test in zip(self.test_contents * 3, inputter.get_input()):
            self.assertEqual(contr, test, "Read incorrect value contr{} != test{}\n".format(contr, test))

    @patch('sys.stdin', mock_input)
    def test_stdin_input_stdin_false(self):
        inputter = GenericInput([self.test_input_file, self.test_input_file], False)
        for contr, test in zip(self.test_contents * 2, inputter.get_input()):
            self.assertEqual(contr, test, "Read incorrect value contr{} != test{}\n".format(contr, test))

    def tearDown(self):
        os.remove(self.test_input_file)
        pass

if __name__ == '__main__':
    unittest.main()
