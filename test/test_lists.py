import unittest
from parser.parser import *
from tokenizing.token_scanning import *
from datatypes.datatypes import *
from evaluation.eval import *
from evaluation.resolve import *

class TestLists(unittest.TestCase): 
    def test_lists(self):
        '''
        Test that lists are created correctly
        '''
        e1 = ListLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(3)], 3, 1)
        e2 = ListLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(3), IntLiteral(4)], 4, 1)
        e3 = ListLiteral([IntLiteral(1), IntLiteral(2), BoolLiteral(True), StrLiteral("Hello")], 4, 1)

        self.assertEqual(evaluate(e1).elements, [1, 2, 3])
        self.assertEqual(evaluate(e2).elements, [1, 2, 3, 4])
        self.assertEqual(evaluate(e3).elements, [1, 2, True, StrLiteral(value='Hello', line=0)])


    def test_methods(self):
        '''
        Test that methods are evaluated correctly
        '''
        e1 = ListLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(3)], 3, 1)
        e2 = ListLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(3), IntLiteral(4)], 4, 1)
        e3 = MethodLiteral("length", [], 1)
        e4 = MethodLiteral("head", [], 1)
        e5 = MethodLiteral("tail", [], 1)
        e6 = MethodLiteral("slice", [IntLiteral(1), IntLiteral(3)], 1)
        e11 = MethodLiteral("at", [IntLiteral(2)], 1)
        # e6 = MethodLiteral("add", [IntLiteral(7)], 1)

        e7 = BinOp(e1, TokenType.DOT, e3)
        e8 = BinOp(e1, TokenType.DOT, e4)
        e9 = BinOp(e2, TokenType.DOT, e5)
        e10 = BinOp(e2, TokenType.DOT, e6)
        e12 = BinOp(e2, TokenType.DOT, e11)

        self.assertEqual(evaluate(e7), 3)
        self.assertEqual(evaluate(e8), 1)
        self.assertEqual(evaluate(e9).elements, [2, 3, 4])
        self.assertEqual(evaluate(e10).elements, [2, 3])
        self.assertEqual(evaluate(e12), 3)

    def test_list_references(self):
        '''
        Test that lists are passed by reference
        '''
        error = DinoError()
        env = Scope()
        resolution_scope = Scope()
        expressions = ["assign a = [1,2,3];" , "assign b = a;", "a;", "b;"] 
        outputs = []
        for expr in expressions:
            expression = Parser(Scanner(expr, error).generate_tokens(), error).parse()
            resolved = resolution(expression, resolution_scope)
            outputs.append(evaluate(resolved, env))
        self.assertEqual(id(outputs[2].elements), id(outputs[3].elements))

    def test_list_references_methods(self):
        '''
        Test that using methods on lists and assigning changes the reference
        '''
        error = DinoError()
        env = Scope()
        resolution_scope = Scope()
        expressions = ["assign a = [1,2,3];" , "assign b = a.tail;", "a;", "b;", "assign z = a.copy;", "z;"] 
        outputs = []
        for expr in expressions:
            expression = Parser(Scanner(expr, error).generate_tokens(), error).parse()
            resolved = resolution(expression, resolution_scope)
            outputs.append(evaluate(resolved, env))
        self.assertNotEqual(id(outputs[2].elements), id(outputs[3].elements))
        self.assertNotEqual(id(outputs[2].elements), id(outputs[5].elements))

    
