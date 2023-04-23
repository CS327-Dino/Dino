from parser.parser import *
from tokenizing.token_scanning import *
from datatypes.datatypes import *
from errors.error import*
import unittest

class TestParser(unittest.TestCase):
    def test_arithmetic_operators(self):
        expression = Parser(Scanner("10==23;", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(
            expression, Seq(things=[BinOp(left=IntLiteral(value=10, line=1), op=TokenType.EQUAL_EQUAL, right=IntLiteral(value=23, line=1), line=1)]))

        expression = Parser(Scanner("2*3+1<= 2/3;", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(
            expression, Seq(things=[BinOp(left=BinOp(left=BinOp(left=IntLiteral(value=2, line=1), op=TokenType.STAR, right=IntLiteral(value=3, line=1), line=1), op=TokenType.PLUS, right=IntLiteral(value=1, line=1), line=1), op=TokenType.LESS_EQUAL, right=BinOp(left=IntLiteral(value=2, line=1), op=TokenType.SLASH, right=IntLiteral(value=3, line=1), line=1), line=1)]))

        expression = Parser(Scanner("2^3^2 + 3;", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(
            expression, Seq(things=[BinOp(left=BinOp(left=IntLiteral(value=2, line=1), op=TokenType.EXPONENT, right=BinOp(left=IntLiteral(value=3, line=1), op=TokenType.EXPONENT, right=IntLiteral(value=2, line=1), line=1), line=1), op=TokenType.PLUS, right=IntLiteral(value=3, line=1), line=1)]))
        
    def test_unary_operators(self):
        expression = Parser(Scanner("!2;", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[UnOp(op=TokenType.BANG, right=IntLiteral(value=2, line=1), line=1)]))

        expression = Parser(Scanner("++2;", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[UnOp(op=TokenType.INCREMENT, right=IntLiteral(value=2, line=1), line=1)]))

        expression = Parser(Scanner("-2;", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[UnOp(op=TokenType.MINUS, right=IntLiteral(value=2, line=1), line=1)]))

    def test_bitwise_operators(self):
        expression = Parser(Scanner("2&3;", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[BinOp(left=IntLiteral(value=2, line=1), op=TokenType.BIT_AND, right=IntLiteral(value=3, line=1), line=1)]))

        expression = Parser(Scanner("4|5;", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[BinOp(left=IntLiteral(value=4, line=1), op=TokenType.BIT_OR, right=IntLiteral(value=5, line=1), line=1)]))


    def test_logical_operators(self):
        expression = Parser(Scanner("echo(2<3 and 1<4+2);", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Echo(expr=[BinOp(left=BinOp(left=IntLiteral(value=2, line=1), op=TokenType.LESS, right=BinOp(left=IntLiteral(value=3, line=1), op=TokenType.AND, right=IntLiteral(value=1, line=1), line=1), line=1), op=TokenType.LESS, right=BinOp(left=IntLiteral(value=4, line=1), op=TokenType.PLUS, right=IntLiteral(value=2, line=1), line=1), line=1)], line=1)]))

    #     expression = Parser(Scanner("echo([2,3] or 0);", DinoError()).generate_tokens(), DinoError()).parse()
    #     self.assertEqual(expression, Seq(things=[Echo(expr=BinOp(left=ListLiteral(elements=[IntLiteral(value=2, line=1), IntLiteral(value=3, line=1)], length=2, line=1), op=TokenType.OR, right=IntLiteral(value=0, line=1), line=1), line=1)]))

    def test_if(self):
        expression = Parser(Scanner("if (2<=3) 2+3; end else 4+4; end", DinoError()).generate_tokens(), DinoError()).parse()
        print(expression)
        self.assertEqual(
            expression, Seq(things=[If(condition=BinOp(left=IntLiteral(value=2, line=1), op=TokenType.LESS_EQUAL, right=IntLiteral(value=3, line=1), line=1), ifPart=Seq(things=[BinOp(left=IntLiteral(value=2, line=1), op=TokenType.PLUS, right=IntLiteral(value=3, line=1), line=1)]), elsePart=Seq(things=[BinOp(left=IntLiteral(value=4, line=1), op=TokenType.PLUS, right=IntLiteral(value=4, line=1), line=1)]))]))

    
    # def test_loop(self):
    #     expression = Parser(Scanner("loop(i<5) i = i + 1; echo(i); end", DinoError()).generate_tokens(), DinoError()).parse()
    #     self.assertEqual(
    #         expression, Seq(things=[Loop(condition=BinOp(left=Identifier(name='i', line=1, isconst=False, uid=12), op=TokenType.LESS, right=IntLiteral(value=5, line=1), line=1), body=Seq(things=[Assignment(var=Identifier(name='i', line=1, isconst=False, uid=13), value=BinOp(left=Identifier(name='i', line=1, isconst=False, uid=14), op=TokenType.PLUS, right=IntLiteral(value=1, line=1), line=1), line=1, declaration=False), Echo(expr=Identifier(name='i', line=1, isconst=False, uid=15), line=1)]))]))
    
    def test_list(self):
        expression = Parser(Scanner("[2, [3, 4], true, [2^3*2], []];", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(
            expression, Seq(things=[ListLiteral(elements=[IntLiteral(value=2, line=1), ListLiteral(elements=[IntLiteral(value=3, line=1), IntLiteral(value=4, line=1)], length=2, line=1), BoolLiteral(value=True, line=1), ListLiteral(elements=[BinOp(left=BinOp(left=IntLiteral(value=2, line=1), op=TokenType.EXPONENT, right=IntLiteral(value=3, line=1), line=1), op=TokenType.STAR, right=IntLiteral(value=2, line=1), line=1)], length=1, line=1), ListLiteral(elements=[], length=0, line=1)], length=5, line=1)]))
    
    def test_emptylist(self):
        expression = Parser(Scanner("[];", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[ListLiteral(elements=[], length=0, line=1)]))

    def test_assign(self):
            expression = Parser(Scanner("assign var = 1.0;", DinoError()).generate_tokens(), DinoError()).parse()
            self.assertEqual(expression, Seq(things=[Assignment(var=Identifier(name='var', line=1, isconst=False, uid=0), value=NumLiteral(value=1.0, line=1), line=1, declaration=True)]))

    def test_input(self):
        expression = Parser(Scanner('assign input_var = capture("Enter Text");', DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Assignment(var=Identifier(name='input_var', line=1, isconst=False, uid=1), value=Capture(msg='Enter Text', line=1), line=1, declaration=True)]))

        expression = Parser(Scanner('assign input_var = capture("Enter Number") + 3;', DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Assignment(var=Identifier(name='input_var', line=1, isconst=False, uid=2), value=BinOp(left=Capture(msg='Enter Number', line=1), op=TokenType.PLUS, right=IntLiteral(value=3, line=1), line=1), line=1, declaration=True)]))
    
    def test_output(self):
        expression = Parser(Scanner('echo("Hello World");', DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Echo(expr=[StrLiteral(value='Hello World', line=1)], line=1)]))

    def test_exit(self):
        expression = Parser(Scanner('abort();', DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Abort(msg='Program Aborted', line=0)]))


    def test_list_methods(self):
        expression = Parser(Scanner("assign a = [2, 6^2, 3, 4, 6>7];", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Assignment(var=Identifier(name='a', line=1, isconst=False, uid=3), value=ListLiteral(elements=[IntLiteral(value=2, line=1), BinOp(left=IntLiteral(value=6, line=1), op=TokenType.EXPONENT, right=IntLiteral(value=2, line=1), line=1), IntLiteral(value=3, line=1), IntLiteral(value=4, line=1), BinOp(left=IntLiteral(value=6, line=1), op=TokenType.GREATER, right=IntLiteral(value=7, line=1), line=1)], length=5, line=1), line=1, declaration=True)]))

        expression = Parser(Scanner("echo(b.length);", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Echo(expr=[BinOp(left=Identifier(name='b', line=1, isconst=False, uid=4), op=TokenType.DOT, right=MethodLiteral(name='length', args=[], line=1), line=1)], line=1)]))

        expression = Parser(Scanner("echo(c.head);", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Echo(expr=[BinOp(left=Identifier(name='c', line=1, isconst=False, uid=6), op=TokenType.DOT, right=MethodLiteral(name='head', args=[], line=1), line=1)], line=1)]))

        expression = Parser(Scanner("echo(d.tail);", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Echo(expr=[BinOp(left=Identifier(name='d', line=1, isconst=False, uid=8), op=TokenType.DOT, right=MethodLiteral(name='tail', args=[], line=1), line=1)], line=1)]) )

        expression = Parser(Scanner("echo(e.slice(0,3));", DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression, Seq(things=[Echo(expr=[BinOp(left=Identifier(name='e', line=1, isconst=False, uid=10), op=TokenType.DOT, right=MethodLiteral(name='slice', args=[IntLiteral(value=0, line=1), IntLiteral(value=3, line=1)], line=1), line=1)], line=1)]))

    # def test_string_methods(self):
    #     expression = Parser(Scanner('assign g = "hello!! This is our compiler";', DinoError()).generate_tokens(), DinoError()).parse()
    #     self.assertEqual(expression, Seq(things=[Assignment(var=Identifier(name='g', line=1, isconst=False, uid=16), value=StrLiteral(value='hello!! This is our compiler', line=1), line=1, declaration=True)]))

    #     expression = Parser(Scanner("echo(g.slice(2,5));", DinoError()).generate_tokens(), DinoError()).parse()
    #     self.assertEqual(expression, Seq(things=[Echo(expr=BinOp(left=Identifier(name='g', line=1, isconst=False, uid=17), op=TokenType.DOT, right=MethodLiteral(name='slice', args=[IntLiteral(value=2, line=1), IntLiteral(value=5, line=1)], line=1), line=1), line=1)]))

    #     expression = Parser(Scanner('echo("Hello" + " World");', DinoError()).generate_tokens(), DinoError()).parse()
    #     self.assertEqual(expression, Seq(things=[Echo(expr=BinOp(left=StrLiteral(value='Hello', line=1), op=TokenType.PLUS, right=StrLiteral(value=' World', line=1), line=1), line=1)]))
    
    