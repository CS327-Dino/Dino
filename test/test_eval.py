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

    def test_lambda(self):
        # lambda a = 2 in a + a end
        e1 = NumLiteral(2)
        e2 = Identifier("a")
        e3 = BinOp(e2, TokenType.PLUS, e2)
        e4 = Lambda(e2, e1, e3, 0)

        # lambda a = 2 in lambda b = 3 in a * b end end
        e5 = NumLiteral(5)
        e6 = Identifier("b")
        e7 = BinOp(e2, TokenType.STAR, e6)
        e8 = Lambda(e6, e5, e7, 0)
        e9 = Lambda(e2, e1, e8, 0)

        #lambda a=true in lambda b=false in a and b end end

        e10 = BoolLiteral(True)
        e11 = BoolLiteral(False)
        e12 = BinOp(e2, TokenType.AND, e6)
        e13 = Lambda(e6, e11, e12, 0)
        e14 = Lambda(e2, e10, e13, 0)


        self.assertEqual(evaluate(e4), 4)
        self.assertEqual(evaluate(e9), 10)
        self.assertFalse(evaluate(e14))

    def test_lists(self):
        e1 = ListLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(3)], 3, 1)
        e2 = ListLiteral([IntLiteral(1), IntLiteral(2), IntLiteral(3), IntLiteral(4)], 4, 1)
        e3 = ListLiteral([IntLiteral(1), IntLiteral(2), BoolLiteral(True), StrLiteral("Hello")], 4, 1)

        self.assertEqual(evaluate(e1).elements, [1, 2, 3])
        self.assertEqual(evaluate(e2).elements, [1, 2, 3, 4])
        self.assertEqual(evaluate(e3).elements, [1, 2, True, StrLiteral(value='Hello', line=0)])


    def test_methods(self):
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
    def test_functions(self):

        #func fn(n) if (n == 0) return 1; end else return 0; end end
        #evaluating fn(0) should return 1

        e1 = Identifier("n")
        e2 = BinOp(e1, TokenType.EQUAL_EQUAL, IntLiteral(0))
        e3 = Return(IntLiteral(1))
        e4 = Return(IntLiteral(0))
        e5 = If(e2, e3, e4)
        e6 = Function("fn", [e1], e5,1)
        evaluate(e6)
        print(e6)
        #Function call for fn(0)
        e7 = Call("fn", [IntLiteral(0)],1)
        evaluate(e7)
        # print("evaluated = " , evaluate(e7))

