from parser.parser import *
from tokenizing.token_scanning import *
from datatypes.datatypes import *
from errors.error import*
import unittest

class TestParser(unittest.TestCase):
    def test_operators(self):
        expression = Parser(Scanner("10==23;", DinoError()).generate_tokens()).parse()
        self.assertEqual(expression,Seq(things=[BinOp(left=NumLiteral(Fraction(10, 1)), op=TokenType.EQUAL_EQUAL, right=NumLiteral(Fraction(23, 1)))]))

        expression = Parser(Scanner("2*3+1<= 2/3;", DinoError()).generate_tokens()).parse()
        self.assertEqual(expression, Seq(things=[BinOp(left=BinOp(left=BinOp(left=NumLiteral(Fraction(2, 1)), op=TokenType.STAR, right=NumLiteral(Fraction(3, 1))), op=TokenType.PLUS, right=NumLiteral(Fraction(1, 1))), op=TokenType.LESS_EQUAL, right=BinOp(left=NumLiteral(Fraction(2, 1)), op=TokenType.SLASH, right=NumLiteral(Fraction(3, 1))))]) )
    def test_if(self):
        expression = Parser(Scanner("if (2<=3) 2+3; end else 4+4; end", DinoError()).generate_tokens()).parse()
        self.assertEqual(expression, Seq(things=[If(condition=BinOp(left=NumLiteral(Fraction(2, 1)), op=TokenType.LESS_EQUAL, right=NumLiteral(Fraction(3, 1))), ifPart=Seq(things=[BinOp(NumLiteral(Fraction(2, 1)), op=TokenType.PLUS, right=NumLiteral(Fraction(3, 1)))]), elsePart=Seq([BinOp(left=NumLiteral(Fraction(4, 1)), op=TokenType.PLUS, right=NumLiteral(Fraction(4, 1)))]))]))


        