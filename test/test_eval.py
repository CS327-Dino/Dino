import unittest
from parser.parser import *
from tokenizing.token_scanning import *
from datatypes.datatypes import *
from evaluation.eval import *


class TestEval(unittest.TestCase):
    def test_eval(self):
        e1 = NumLiteral(2)
        e2 = NumLiteral(7)
        e3 = NumLiteral(9)
        e4 = NumLiteral(5)
        e5 = BinOp(e2, TokenType.PLUS, e3)
        e6 = BinOp(e4, TokenType.MINUS, e1)
        e7 = BinOp(e4, TokenType.STAR, e3)
        e8 = BinOp(e3, TokenType.SLASH, e1)
        e9 = BinOp(e5, TokenType.SLASH, e3)

        e10 = BinOp(e4, TokenType.LESS, e3)
        e11 = BinOp(e2, TokenType.BANG_EQUAL, e1)
        e12 = BinOp(e2, TokenType.EQUAL_EQUAL, NumLiteral(7))
        e13 = BinOp(NumLiteral(7), TokenType.SLASH, NumLiteral(0))

        self.assertEqual(evaluate(e5), 16)
        self.assertEqual(evaluate(e6), 3)
        self.assertEqual(evaluate(e7), 45)
        self.assertEqual(evaluate(e8), 9/2)
        self.assertEqual(evaluate(e9), 16/9)

        self.assertTrue(evaluate(e10))
        self.assertTrue(evaluate(e11))
        self.assertTrue(evaluate(e12))
        self.assertFalse(evaluate(UnOp(TokenType.BANG, BoolLiteral(True))))
		
        self.assertEqual(evaluate(UnOp(TokenType.INCREMENT, e4)), 6)
        with self.assertRaises(SystemExit):
            evaluate(e13)

    def test_let_eval(self):
        a = Identifier("a")
        e1 = NumLiteral(5)
        e2 = BinOp(a, TokenType.PLUS, a)
        e = Lambda(a, e1, e2)
        self.assertEqual(evaluate(e), 10)

        e = Lambda(a, e1, Lambda(a, e2, e2))
        self.assertEqual(evaluate(e), 20)

    def test_If_eval(self):
        e1 = BinOp(NumLiteral(10), TokenType.GREATER,NumLiteral(7))
        e2 = NumLiteral(20)
        e3 = NumLiteral(30)

        e = If(e1, e2, e3)
        self.assertEqual(evaluate(e), 20)

        e1 = BinOp(NumLiteral(5), TokenType.GREATER, NumLiteral(7))
        e = If(e1, e2, e3)
        self.assertEqual(evaluate(e), 30)

    def test_conditional_eval(self):
        e1 = BinOp(BinOp(IntLiteral(10), TokenType.SLASH, IntLiteral(2)), TokenType.EQUAL_EQUAL, right=IntLiteral(5))
        e2 = BinOp(BinOp(IntLiteral(10), TokenType.MOD, IntLiteral(2)), TokenType.EQUAL_EQUAL, right=IntLiteral(0))

        self.assertTrue(evaluate(BinOp(e1, TokenType.AND, e2)))
        self.assertTrue(evaluate(BinOp(e1, TokenType.OR, e2)))

        e2 = BinOp(BinOp(IntLiteral(10), TokenType.MOD, IntLiteral(3)), TokenType.EQUAL_EQUAL, right=IntLiteral(0))
        self.assertFalse(evaluate(BinOp(e1, TokenType.AND, e2)))
        self.assertTrue(evaluate(BinOp(e1, TokenType.OR, e2)))

    def test_bitwise(self):
        e1 = BinOp(IntLiteral(10), TokenType.BIT_AND, IntLiteral(2))
        e2 = BinOp(IntLiteral(10), TokenType.BIT_OR, IntLiteral(2))

        self.assertEqual(evaluate(e1), 2)
        self.assertEqual(evaluate(e2), 10)