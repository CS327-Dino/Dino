from fractions import Fraction
from dataclasses import dataclass
from tokenizing.token_scanning import *
from datatypes.datatypes import *

@dataclass
class Parser:
    __tokens : list
    __current : int = 0


    def __ifstmt(self):
        self.__consume(TokenType.LEFT_PAREN, "'(' expected after if")
        __condition = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN, "')' expected after condition end")
        __ifpart = Seq([])
        __elsepart = Seq([])
        while(not self.__match(TokenType.END, "")):
            __ifpart.things.append(self.__declare())
        self.__consume(TokenType.ELSE, "")
        while(not self.__match(TokenType.END, "")):
            __elsepart.things.append(self.__declare())
        return If(__condition, __ifpart, __elsepart)

    def __loop(self):
        self.__consume(TokenType.LEFT_PAREN, "'(' expected after if")
        __condition = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN, "')' expected after condition end")
        __body = Seq([])
        while(not self.__match(TokenType.END, "")):
            __body.things.append(self.__declare())
        return Loop(__condition, __body)

    def __expression(self):
        return self.__equality()

    def __equality(self):
        __expr = self.__comparison()
        while(self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
            __op = self.__prev().text
            __right = self.__comparison()
            __expr = BinOp( __expr, __op, __right)

        return __expr

    def __comparison(self):
        __expr = self.__add()
        while(self.__match(TokenType.GREATER, TokenType.GREATER_EQUAL, 
        TokenType.LESS, TokenType.LESS_EQUAL)):
            __op = self.__prev().text
            __right = self.__add()
            __expr = BinOp( __expr, __op, __right)

        return __expr

    def __add(self):
        __expr = self.__multiply()
        while(self.__match(TokenType.MINUS, TokenType.PLUS)):
            __op = self.__prev().text
            __right = self.__multiply()
            __expr = BinOp( __expr, __op, __right)

        return __expr

    def __multiply(self):
        __expr = self.__unary()
        while(self.__match(TokenType.SLASH, TokenType.STAR)):
            __op = self.__prev().text
            __right = self.__unary()
            __expr = BinOp( __expr, __op, __right)

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
            exit()

    def __exprstmt(self):
        __expr = self.__expression()
        self.__consume(TokenType.SEMICOLON, "';' expected after expression")
        return __expr

    def __statement(self):
        if(self.__match(TokenType.IF)):
            return self.__ifstmt()
        if(self.__match(TokenType.LOOP)):
            return self.__loop()
        return self.__exprstmt()

    def __assign(self, var):
        # self.__consume(TokenType.ASSIGN, "Syntax Error")
        if(self.__match(TokenType.EQUAL)):
            __expr = self.__expression()

        self.__consume(TokenType.SEMICOLON, "';' expected after declaration")
        return Variable(var.text, __expr)

    def __declare(self):
        # print(self.__peek().text)
        if(self.__match(TokenType.ASSIGN)):
            return self.__assign(self.__consume(TokenType.IDENTIFIER, "Identifier expected"))
        if(self.__match(TokenType.IDENTIFIER)):
            __var = self.__prev()
            return  self.__assign(__var)
        if(self.__match(TokenType.ECHO)):
            self.__consume(TokenType.LEFT_PAREN, "'(' expected")
            __expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN, "')' expected")
            self.__consume(TokenType.SEMICOLON, "';' expected after declaration")
            return Echo(__expr)
        return self.__statement()

    def parse(self):
        __statements = Seq([])
        while(not self.__atEnd()):
            __statements.things.append(self.__declare())
        return __statements


        

