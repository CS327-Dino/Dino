
from errors.error import *
from enum import Enum


class TokenType(Enum):

    LEFT_PAREN = 0
    RIGHT_PAREN = 1
    LEFT_BRACE = 2
    RIGHT_BRACE = 3
    COMMA = 4
    DOT = 5
    MINUS = 6
    PLUS = 7
    SLASH = 8
    STAR = 9
    SEMICOLON = 10
    BANG = 11
    BANG_EQUAL = 12
    EQUAL = 13
    EQUAL_EQUAL = 14
    GREATER = 15
    GREATER_EQUAL = 16
    LESS = 17
    LESS_EQUAL = 18
    IDENTIFIER = 19
    STRING = 20
    NUMBER = 21
    ASSIGN = 22
    IF = 23
    ELSE = 24
    END = 25
    TRUE = 26
    FALSE = 27
    FOR = 28
    LOOP = 29
    FUNC = 30
    NULL = 31
    AND = 32
    OR = 33
    RETURN = 34
    EOF = 35
    ECHO = 36
    LEFT_BRACKET = 37
    RIGHT_BRACKET = 38
    EXPONENT = 39
    COMMENT = 40
    BIT_OR = 41
    BIT_AND = 42
    LAMBDA = 43
    IN = 44
    ABORT = 45
    CAPTURE = 46
    INTEGER = 47
    CONST = 48
    INCREMENT = 49
    DECREMENT = 50
    MOD = 51
    SLASH_SLASH = 52
    COLON = 53
    STOP = 54
    ITERATE = 55


class Token():
    ttype: TokenType
    text: str
    literal: object
    line: int

    def __init__(self, ttype: TokenType, text: str, literal: object, line: int):
        self.ttype = ttype
        self.text = text
        self.literal = literal
        self.line = line

    def print_token(self):
        print(str(self.ttype.name), self.text, ", Literal :",
              str(self.literal), ", On Line :", self.line)


