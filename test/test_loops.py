# import unittest
# from evaluation.eval import *
# from errors.error import *
# from tokenizing.token_scanning import *
# from parser.parser import *
# from evaluation.eval import *
# from evaluation.resolve import *
# from unittest.mock import patch


# class TestLoops(unittest.TestCase):
#     @patch('builtins.print')
#     def test_loop_1(self, mock_print):
#         error = DinoError()
#         code = "assign i=1; loop(i<10) echo(i); i=i+1; end"
#         scanned_code = Scanner(code, error)
#         token_list = scanned_code.generate_tokens()
#         parser = Parser(token_list, error)
#         expression = parser.parse()
#         resolved = resolution(expression)
#         output = evaluate(resolved)
#         mock_print.assert_called_with('1\n2\n3\n4\n5\n6\n7\n8\n9')

#         # Showing what is in mock
#         import sys
#         sys.stdout.write(str( mock_print.call_args ) + '\n')
#         sys.stdout.write(str( mock_print.call_args_list ) + '\n')

# def greet(name):
#     print('Hello ', name)

# from unittest.mock import patch

# @patch('builtins.print')
# def test_greet(mock_print):
#     # The actual test
#     greet('John')
#     mock_print.assert_called_with('Hello ', 'John')
#     greet('Eric')
#     mock_print.assert_called_with('Hello ', 'Eric')

#     # Showing what is in mock
#     import sys
#     sys.stdout.write(str( mock_print.call_args ) + '\n')
#     sys.stdout.write(str( mock_print.call_args_list ) + '\n')