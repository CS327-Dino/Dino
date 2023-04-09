from parser.parser import *
from tokenizing.token_scanning import *
from datatypes.datatypes import *
from errors.error import *
from evaluation.bytecode import *
from evaluation.resolve import *
import unittest

class TestByte(unittest.TestCase):
    def test_bytecode(self):
        expression = Parser(Scanner("2*3+1 <= 2/3;", DinoError()).generate_tokens(), DinoError()).parse()
        code = Bytecode()
        code.bytecode_generator(expression)
        self.assertEqual(VM(code.code).run(), False)

    def test_if(self):
        expression = Parser(Scanner("if(2*3+1<= 2/3) 2+1; end else 6*8; end", DinoError()).generate_tokens(), DinoError()).parse()
        code = Bytecode()
        code.bytecode_generator(expression)
        self.assertEqual(VM(code.code).run(), 48)

    def test_assign(self):
        expression = resolution(Parser(Scanner("assign a = 10; a + 25;", DinoError()).generate_tokens(), DinoError()).parse(), Scope())
        bytecode = Bytecode()
        bytecode.bytecode_generator(expression)
        vm = VM(bytecode.code) 
        output = vm.run() 
        assert output == 35 
    
    def test_file(self): 
        expression = resolution(Parser(Scanner("assign a = 10; a + 25;assign b = 2; a / b; if(2*b+1<= b-a) 2+1; end else assign b = 12; 6*8 + b; end", DinoError()).generate_tokens(), DinoError()).parse(), Scope())
        bytecode = Bytecode()
        bytecode.bytecode_generator(expression) 
        vm = VM(bytecode.code) 
        output = vm.run() 
        self.assertEqual(output, 60)