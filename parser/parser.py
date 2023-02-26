from fractions import Fraction
from dataclasses import dataclass
from tokenizing.token_scanning import *
from datatypes.datatypes import *
from evaluation.eval import *


@dataclass
class Parser:
    def __init__(self, tokenlist, error) -> None:
        self.__tokens = tokenlist
        self.__current = 0
        self.__parseError = error
        self.__lambdaflag=False
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
        line = self.__tokens[self.__current - 1].line
        parameters = []
        self.__consume(TokenType.LEFT_PAREN,
                       "Expected a '(' after the function name")
        if (self.__check(TokenType.RIGHT_PAREN) == False):
            while (self.__peek_next().ttype == TokenType.COMMA):
                if len(parameters) > 255:
                    self.__parseError.line = 1
                    self.__parseError.message = "Can't have more than 255 arguments"
                    self.__parseError.triggered = True
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
        return Function(name, parameters, body, line)
    def __lambda(self):
        '''To parse lambda expressions'''
        name = self.__peek().text
        self.__consume(TokenType.IDENTIFIER,
                              "A variable name was expected")
        self.__consume(TokenType.EQUAL, "Expected Equal Sign")
        __expression_1=Seq([])
        __expression_2=Seq([])
        while(not self.__match(TokenType.END)):
            if(self.__peek().ttype==TokenType.IN):
                self.__consume(TokenType.IN, "invalid in statement")
                break
            __expression_1.things.append(self.__exprstmt())
            if(self.__peek().ttype==TokenType.END):
                self.__consume(TokenType.END,"Expected end after the statement")
                return Assignment(Identifier(name), __expression_1,self.__tokens[self.__current - 1].line , True)
        while(not self.__match(TokenType.END)):
            if(self.__peek().ttype==TokenType.END):
                self.__consume(TokenType.END,"Expected end after the statement")
                break
            __expression_2.things.append(self.__exprstmt())
        return Lambda(Identifier(name),__expression_1,__expression_2)
                
    def __list(self):
        __elements = []
        __length = 0
        # print(self.__tokens[self.__current].text)
        if self.__tokens[self.__current].ttype == TokenType.RIGHT_BRACKET:
            self.__consume(TokenType.RIGHT_BRACKET,
                           "']' expected at the end of a list")
            return ListLiteral(__elements, __length, self.__prev().line)
        while self.__peek_next():

            __elements.append(self.__expression())
            __length += 1
            match self.__tokens[self.__current].ttype:
                case TokenType.COMMA:
                    self.__consume(TokenType.COMMA,
                                   "',' expected as delimiter")
                case TokenType.RIGHT_BRACKET:
                    self.__consume(TokenType.RIGHT_BRACKET,
                                   "']' expected at the end of a list")
                    break
                case _:
                    break
        return ListLiteral(__elements, __length, self.__prev().line)

    # def __methods_list(self, identifier):
    #     self.__consume(TokenType.DOT, "Expected '.' to call methods of the list")
    #     __method = self.__expression()
    #     __iden = evaluate(identifier)
    #     print(type(__iden))
    #     if (__method.name== "length"):
    #         return NumLiteral(len(__iden), self.__tokens[self.__current].line)
    #     # if (__method.name == "head"):
    #     #     return NumLiteral(__iden[0], self.__tokens[self.__current].line)

    def __expression(self) -> AST:
        if (self.__match(TokenType.LAMBDA)):
            if(self.__lambdaflag):
                return self.__lambda()
            else:
                self.__lambdaflag=True
                return_value= self.__lambda()
                self.__lambdaflag=False
                return return_value
        return self.__simpleAssignment()

    def __simpleAssignment(self):
        __left = self.__equality()
        if self.__match(TokenType.EQUAL):
            if __left == None or not isinstance(__left, Identifier):
                self.__parseError.error(
                    self.__tokens[self.__current - 1].line, "Invalid assignment target")
            else:
                __right = self.__expression()
                return Assignment(__left, __right, self.__tokens[self.__current - 1].line)
        return __left

    def __equality(self):
        left_operand = self.__comparison()
        while self.__peek_next():
            match self.__tokens[self.__current].ttype:
                case op if op in [TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]:
                    self.__forward()
                    right_operand = self.__comparison()
                    left_operand = BinOp(
                        left_operand, op, right_operand, self.__tokens[self.__current - 1].line)
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
                    left_operand = BinOp(
                        left_operand, op, right_operand, self.__tokens[self.__current - 1].line)
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
                    left_operand = BinOp(
                        left_operand, op, right_operand, self.__tokens[self.__current - 1].line)
                case _:
                    break
        return left_operand

    def __multiply(self):
        left_operand = self.__exponential()
        while self.__peek_next():
            match self.__tokens[self.__current].ttype:
                case op if op in [TokenType.STAR, TokenType.SLASH]:
                    self.__forward()
                    right_operand = self.__exponential()
                    left_operand = BinOp(
                        left_operand, op, right_operand, self.__tokens[self.__current - 1].line)
                case _:
                    break
        return left_operand

    def __exponential(self):
        left_operand = self.__unary()
        operands = [left_operand]
        while self.__peek_next():
            if self.__tokens[self.__current].ttype == TokenType.EXPONENT:
                self.__forward()
                right_operand = self.__unary()
                operands.append(right_operand)
            else:
                break
        val = operands[-1]
        operands = operands[::-1]
        for num in operands[1:]:
            val = BinOp(num, TokenType.EXPONENT, val, self.__prev().line)
        return val

    def __unary(self):
        while (self.__match(TokenType.BANG, TokenType.MINUS)):
            __op = self.__prev().text
            __right = self.__unary()
            return UnOp(__op, __right, self.__tokens[self.__current - 1].line)
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
                    self.__parseError.line = 1
                    self.__parseError.message = "Can't have more than 255 arguments"
                    self.__parseError.triggered = True
                arguments.append(self.__expression())
                self.__advance()
            arguments.append(self.__expression())
        paren = self.__consume(TokenType.RIGHT_PAREN,
                               "Expect ')' after arguments.")

        return Call(expr, paren, arguments)

    def __primary(self):
        # print(self.__current)
        if (self.__match(TokenType.FALSE)):
            return BoolLiteral(False, self.__tokens[self.__current - 1].line)
        if (self.__match(TokenType.TRUE)):
            return BoolLiteral(True, self.__tokens[self.__current - 1].line)
        if (self.__match(TokenType.NULL)):
            return None
        if (self.__match(TokenType.NUMBER)):
            return NumLiteral(self.__prev().literal, self.__tokens[self.__current - 1].line)
        if (self.__match(TokenType.STRING)):
            return StrLiteral(self.__prev().literal, self.__tokens[self.__current - 1].line)
        if (self.__match(TokenType.IDENTIFIER)):
            # if self.__tokens[self.__current].ttype == TokenType.DOT:
            #     __i = evaluate(Identifier(self.__prev().text, self.__tokens[self.__current - 1].line))
            #     if (type(__i) == list):
            #         return self.__methods_list(Identifier(self.__prev().text, self.__tokens[self.__current - 1].line))
            return Identifier(self.__prev().text, self.__tokens[self.__current - 1].line)
        if (self.__match(TokenType.LEFT_PAREN)):
            __expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN,
                           "')' expected after expression.")
            return __expr
        if (self.__match(TokenType.LEFT_BRACKET)):
            return self.__list()
        self.__parseError.message = "Syntax Error: Expected something after '" + \
            self.__prev().text + "'"
        self.__parseError.line = self.__prev().line
        report_error(self.__parseError)
        self.__advance()

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
            self.__parseError.message = "Syntax Error:" + msg
            self.__parseError.line = self.__prev().line
            report_error(self.__parseError)
            self.__advance()
            # print(msg)
            # exit()

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
        if(self.__lambdaflag):
            return __expr
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
            self.__consume(TokenType.SEMICOLON,
                           "';' expected after declaration")
            return Assignment(Identifier(var.text, self.__tokens[self.__current - 1].line), __expr, self.__tokens[self.__current - 1].line, True)
        else:
            self.__parseError.message = "Syntax Error: Expected '=' after variable declaration"
            self.__parseError.line = self.__prev().line
            report_error(self.__parseError)

    def __declare(self):
        # print(self.__peek().text)
        if (self.__match(TokenType.ASSIGN)):
            return self.__assign(self.__consume(TokenType.IDENTIFIER, "Identifier expected"))
        # if(self.__match(TokenType.IDENTIFIER)):
        #     __var = self.__prev()
        #     return  self.__assign(__var)
        if (self.__match(TokenType.ECHO)):
            self.__consume(TokenType.LEFT_PAREN, "'(' expected")
            __expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN, "')' expected")
            self.__consume(TokenType.SEMICOLON,
                           "';' expected after declaration")
            return Echo(__expr, self.__tokens[self.__current - 1].line)
        return self.__statement()

    def parse(self):
        __statements = Seq([])
        while (not self.__atEnd()):
            expr = self.__declare()
            if (expr):
                __statements.things.append(expr)
        return __statements
