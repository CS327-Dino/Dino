from enum import Enum
from errors.error import *


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
        print(str(self.ttype.name), ":", self.text,
              str(self.literal), "On Line :", self.line)


class Token_List():
    code: str
    token_list: list
    error: DinoError
    star = 0
    current = 0
    line = 1

    def __init__(self, code, error):
        self.code = code
        self.error = error

    def generate_tokens(self):
        while(self.current < len(self.code)):
            self.start = self.current
            self.__scan_tokens()

        eof_token = Token(TokenType.EOF, "", None, self.line)
        self.token_list.append(eof_token)
        return self.token_list

    def __scan_tokens(self):
        c = self.code[self.current]
        self.current += 1
