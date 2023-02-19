from parser.parser import *
from tokenizing.token_scanning import *
from datatypes.datatypes import *
from errors.error import*
import unittest

class TestParser(unittest.TestCase):
    def test_operators(self):
        expression = Parser(Scanner("10==23;", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[BinOp(left=NumLiteral(value=10.0, line=1), op=TokenType.EQUAL_EQUAL, right=NumLiteral(value=23.0, line=1), line=1)]))

        expression = Parser(Scanner("2*3+1<= 2/3;", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[BinOp(left=BinOp(left=BinOp(left=NumLiteral(value=2.0, line=1), op=TokenType.STAR, right=NumLiteral(value=3.0, line=1), line=1), op=TokenType.PLUS, right=NumLiteral(value=1.0, line=1), line=1), op=TokenType.LESS_EQUAL, right=BinOp(left=NumLiteral(value=2.0, line=1), op=TokenType.SLASH, right=NumLiteral(value=3.0, line=1), line=1), line=1)]) )
    def test_if(self):
        expression = Parser(Scanner("if (2<=3) 2+3; end else 4+4; end", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[If(condition=BinOp(left=NumLiteral(value=2.0, line=1), op=TokenType.LESS_EQUAL, right=NumLiteral(value=3.0, line=1), line=1), ifPart=Seq(things=[BinOp(left=NumLiteral(value=2.0, line=1), op=TokenType.PLUS, right=NumLiteral(value=3.0, line=1), line=1)]), elsePart=Seq(things=[BinOp(left=NumLiteral(value=4.0, line=1), op=TokenType.PLUS, right=NumLiteral(value=4.0, line=1), line=1)]))]))