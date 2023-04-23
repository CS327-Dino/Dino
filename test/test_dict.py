import unittest
from evaluation.eval import *
from errors.error import *
from tokenizing.token_scanning import *
from parser.parser import *
from evaluation.eval import *
from evaluation.resolve import *


class TestDict(unittest.TestCase):
    def test_dict_1(self):
        error = DinoError()
        code = "assign dict = {1: 2, 3: 4}; dict[1];"
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression, Scope())
        output = evaluate(resolved, Scope())
        # Should return 2 as that is what is being echoed
        self.assertEqual(output, 2)

    def test_dict_2(self):
        error = DinoError()
        code = "assign a = 4;assign dict = {1: a, 3: 4}; dict[1];"
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression, Scope())
        output = evaluate(resolved, Scope())
        # Should return 2 as that is what is being echoed
        self.assertEqual(output, 4)

    def test_dict_3(self):
        error = DinoError()
        code = "assign a = 4;assign dict = {1: a, 3: 4};a = 5; dict[1];"
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression, Scope())
        output = evaluate(resolved, Scope())
        # Should return 2 as that is what is being echoed
        self.assertEqual(output, 5)

    def test_dict_4(self):
        error = DinoError()
        code = 'assign a = 4;assign dict = {"a": a, 3: 4};a = 5; dict["a"];'
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression, Scope())
        output = evaluate(resolved, Scope())
        # Should return 2 as that is what is being echoed
        self.assertEqual(output, 5)

    def test_dict_5(self):
        error = DinoError()
        code = 'assign a = 4;assign dict = {"a": 1, 3: 4}; dict["a"] = a; a = 5; dict["a"]'
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression, Scope())
        output = evaluate(resolved, Scope())
        # Should return 2 as that is what is being echoed
        self.assertEqual(output, 5)