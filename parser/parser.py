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
        self.__lambdaflag = False

    def __ifstmt(self):
        self.__consume(TokenType.LEFT_PAREN, "'(' expected after if")
        __condition = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN,
                       "')' expected after condition end")
        __ifpart = Seq([])
        __elsepart = Seq([])
        while (not self.__match(TokenType.END, "")):
            __ifpart.things.append(self.__declare())
        if (self.__match(TokenType.ELSE, "")):
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
        self.__consume(TokenType.IDENTIFIER, "A function name was expected")
        name = self.__prev().text
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
                var = self.__consume(TokenType.IDENTIFIER,
                                     "Expected Parameter Name")
                if var != None:
                    parameters.append(Identifier(var.text, var.line))
                self.__advance()

            var = self.__consume(TokenType.IDENTIFIER,
                                 "Expected Parameter Name")
            if var != None:
                parameters.append(Identifier(var.text, var.line))
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

        body = Seq([])
        while (not self.__match(TokenType.END, "")):
            body.things.append(self.__declare())
        return Function(Identifier(name, line), parameters, body, line)

    def __lambda(self):
        '''To parse lambda expressions'''
        name = self.__peek().text
        self.__consume(TokenType.IDENTIFIER,
                       "A variable name was expected")
        self.__consume(TokenType.EQUAL, "Expected Equal Sign")
        __expression_1 = Seq([])
        __expression_2 = Seq([])
        while (not self.__match(TokenType.END)):
            if (self.__peek().ttype == TokenType.IN):
                self.__consume(TokenType.IN, "invalid in statement")
                break
            __expression_1.things.append(self.__exprstmt())
            if (self.__peek().ttype == TokenType.END):
                self.__consume(
                    TokenType.END, "Expected end after the statement")
                return Assignment(Identifier(name), __expression_1, self.__tokens[self.__current - 1].line, True)
        while (not self.__match(TokenType.END)):
            if (self.__peek().ttype == TokenType.END):
                self.__consume(
                    TokenType.END, "Expected end after the statement")
                break
            __expression_2.things.append(self.__exprstmt())
        return Lambda(Identifier(name), __expression_1, __expression_2)

    def __list(self):
        '''
        parses the list and adds it to the AST as the ListLiteral datatype of Dino
        '''
        __elements = []
        __length = 0
        # print(self.__tokens[self.__current].text)
        if self.__tokens[self.__current].ttype == TokenType.RIGHT_BRACKET:
            self.__consume(TokenType.RIGHT_BRACKET,
                           "']' expected at the end of a list")
            return ListLiteral(__elements, __length, self.__prev().line)
        while self.__peek_next().ttype != TokenType.EOF:

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

    def __dict(self):
        '''
        Parses the dictionary and adds it to the AST as the DictLiteral datatype of Dino
        '''
        __elements = {}
        __length = 0
        if self.__tokens[self.__current].ttype == TokenType.RIGHT_BRACE:
            self.__consume(TokenType.RIGHT_BRACE,
                           "'}' expected at the end of a dictionary")
            return DictLiteral(__elements, __length, self.__prev().line)
        while self.__peek_next().ttype != TokenType.EOF:
            __key = self.__expression()
            self.__consume(TokenType.COLON, "':' expected as delimiter")
            __value = self.__expression()
            __elements[__key.value] = __value
            __length += 1
            match self.__tokens[self.__current].ttype:
                case TokenType.COMMA:
                    self.__consume(TokenType.COMMA,
                                   "',' expected as delimiter")
                case TokenType.RIGHT_BRACE:
                    self.__consume(TokenType.RIGHT_BRACE,
                                   "'}' expected at the end of a dictionary")
                    break
                case _:
                    break
        return DictLiteral(__elements, __length, self.__prev().line)

    def __methods(self, identifier):
        '''
        methods of all datatypes of Dino are added to the AST as MethodLiteral datatype of Dino
        '''
        self.__consume(TokenType.DOT, "Expected '.' to call methods")
        __iden = self.__primary()
        __args = []
        reading_args = False
        if self.__peek_next() and self.__tokens[self.__current].ttype == TokenType.LEFT_PAREN:
            reading_args = True
        while self.__peek_next() and reading_args:
            match self.__tokens[self.__current].ttype:
                case TokenType.LEFT_PAREN:
                    self.__forward()
                    match self.__tokens[self.__current].ttype:
                        case TokenType.RIGHT_PAREN:
                            report_error(
                                DinoError("Invalid Syntax", self.__tokens[self.__current].line))

                        case TokenType.COMMA:
                            report_error(DinoError(
                                "Expected an argument before ',' ", self.__tokens[self.__current].line))

                    __args.append(self.__expression())

                case TokenType.COMMA:
                    self.__consume(TokenType.COMMA,
                                   "Invalid Syntax")
                    __args.append(self.__expression())
                case TokenType.RIGHT_PAREN:
                    self.__consume(TokenType.RIGHT_PAREN,
                                   "')' expected at the end of the arguments")
                    break
                case _:
                    break
        # print(self.__tokens[self.__current].text)
        __method = MethodLiteral(__iden.name, __args, self.__tokens[self.__current].line)
        if (__method.name not in all_methods):
            return report_error(DinoError("{} is not a valid method".format(__method.name), self.__tokens[self.__current].line))
        return BinOp(identifier, TokenType.DOT, __method,  self.__tokens[self.__current].line)

    def __expression(self) -> AST:
        if (self.__match(TokenType.LAMBDA)):
            if (self.__lambdaflag):
                return self.__lambda()
            else:
                self.__lambdaflag = True
                return_value = self.__lambda()
                self.__lambdaflag = False
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
        '''
        Parsing the expressions having operators: "!=" (not equal to) and "=="(equal to)
        '''
        left_operand = self.__comparison()
        while self.__peek_next().ttype != TokenType.EOF:
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
        '''
        Parsing the expressions having operators: '<', '<=' , '>', '>='
        '''
        left_operand = self.__logical_or()
        while self.__peek_next().ttype != TokenType.EOF:
            match self.__tokens[self.__current].ttype:
                case op if op in [TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL]:
                    self.__forward()
                    right_operand = self.__logical_or()
                    left_operand = BinOp(
                        left_operand, op, right_operand, self.__tokens[self.__current - 1].line)
                case _:
                    break
        return left_operand

    def __logical_or(self):

        left_operand = self.__logical_and()
        while self.__peek_next():
            match self.__tokens[self.__current].ttype:
                case op if op == TokenType.OR:
                    self.__forward()
                    right_operand = self.__logical_and()
                    left_operand = BinOp(
                        left_operand, op, right_operand, self.__tokens[self.__current - 1].line)
                case _:
                    break
        return left_operand

    def __logical_and(self):
        left_operand = self.__bitwise_or()
        while self.__peek_next():
            match self.__tokens[self.__current].ttype:
                case op if op == TokenType.AND:
                    self.__forward()
                    right_operand = self.__bitwise_or()
                    left_operand = BinOp(
                        left_operand, op, right_operand, self.__tokens[self.__current - 1].line)
                case _:
                    break
        return left_operand

    def __bitwise_or(self):
        left_operand = self.__bitwise_and()
        while self.__peek_next():
            match self.__tokens[self.__current].ttype:
                case op if op == TokenType.BIT_OR:
                    self.__forward()
                    right_operand = self.__bitwise_and()
                    left_operand = BinOp(
                        left_operand, op, right_operand, self.__tokens[self.__current - 1].line)
                case _:
                    break
        return left_operand

    def __bitwise_and(self):
        left_operand = self.__add()
        while self.__peek_next():
            match self.__tokens[self.__current].ttype:
                case op if op == TokenType.BIT_AND:
                    self.__forward()
                    right_operand = self.__add()
                    left_operand = BinOp(
                        left_operand, op, right_operand, self.__tokens[self.__current - 1].line)
                case _:
                    break
        return left_operand

    def __add(self):

        left_operand = self.__multiply()
        while self.__peek_next().ttype != TokenType.EOF:
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
        while self.__peek_next().ttype != TokenType.EOF:
            match self.__tokens[self.__current].ttype:
                case op if op in [TokenType.STAR, TokenType.SLASH, TokenType.MOD, TokenType.SLASH_SLASH]:
                    self.__forward()
                    right_operand = self.__exponential()
                    left_operand = BinOp(left_operand, op, right_operand, self.__tokens[self.__current - 1].line)
                case _:
                    break
        return left_operand

    def __exponential(self):
        left_operand = self.__unary()
        operands = [left_operand]
        while self.__peek_next().ttype != TokenType.EOF:
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
        while (self.__match(TokenType.BANG, TokenType.MINUS, TokenType.INCREMENT, TokenType.DECREMENT)):
            __op = self.__prev().ttype
            __right = self.__unary()
            return UnOp(__op, __right, self.__tokens[self.__current - 1].line)
        return self.__call()

    def __call(self):
        expr = self.__primary()
        while (True):
            if self.__match(TokenType.LEFT_PAREN):
                if isinstance(expr, Identifier):
                    expr = self.__finishCall(expr)
                else:
                    self.__parseError.line = self.__tokens[self.__current].line
                    self.__parseError.message = "Identifier can't be called"
                    self.__parseError.triggered = True
                    self.__advance()
                    break
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

        return Call(expr, arguments, self.__prev().line)

    def __return(self):
        expr = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Return(expr, self.__prev().line)

    def __primary(self):
        # print(self.__current)
        if (self.__match(TokenType.CAPTURE)):
            self.__consume(TokenType.LEFT_PAREN, "'(' expected")
            if (self.__match(TokenType.STRING)):
                val = Capture(self.__prev().literal, self.__tokens[self.__current - 1].line)
                self.__consume(TokenType.RIGHT_PAREN, "')' expected")
                return val
            else:
                self.__parseError.message = "Syntax Error: Only string accepted during capture"
                self.__parseError.line = self.__prev().line
                report_error(self.__parseError)
                self.__consume(TokenType.RIGHT_PAREN, "')' expected")
        if (self.__match(TokenType.FALSE)):
            return BoolLiteral(False, self.__tokens[self.__current - 1].line)
        if (self.__match(TokenType.TRUE)):
            return BoolLiteral(True, self.__tokens[self.__current - 1].line)
        if (self.__match(TokenType.NULL)):
            return None
        if (self.__match(TokenType.NUMBER)):
            return NumLiteral(self.__prev().literal, self.__tokens[self.__current - 1].line)
        if (self.__match(TokenType.INTEGER)):
            return IntLiteral(self.__prev().literal, self.__tokens[self.__current - 1].line)
        if (self.__match(TokenType.STRING)):
            return StrLiteral(self.__prev().literal, self.__tokens[self.__current - 1].line)
        
        if (self.__match(TokenType.IDENTIFIER)):
            if self.__tokens[self.__current].ttype == TokenType.DOT:
                return self.__methods(Identifier(self.__prev().text, self.__tokens[self.__current - 1].line))
            if (self.__tokens[self.__current].ttype == TokenType.LEFT_BRACKET):
                __iden  = Identifier(self.__prev().text, self.__tokens[self.__current - 1].line)
                index = self.__primary() 
                __method = MethodLiteral("at", index.elements, self.__tokens[self.__current - 1].line)
                
                # return BinOp(__iden ,TokenType.DOT, __method,  self.__tokens[self.__current].line)
                if (self.__tokens[self.__current].ttype == TokenType.EQUAL): 
                    self.__forward()
                    __new_val = self.__expression()

                    __method = MethodLiteral("update", [index.elements[0], __new_val], self.__tokens[self.__current - 1].line)
                    return BinOp(__iden ,TokenType.DOT, __method,  self.__tokens[self.__current].line)
                else:
                    return BinOp(__iden ,TokenType.DOT, __method,  self.__tokens[self.__current].line)
            return Identifier(self.__prev().text, self.__tokens[self.__current - 1].line)
        
        if (self.__match(TokenType.LEFT_PAREN)):
            __expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN,
                           "')' expected after expression.")
            return __expr
        if (self.__match(TokenType.LEFT_BRACKET)):
            return self.__list()
        if (self.__match(TokenType.LEFT_BRACE)):
            return self.__dict()
        if (self.__peek().ttype == TokenType.RIGHT_PAREN):
            return None
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
            return self.__advance()
            # print(msg)
            # exit()

    def __forward(self):
        '''
        helper function to increment the pointer to the current token in the list of tokens.
        If the iterator 'self.__current' is pointing to the last token, function does nothing. 
        Otherwise, increments the iterator
        '''
        if (self.__current >= len(self.__tokens)-1):
            return
        self.__current += 1

    def __peek_next(self):
        '''
        helper function to check if there is any other token after the current token.
        returns next token (if its there) or False(bool) if the current token is the last token
        '''
        if (self.__current+1 < len(self.__tokens)-1):
            return self.__tokens[self.__current + 1]
        else:
            return Token(TokenType.EOF, "", None, -1)

    def __exprstmt(self):

        __expr = self.__expression()
        if (self.__lambdaflag):
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
        if (self.__match(TokenType.RETURN)):
            return self.__return()
        return self.__exprstmt()

    def __assign(self, var, isconst=False):
        if (self.__match(TokenType.EQUAL)):
            __expr = self.__expression()
            self.__consume(TokenType.SEMICOLON,
                           "';' expected after declaration")
            return Assignment(Identifier(var.text, self.__tokens[self.__current - 1].line, isconst), __expr, self.__tokens[self.__current - 1].line, True)
        elif (isconst):
            self.__parseError.message = "Syntax Error: Expected '=' after const variable declaration"
            self.__parseError.line = self.__prev().line
            report_error(self.__parseError)
        else:
            self.__consume(TokenType.SEMICOLON,
                           "';' expected after declaration")
            return Assignment(Identifier(var.text, self.__tokens[self.__current - 1].line), NullLiteral(self.__tokens[self.__current - 1].line), self.__tokens[self.__current - 1].line, True)

    def __declare(self):
        if (self.__match(TokenType.ASSIGN)):
            return self.__assign(self.__consume(TokenType.IDENTIFIER, "Identifier expected"))
        if (self.__match(TokenType.CONST)):
            return self.__assign(self.__consume(TokenType.IDENTIFIER, "Identifier expected"), True)
        # if(self.__match(TokenType.IDENTIFIER)):
        #     __var = self.__prev()
        #     return  self.__assign(__var)
        if (self.__match(TokenType.ECHO)):
            self.__consume(TokenType.LEFT_PAREN, "'(' expected")
            elems = []
            # __expr = self.__expression()
            left = self.__expression()
            elems.append(left)
            while (self.__match(TokenType.COMMA)):
                left = self.__expression()
                elems.append(left)     
                       
            self.__consume(TokenType.RIGHT_PAREN, "')' expected")
            self.__consume(TokenType.SEMICOLON,
                           "';' expected after declaration")
            return Echo(elems, self.__tokens[self.__current - 1].line)
        if (self.__match(TokenType.ABORT)):
            self.__consume(TokenType.LEFT_PAREN, "'(' expected")
            self.__consume(TokenType.RIGHT_PAREN, "')' expected")
            self.__consume(TokenType.SEMICOLON,
                           "';' expected after declaration")
            return Abort("Program Aborted")
        return self.__statement()

    def parse(self):
        __statements = Seq([])
        while (not self.__atEnd()):
            expr = self.__declare()
            if (expr):
                __statements.things.append(expr)
        return __statements
