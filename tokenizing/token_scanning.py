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

    def __init__(self, code, error):
        self.code = code
        self.error = error
        self.token_list = []

    def __end_reached(self):
        return self.current >= len(self.code)

    def __peek(self):
        if(self.__end_reached()):
            return '\0'
        return self.code[self.current]

    def generate_tokens(self):
        while(self.__end_reached() == False):
            self.start = self.current
            self.__scan_tokens()

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
            self.__add_tokens(TokenType.MINUS)
        elif c == '+':
            self.__add_tokens(TokenType.PLUS)
        elif c == ';':
            self.__add_tokens(TokenType.SEMICOLON)
        elif c == '*':
            self.__add_tokens(TokenType.STAR)
        elif c == '/':
            self.__add_tokens(TokenType.SLASH)
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
        else:
            # Produce Error
            self.error.line = self.line
            self.error.message = "Unexpected Symbol"
            self.error.triggered = True

    def __add_tokens(self, ttype: TokenType):
        text = self.code[self.start: self.current]
        token = Token(ttype, text, None, self.line)
        self.token_list.append(token)
