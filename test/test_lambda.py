from parser.parser import *
from tokenizing.token_scanning import *
from datatypes.datatypes import *
from errors.error import*
import unittest
class TestParser(unittest.TestCase):
    
    def test_lambda(self):
        expression = Parser(Scanner('lambda a=12 in a+a end;', DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression,Seq(things=[Lambda(var=Identifier(name='a', line=0, isconst=False, uid=2), e1=Seq(things=[IntLiteral(value=12, line=1)]), e2=Seq(things=[BinOp(left=Identifier(name='a', line=1, isconst=False, uid=0), op=TokenType.PLUS, right=Identifier(name='a', line=1, isconst=False, uid=1), line=1)]), line=0)]))

        expression = Parser(Scanner('lambda a=12 end;', DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression,Seq(things=[Assignment(var=Identifier(name='a', line=0, isconst=False, uid=3), value=Seq(things=[IntLiteral(value=12, line=1)]), line=1, declaration=True)]))

        
        expression = Parser(Scanner('lambda v1=true in lambda v2=false in v1 and v2 end end;', DinoError()).generate_tokens(), DinoError()).parse()
        self.assertEqual(expression,Seq(things=[Lambda(var=Identifier(name='v1', line=0, isconst=False, uid=3), e1=Seq(things=[BoolLiteral(value=True, line=1)]), e2=Seq(things=[Lambda(var=Identifier(name='v2', line=0, isconst=False, uid=2), e1=Seq(things=[BoolLiteral(value=False, line=1)]), e2=Seq(things=[BinOp(left=Identifier(name='v1', line=1, isconst=False, uid=0), op=TokenType.AND, right=Identifier(name='v2', line=1, isconst=False, uid=1), line=1)]), line=0)]), line=0)]))
        

    