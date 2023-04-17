import unittest
from evaluation.eval import *
from errors.error import *
from tokenizing.token_scanning import *
from parser.parser import *
from evaluation.eval import *
from evaluation.resolve import *


class TestMisc(unittest.TestCase):
    def test_echo_1(self):
        error = DinoError()
        code = "echo(1);"
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)
        ans = ""
        for i in output:
            ans = ans + str(i)
        # Should return 1 as that is what is being echoed
        self.assertEqual(ans, '1')

    def test_echo_2(self):
        error = DinoError()
        code = 'echo("Hello World!");'
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)
        ans = ""
        for i in output:
            ans = ans + str(i)
        # Should return "Hello World!" as that is what is being echoed
        self.assertEqual(ans, "Hello World!")

    def test_echo_3(self):
        error = DinoError()
        code = "echo(1 + 2);"
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)
        ans = ""
        for i in output:
            ans = ans + str(i)
        # Should return 3 as 1 + 2 = 3
        self.assertEqual(ans, '3')

    def test_echo_4(self):
        error = DinoError()
        code = 'echo("Hello" + " World!");'
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)
        ans = ""
        for i in output:
            ans = ans + str(i)
        # Should return "Hello World!" as that is what is being echoed
        self.assertEqual(ans, "Hello World!")

    def test_echo_5(self):
        error = DinoError()
        code = 'assign i = 1; echo(i, " This is test of multiple arguments");'
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)
        ans = ""
        for i in output:
            print(i)
            ans = ans + str(i)
        self.assertEqual(ans, '1 This is test of multiple arguments')

    def test_echo_6(self):
        error = DinoError()
        code = 'assign j = 1; echo(j+1, ": This is test of multiple arguments ", 2);'
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)
        ans = ""
        for i in output:
            ans = ans + str(i)
        self.assertEqual(ans, '2: This is test of multiple arguments 2')

    def test_echo_7(self):
        error = DinoError()
        code = 'assign k = 1; echo(k, ": Test of multiple arguments, ", k+1, ": Another Test");'
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)
        ans = ""
        for i in output:
            ans = ans + str(i)
        self.assertEqual(ans, '1: Test of multiple arguments, 2: Another Test')

    def test_echo_8(self):
        error = DinoError()
        code = 'echo(k, ": Test of multiple arguments, ", k+1, ": Another Test", k+2, ": Final Test");'
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)
        ans = ""
        for i in output:
            ans = ans + str(i)
        self.assertEqual(ans, '1: Test of multiple arguments, 2: Another Test3: Final Test')
