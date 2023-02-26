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

        expression = Parser(Scanner("2^3^2 + 3;", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[BinOp(left=BinOp(left=NumLiteral(value=2.0, line=1), op=TokenType.EXPONENT, right=BinOp(left=NumLiteral(value=3.0, line=1), op=TokenType.EXPONENT, right=NumLiteral(value=2.0, line=1), line=1), line=1), op=TokenType.PLUS, right=NumLiteral(value=3.0, line=1), line=1)]))

    def test_logical_operators(self):
        expression = Parser(Scanner("echo(2<3 and 1<4+2);", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Echo(expr=BinOp(left=BinOp(left=NumLiteral(2.0, line=1), op=TokenType.LESS, right=BinOp(left=NumLiteral(value=3.0, line=1), op=TokenType.AND, right=NumLiteral(1.0, line=1), line=1), line=1), op=TokenType.LESS, right=BinOp(left=NumLiteral(4.0, line=1), op=TokenType.PLUS, right=NumLiteral(2.0, line=1), line=1), line=1), line=1)]) )

        expression = Parser(Scanner("echo([2,3] or 0);", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Echo(expr=BinOp(left=ListLiteral(elements=[NumLiteral(2.0, line=1), NumLiteral(3.0, line=1)], length=2, line=1), op=TokenType.OR, right=NumLiteral(0.0, line=1), line=1), line=1)]))

    def test_if(self):
        expression = Parser(Scanner("if (2<=3) 2+3; end else 4+4; end", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[If(condition=BinOp(left=NumLiteral(value=2.0, line=1), op=TokenType.LESS_EQUAL, right=NumLiteral(value=3.0, line=1), line=1), ifPart=Seq(things=[BinOp(left=NumLiteral(value=2.0, line=1), op=TokenType.PLUS, right=NumLiteral(value=3.0, line=1), line=1)]), elsePart=Seq(things=[BinOp(left=NumLiteral(value=4.0, line=1), op=TokenType.PLUS, right=NumLiteral(value=4.0, line=1), line=1)]))]))
    
    def test_list(self):
        expression = Parser(Scanner("[2, [3, 4], true, [2^3*2], []];", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[ListLiteral(elements=[NumLiteral(value=2.0, line=1), ListLiteral(elements=[NumLiteral(value=3.0, line=1), NumLiteral(value=4.0, line=1)], length=2, line=1), BoolLiteral(value=True, line=1), ListLiteral(elements=[BinOp(left=BinOp(left=NumLiteral(value=2.0, line=1), op=TokenType.EXPONENT, right=NumLiteral(value=3.0, line=1), line=1), op=TokenType.STAR, right=NumLiteral(value=2.0, line=1), line=1)], length=1, line=1), ListLiteral(elements=[], length=0, line=1)], length=5, line=1)]))
    
    def test_emptylist(self):
        expression = Parser(Scanner("[];", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[ListLiteral(elements=[], length=0, line=1)]))

    def test_list_methods(self):
        expression = Parser(Scanner("assign a = [2, 6^2, 3, 4, 6>7];", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Assignment(var=Identifier(name='a', line=1), value=ListLiteral(elements=[NumLiteral(2.0, line=1), BinOp(left=NumLiteral(6.0, line=1), op=TokenType.EXPONENT, right=NumLiteral(2.0, line=1), line=1), NumLiteral(3.0, line=1), NumLiteral(4.0, line=1), BinOp(left=NumLiteral(6.0, line=1), op=TokenType.GREATER, right=NumLiteral(7.0, line=1), line=1)], length=5, line=1), line=1, declaration=True)]))

        expression = Parser(Scanner("echo(a.length);", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Echo(expr=BinOp(left=Identifier(name='a', line=1), op=TokenType.DOT, right=MethodLiteral(name='length', args=[], line=1), line=1), line=1)]))

        expression = Parser(Scanner("echo(a.head);", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Echo(expr=BinOp(left=Identifier(name='a', line=1), op=TokenType.DOT, right=MethodLiteral(name='head', args=[], line=1), line=1), line=1)]) )

        expression = Parser(Scanner("echo(a.tail);", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Echo(expr=BinOp(left=Identifier(name='a', line=1), op=TokenType.DOT, right=MethodLiteral(name='tail', args=[], line=1), line=1), line=1)]) )

        expression = Parser(Scanner("echo(a.slice(0,3));", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Echo(expr=BinOp(left=Identifier(name='a', line=1), op=TokenType.DOT, right=MethodLiteral(name='slice', args=[NumLiteral(0.0, line=1), NumLiteral(3.0, line=1)], line=1), line=1), line=1)]))

    def test_string_methods(self):
        expression = Parser(Scanner("echo(g.slice(2,5));", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Echo(expr=BinOp(left=Identifier(name='g', line=1), op=TokenType.DOT, right=MethodLiteral(name='slice', args=[NumLiteral(2.0, line=1), NumLiteral(5.0, line=1)], line=1), line=1), line=1)]) )

        expression = Parser(Scanner("echo(g.slice(2,5));", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Echo(expr=BinOp(left=Identifier(name='g', line=1), op=TokenType.DOT, right=MethodLiteral(name='slice', args=[NumLiteral(2.0, line=1), NumLiteral(5.0, line=1)], line=1), line=1), line=1)]) )

    