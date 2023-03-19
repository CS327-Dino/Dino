import unittest
from errors.error import *
from tokenizing.token_scanning import *
from parser.parser import *
from evaluation.eval import *
from evaluation.resolve import *
from evaluation.typecheck import *


class TestType(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(LiteralType.INT, typecheck(IntLiteral(5), Scope(), DinoError()))
        self.assertEqual(LiteralType.FLOAT, typecheck(NumLiteral(5.5), Scope(), DinoError()))
        self.assertEqual(LiteralType.BOOL, typecheck(BoolLiteral(True), Scope(), DinoError()))
        self.assertEqual(LiteralType.FLOAT, typecheck(BinOp(IntLiteral(5), TokenType.PLUS, NumLiteral(5.5)), Scope(), DinoError()))
    
    def test_BinOP(self):
        error = DinoError()
        typecheck(resolution(Parser(Scanner("2+3;", DinoError()).generate_tokens(), DinoError()).parse()), Scope(), error)
        self.assertFalse(error.triggered)
        typecheck(resolution(Parser(Scanner("2+3.0;", DinoError()).generate_tokens(), DinoError()).parse()), Scope(), error)
        self.assertFalse(error.triggered)
        typecheck(resolution(Parser(Scanner("2.0+3;", DinoError()).generate_tokens(), DinoError()).parse()), Scope(), error)
        self.assertFalse(error.triggered)
        typecheck(resolution(Parser(Scanner("2.0+3.0;", DinoError()).generate_tokens(), DinoError()).parse()), Scope(), error)
        self.assertFalse(error.triggered)
        error = DinoError()
        typecheck(resolution(Parser(Scanner("2+true;", DinoError()).generate_tokens(), DinoError()).parse()), Scope(), error)
        self.assertTrue(error.triggered)
        
    def test_const(self):
        error = DinoError()
        typecheck(resolution(Parser(Scanner("assign a=5;a=3;", DinoError()).generate_tokens(), DinoError()).parse(), Scope()), Scope(), error)
        self.assertFalse(error.triggered)
        typecheck(resolution(Parser(Scanner("const a=5;a=3;", DinoError()).generate_tokens(), DinoError()).parse(), Scope()), Scope(), error)
        self.assertTrue(error.triggered)

    def test_if(self):
        error = DinoError()
        typecheck(resolution(Parser(Scanner("if (2 >= 3) 2+3; end else 4+4; end", DinoError()).generate_tokens(), DinoError()).parse()), Scope(), error)
        self.assertFalse(error.triggered)
        typecheck(resolution(Parser(Scanner("if (2) 2+3; end else 4+4; end", DinoError()).generate_tokens(), DinoError()).parse()), Scope(), error)
        self.assertTrue(error.triggered)
        error = DinoError()
        typecheck(resolution(Parser(Scanner("if (2 >= 3) 2+3; end else 4+4.0; end", DinoError()).generate_tokens(), DinoError()).parse()), Scope(), error)
        self.assertTrue(error.triggered)
