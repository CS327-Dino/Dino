import unittest
from evaluation.eval import *
from errors.error import *
from tokenizing.token_scanning import *
from parser.parser import *
from evaluation.eval import *
from evaluation.resolve import *

class TestParser(unittest.TestCase):

    
    
    def test_lambda_0(self):
        error = DinoError()
        code = "lambda a=12 in a+a end"
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)
        
        #Should output 12+12=24
        self.assertEqual(output, 24)
    def test_lambda_1(self):
        error = DinoError()
        code = "lambda a= lambda b = 2 in b+ b*b end in a+a end"
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)
        
        #Should output 12
        self.assertEqual(output, 12)
    def test_lambda_2(self):
        error = DinoError()
        code = "lambda a= lambda a = 2 in a+ a*a end in a+a end"
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        # Should return 12 as a= 2+2*2 in a+a i.e., a=6 in a+a. 

        self.assertEqual(output, 12)

    def test_lambda_3(self):
        error = DinoError()
        code = "lambda a = 12 in lambda b = 7 in b*b+a end end"
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        #7*7+12=61
        self.assertEqual(output, 61)
    def test_lambda_4(self):
        error = DinoError()
        code = "lambda a = true in lambda b = false in a and b end end"
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)

        self.assertEqual(output, False)
    def test_lambda_5(self):
        error = DinoError()
        code = "lambda a=2 in a*(lambda b=3 in lambda a=10 in a+b end end) end"
        scanned_code = Scanner(code, error)
        token_list = scanned_code.generate_tokens()
        parser = Parser(token_list, error)
        expression = parser.parse()
        resolved = resolution(expression)
        output = evaluate(resolved)
        print("Output = ",output)
        self.assertEqual(output, 26)

        

    