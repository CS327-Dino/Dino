from dataclasses import dataclass
from fractions import Fraction
from typing import List
from errors.error import *
from tokenizing.token_scanning import *


@dataclass
class NumLiteral:
    value: float
    line: int = 0

    # def __init__(self, *args):
    #     self.value = Fraction(*args)


@dataclass
class BoolLiteral:
    value: bool
    line: int = 0


@dataclass
class BinOp:
    left: 'AST'
    op: TokenType
    right: 'AST'
    line: int = 0


@dataclass
class Identifier:
    name: str
    line: int = 0


@dataclass
class UnOp:
    op: str | TokenType
    right: 'AST'
    line: int = 0

# @dataclass
# class Variable:
#     name: str
#     value: 'AST'


@dataclass
class Assignment:
    var: "Identifier"
    value: "AST"
    line: int = 0
    declaration: bool = False


@dataclass
class Let:
    var: "AST"
    e1: "AST"
    e2: "AST"
    line: int = 0


@dataclass
class If:
    condition: 'AST'
    ifPart: 'AST'
    elsePart: 'AST'


@dataclass
class StrLiteral:
    value: str
    line: int = 0


@dataclass
class Loop:
    condition: 'AST'
    body: 'AST'


@dataclass
class Call:
    callee: 'AST'
    paren: Token
    arguments: List


@dataclass
class Function:
    name: Token
    parameters: List
    body: 'AST'
    line: int = 0


@dataclass
class Expression:
    expr: 'AST'


@dataclass
class Echo:
    expr: 'AST'
    line: int = 0


@dataclass
class Seq:
    things: List['AST']


@dataclass
class ListLiteral:
    elements: list()
    length: int
    line: int
    head = 'AST'
    tail = 'AST'


AST = NumLiteral | BinOp | UnOp | Identifier | Let | BoolLiteral | ListLiteral  |  If | Loop | StrLiteral | Expression | Seq | Assignment | Echo | None

Value = Fraction | bool | int | str | None | AST