class Scanner():
    code: str
    token_list: list
    error: DinoError
    start = 0
    current = 0
    line = 1

    keywords = {

        "assign": TokenType.ASSIGN,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "end": TokenType.END,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "loop": TokenType.LOOP,
        "func": TokenType.FUNC,
        "null": TokenType.NULL,
        "and": TokenType.AND,
        "or": TokenType.OR,
        "return": TokenType.RETURN,
        "echo": TokenType.ECHO,
        "abort": TokenType.ABORT,
        "capture": TokenType.CAPTURE,
        "const": TokenType.CONST,
        "lambda": TokenType.LAMBDA,
        "in": TokenType.IN,
        "stop": TokenType.STOP,
        "iterate": TokenType.ITERATE,
    }

    def __init__(self, code, error):
        self.code = code
        self.error = error
        self.token_list = []

    def __end_reached(self):
        return self.current >= len(self.code)

    def __peek(self):
        if (self.__end_reached()):
            return '\0'
        return self.code[self.current]

    def __peek_next(self):
        if (self.current + 1 >= len(self.code)):
            return '\0'
        return self.code[self.current+1]

    def generate_tokens(self):
        while (self.__end_reached() == False):
            self.start = self.current
            self.__scan_tokens()

        eof_token = Token(TokenType.EOF, "", None, self.line)
        self.token_list.append(eof_token)
        return self.token_list

    def __scan_tokens(self):
        c = self.code[self.current]
        self.current += 1

        if c == '(':
            self.__add_tokens(TokenType.LEFT_PAREN)
        elif c == ')':
            self.__add_tokens(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.__add_tokens(TokenType.LEFT_BRACE)
        elif c == '}':
            self.__add_tokens(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.__add_tokens(TokenType.COMMA)
        elif c == '.':
            self.__add_tokens(TokenType.DOT)
        elif c == '-':
            if self.__peek() == '-':
                self.current += 1
                self.__add_tokens(TokenType.DECREMENT)
            else:
                self.__add_tokens(TokenType.MINUS)
        elif c == '+':
            if self.__peek() == '+':
                self.current += 1
                self.__add_tokens(TokenType.INCREMENT)
            else:
                self.__add_tokens(TokenType.PLUS)
        elif c == ';':
            self.__add_tokens(TokenType.SEMICOLON)
        elif c == '*':
            self.__add_tokens(TokenType.STAR)
        elif c == '/':
            if self.__peek() == '/':
                self.current += 1
                self.__add_tokens(TokenType.SLASH_SLASH)
            else:
                self.__add_tokens(TokenType.SLASH)
        elif c == '%':
            self.__add_tokens(TokenType.MOD)
        elif c == '^':
            self.__add_tokens(TokenType.EXPONENT)
        elif c == '[':
            self.__add_tokens(TokenType.LEFT_BRACKET)
        elif c == ']':
            self.__add_tokens(TokenType.RIGHT_BRACKET)
        elif c == '|':
            self.__add_tokens(TokenType.BIT_OR)
        elif c == '&':
            self.__add_tokens(TokenType.BIT_AND)
        elif c == '!':
            if self.__peek() == '=':
                self.current += 1
                self.__add_tokens(TokenType.BANG_EQUAL)
            else:
                self.__add_tokens(TokenType.BANG)
        elif c == '=':
            if self.__peek() == '=':
                self.current += 1
                self.__add_tokens(TokenType.EQUAL_EQUAL)
            else:
                self.__add_tokens(TokenType.EQUAL)
        elif c == '<':
            if self.__peek() == '=':
                self.current += 1
                self.__add_tokens(TokenType.LESS_EQUAL)
            else:
                self.__add_tokens(TokenType.LESS)
        elif c == '>':
            if self.__peek() == '=':
                self.current += 1
                self.__add_tokens(TokenType.GREATER_EQUAL)
            else:
                self.__add_tokens(TokenType.GREATER)
        elif c == ' ' or c == '\r' or c == '\t':
            pass
        elif c == '?':

            if (self.__peek() == ":"):
                self.current += 1
                self.__multicomment()
            else:
                self.__comment()
        elif c == ':':
            self.__add_tokens(TokenType.COLON)
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.__string()
        elif self.__digit_check(c):
            self.__number()
        elif self.__alpha_check(c):
            self.__identifier()
        else:
            # Produce Error
            print(c)
            self.error.line = self.line
            self.error.message = "Unexpected Symbol"
            self.error.triggered = True

    def __string(self):
        while (self.__peek() != '"' and self.__end_reached() == False):
            if self.__peek() == '\n':
                self.line += 1
            self.current += 1
        if self.__end_reached() == True:
            self.error.line = self.line
            self.error.message = "Unterminated String"
            self.error.triggered = True
            pass
        else:
            self.current += 1
            s = self.code[self.start + 1:self.current - 1]
            string_token = Token(TokenType.STRING, s, s, self.line)
            self.token_list.append(string_token)

    def __number(self):
        while (self.__digit_check(self.__peek()) == True):
            self.current += 1

        if self.__peek() == '.' and self.__digit_check(self.__peek_next()):
            self.current += 1
            while (self.__digit_check(self.__peek()) == True):
                self.current += 1

            n = self.code[self.start:self.current]
            num_token = Token(TokenType.NUMBER, n, float(n), self.line)
            self.token_list.append(num_token)
        else:
            n = self.code[self.start:self.current]
            int_token = Token(TokenType.INTEGER, n, int(n), self.line)
            self.token_list.append(int_token)

    def __identifier(self):
        while (self.__alpha_numeric_check(self.__peek()) == True):
            self.current += 1

        s = self.code[self.start: self.current]
        if s in self.keywords:
            if s == "true":
                token = Token(TokenType.TRUE, "true", True, self.line)
                self.token_list.append(token)
            elif s == "false":
                token = Token(TokenType.FALSE, "false", False, self.line)
                self.token_list.append(token)
            else:
                self.__add_tokens(self.keywords[s])
        else:
            self.__add_tokens(TokenType.IDENTIFIER)

    def __digit_check(self, c):
        return c >= '0' and c <= '9'

    def __alpha_check(self, c):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_'

    def __alpha_numeric_check(self, c):
        return self.__digit_check(c) or self.__alpha_check(c)

    def __add_tokens(self, ttype: TokenType):
        text = self.code[self.start: self.current]
        token = Token(ttype, text, None, self.line)
        self.token_list.append(token)

    def __comment(self):
        while (self.__end_reached() == False):
            self.current += 1
            if (self.__peek() == '\n'):
                self.line += 1
                self.current += 1
                break

    def __multicomment(self):
        while (self.__end_reached() == False and not (self.__peek() == ':' and self.__peek_next() == '?')):
            if self.__peek() == '\n':
                self.line += 1
            self.current += 1
        if (self.__end_reached() == False):
            self.current += 2
        else:
            self.error.line = self.line
            self.error.message = "Unterminated Multiline Comment"
            self.error.triggered = True
            pass
