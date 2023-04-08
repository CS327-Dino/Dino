from parser.parser import *
from tokenizing.token_scanning import *
from datatypes.datatypes import *
from errors.error import*
from evaluation.bytecode import *
import unittest

class TestByte(unittest.TestCase):
    def test_bytecode(self):
        expression = Parser(Scanner("2*3+1<= 2/3;", DinoError()).generate_tokens(), DinoError()).parse()
        print(expression)
        code = Bytecode()
        code.bytecode_generator(expression)
        print(code.code)

    def test_if(self):
        expression = Parser(Scanner("if(2*3+1<= 2/3) 2+1; end else 6*8; end", DinoError()).generate_tokens(), DinoError()).parse()
        print(expression)
        code = Bytecode()
        code.bytecode_generator(expression)
        print(code.code)