from fractions import Fraction
from dataclasses import dataclass
from tokenizing.token_scanning import *
from datatypes.datatypes import *

@dataclass
class Parser:
    __tokens : list
    __current : int = 0

    def __expression(self):
        return self.__equality()

    def __equality(self):
        __expr = self.__comparison()
        while(self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
            __op = self.__prev().text
            __right = self.__comparison()
            __expr = BinOp( __op, __expr, __right)

        return __expr

    def __comparison(self):
        __expr = self.__add()
        while(self.__match(TokenType.GREATER, TokenType.GREATER_EQUAL, 
        TokenType.LESS, TokenType.LESS_EQUAL)):
            __op = self.__prev().text
            __right = self.__add()
            __expr = BinOp( __op, __expr, __right)

        return __expr

    def __add(self):
        __expr = self.__multiply()
        while(self.__match(TokenType.MINUS, TokenType.PLUS)):
            __op = self.__prev().text
            __right = self.__multiply()
            __expr = BinOp( __op, __expr, __right)

        return __expr

    def __multiply(self):
        __expr = self.__unary()
        while(self.__match(TokenType.SLASH, TokenType.STAR)):
            __op = self.__prev().text
            __right = self.__unary()
            __expr = BinOp( __op, __expr, __right)

        return __expr

    def __unary(self):
        while(self.__match(TokenType.BANG, TokenType.MINUS)):
            __op = self.__prev().text
            __right = self.__unary()
            return UnOp(__op, __right)
        return self.__primary()

    def __primary(self):
        if(self.__match(TokenType.FALSE)):
            return BoolLiteral(False)
        if(self.__match(TokenType.TRUE)):
            return BoolLiteral(True)
        if(self.__match(TokenType.NULL)):
            return None
        if(self.__match(TokenType.NUMBER)):
            return NumLiteral(self.__prev().literal)
        if(self.__match(TokenType.STRING)):
            return StrLiteral(self.__prev().literal)
        if(self.__match(TokenType.IDENTIFIER)):
            return Identifier(self.__prev().text)
        if(self.__match(TokenType.LEFT_PAREN)):
            __expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN, "')' expected after expression.")
            return __expr

    def __match(self, *types):
        for type in types:
            if(self.__check(type)):
                self.__advance()
                return True

        return False

    def __check(self, type):
        if(self.__atEnd()):
            return False
        return self.__peek().ttype == type

    def __atEnd(self):
        return self.__peek().ttype == TokenType.EOF

    def __peek(self):
        return self.__tokens[self.__current]

    def __prev(self):
        return self.__tokens[self.__current -1]

    def __advance(self):
        if( not self.__atEnd()):
            self.__current =  self.__current+1
            return self.__prev() 

    def __consume(self, type, msg):
        if self.__check(type):
            return self.__advance()
        else:
            print(msg)

    def parse(self):
        parsedExpr = Seq([])
        while self.__peek().ttype != TokenType.EOF:
            parsedExpr.things.append(self.__expression())
            if self.__peek().ttype == TokenType.SEMICOLON:
                self.__advance()
            else:
                raise Exception("Expected ';' after expression")
        return parsedExpr

        

