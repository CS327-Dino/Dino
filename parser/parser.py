from fractions import Fraction
from dataclasses import dataclass
from tokenizing.token_scanning import *
from datatypes.datatypes import *
from errors.error import *


@dataclass
class Parser:

    __error: DinoError

    def __init__(self, tokenlist, error) -> None:
        self.__tokens = tokenlist
        self.__current = 0
        self.__error = error

    def __ifstmt(self):
        self.__consume(TokenType.LEFT_PAREN, "'(' expected after if")
        __condition = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN,
                       "')' expected after condition end")
        __ifpart = Seq([])
        __elsepart = Seq([])
        while (not self.__match(TokenType.END, "")):
            __ifpart.things.append(self.__declare())
        self.__consume(TokenType.ELSE, "")
        while (not self.__match(TokenType.END, "")):
            __elsepart.things.append(self.__declare())
        return If(__condition, __ifpart, __elsepart)

    def __loop(self):
        self.__consume(TokenType.LEFT_PAREN, "'(' expected after if")
        __condition = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN,
                       "')' expected after condition end")
        __body = Seq([])
        while (not self.__match(TokenType.END, "")):
            __body.things.append(self.__declare())
        return Loop(__condition, __body)

    def __func(self):
        name = self.__consume(TokenType.IDENTIFIER,
                              "A function name was expected")
        parameters = []
        self.__consume(TokenType.LEFT_PAREN,
                       "Expected a '(' after the function name")
        if (self.__check(TokenType.RIGHT_PAREN) == False):
            while (self.__peek_next().ttype == TokenType.COMMA):
                if len(parameters) > 255:
                    self.__error.line = 1
                    self.__error.message = "Can't have more than 255 arguments"
                    self.__error.triggered = True
                parameters.append(self.__consume(
                    TokenType.IDENTIFIER, "Expected Parameter Name"))
                self.__advance()
        parameters.append(self.__consume(
            TokenType.IDENTIFIER, "Expected Parameter Name"))
        self.__consume(TokenType.RIGHT_PAREN,
                       "Expect ')' after parameters.")

        body = Seq([])
        while (not self.__match(TokenType.END, "")):
            body.things.append(self.__declare())
        return Function(name, parameters, body)

    def __expression(self):
        return self.__equality()

    def __equality(self):
        left_operand = self.__comparison()
        while self.__peek_next():
            match self.__tokens[self.__current].ttype:
                case op if op in [TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]:
                    self.__forward()
                    right_operand = self.__comparison()
                    left_operand = BinOp(left_operand, op, right_operand)
                case _:
                    break
        return left_operand

    def __comparison(self):
        left_operand = self.__add()
        while self.__peek_next():
            match self.__tokens[self.__current].ttype:
                case op if op in [TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL]:
                    self.__forward()
                    right_operand = self.__add()
                    left_operand = BinOp(left_operand, op, right_operand)
                case _:
                    break
        return left_operand

    def __add(self):

        left_operand = self.__multiply()
        while self.__peek_next():
            match self.__tokens[self.__current].ttype:
                case op if op in [TokenType.PLUS, TokenType.MINUS]:
                    self.__forward()
                    right_operand = self.__multiply()
                    left_operand = BinOp(left_operand, op, right_operand)
                case _:
                    break
        return left_operand

    def __multiply(self):
        left_operand = self.__unary()
        while self.__peek_next():
            match self.__tokens[self.__current].ttype:
                case op if op in [TokenType.STAR, TokenType.SLASH]:
                    self.__forward()
                    right_operand = self.__unary()
                    left_operand = BinOp(left_operand, op, right_operand)
                case _:
                    break
        return left_operand

    # def __exponential(self):
    #     left_operand = self.__unary()
    #     operands = [left_operand]
    #     while self.__peek_next():
    #         match self.__tokens[self.__current].ttype:
    #             case op if op in [TokenType.EXPO]:
    #                 self.__forward()
    #                 right_operand = self.__unary()
    #                 operands.append(right_operand)
    #             case _:
    #                 break
    #     val = operands[-1]
    #     operands = operands[::-1]
    #     for num in operands[1:]:
    #         val = BinOp(num, op, val)
    #     return val

    def __unary(self):
        while (self.__match(TokenType.BANG, TokenType.MINUS)):
            __op = self.__prev().text
            __right = self.__unary()
            return UnOp(__op, __right)
        return self.__call()

    def __call(self):
        expr = self.__primary()
        while (True):
            if self.__match(TokenType.LEFT_PAREN):
                expr = self.__finishCall(expr)
            else:
                break

        return expr

    def __finishCall(self, expr):
        arguments = []
        if (self.__check(TokenType.RIGHT_PAREN) == False):
            while (self.__peek_next().ttype == TokenType.COMMA):
                if len(arguments) > 255:
                    self.__error.line = 1
                    self.__error.message = "Can't have more than 255 arguments"
                    self.__error.triggered = True
                arguments.append(self.__expression())
                self.__advance()
        arguments.append(self.__expression())
        paren = self.__consume(TokenType.RIGHT_PAREN,
                               "Expect ')' after arguments.")

        return Call(expr, paren, arguments)

    def __primary(self):
        # print(self.__current)
        if (self.__match(TokenType.FALSE)):
            return BoolLiteral(False)
        if (self.__match(TokenType.TRUE)):
            return BoolLiteral(True)
        if (self.__match(TokenType.NULL)):
            return None
        if (self.__match(TokenType.NUMBER)):
            return NumLiteral(self.__prev().literal)
        if (self.__match(TokenType.STRING)):
            return StrLiteral(self.__prev().literal)
        if (self.__match(TokenType.IDENTIFIER)):
            return Identifier(self.__prev().text)
        if (self.__match(TokenType.LEFT_PAREN)):
            __expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN,
                           "')' expected after expression.")
            return __expr

    def __match(self, *types):
        for type in types:
            if (self.__check(type)):
                self.__advance()
                return True

        return False

    def __check(self, type):
        if (self.__atEnd()):
            return False
        return self.__peek().ttype == type

    def __atEnd(self):
        return self.__peek().ttype == TokenType.EOF

    def __peek(self):
        return self.__tokens[self.__current]

    def __prev(self):
        return self.__tokens[self.__current - 1]

    def __advance(self):
        if (not self.__atEnd()):
            self.__current = self.__current+1
            return self.__prev()

    def __consume(self, type, msg):
        if self.__check(type):
            return self.__advance()
        else:
            # print(msg)
            self.__error.line = 1
            self.__error.message = msg
            self.__error.triggered = True
            report_error(self.__error)
            exit()

    def __forward(self):
        if (self.__current >= len(self.__tokens)-1):
            return
        self.__current += 1

    def __peek_next(self):
        if (self.__current+1 < len(self.__tokens)-1):
            return self.__tokens[self.__current + 1]
        else:
            return False

    def __exprstmt(self):
        __expr = self.__expression()
        self.__consume(TokenType.SEMICOLON, "';' expected after expression")
        return __expr

    def __statement(self):
        if (self.__match(TokenType.IF)):
            return self.__ifstmt()
        if (self.__match(TokenType.LOOP)):
            return self.__loop()
        if (self.__match(TokenType.FUNC)):
            return self.__func()
        return self.__exprstmt()

    def __assign(self, var):
        # self.__consume(TokenType.ASSIGN, "Syntax Error")
        if (self.__match(TokenType.EQUAL)):
            __expr = self.__expression()

        self.__consume(TokenType.SEMICOLON, "';' expected after declaration")
        return Variable(var.text, __expr)

    def __declare(self):
        # print(self.__peek().text)
        if (self.__match(TokenType.ASSIGN)):
            return self.__assign(self.__consume(TokenType.IDENTIFIER, "Identifier expected"))
        if (self.__match(TokenType.IDENTIFIER)):
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
        while (not self.__atEnd()):
            __statements.things.append(self.__declare())
        return __statements
