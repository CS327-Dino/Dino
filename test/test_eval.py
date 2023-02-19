import unittest
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

        self.assertEqual(evaluate(e5), 16)
        self.assertEqual(evaluate(e6), 3)
        self.assertEqual(evaluate(e7), 45)
        self.assertEqual(evaluate(e8), 9/2)
        self.assertEqual(evaluate(e9), 16/9)

        self.assertTrue(evaluate(e10))
        self.assertTrue(evaluate(e11))
        self.assertTrue(evaluate(e12))
        self.assertFalse(evaluate(UnOp(TokenType.BANG, BoolLiteral(True))))
		
        self.assertEqual(evaluate(UnOp("++", e4)), 6)

    def test_let_eval(self):
        a = Identifier("a")
        e1 = NumLiteral(5)
        e2 = BinOp(a, TokenType.PLUS, a)
        e = Let(a, e1, e2)
        self.assertEqual(evaluate(e), 10)

        e = Let(a, e1, Let(a, e2, e2))
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
