import unittest
from evaluation.eval import *
from errors.error import *
from tokenizing.token_scanning import *
from parser.parser import *
from evaluation.eval import *
from evaluation.resolve import *


class TestFunctions(unittest.TestCase):
    def test_assign(self):
        error = DinoError()
        code = "assign a=3; a;"
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        self.assertEqual(output, 3)