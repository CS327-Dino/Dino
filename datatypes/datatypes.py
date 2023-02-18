from dataclasses import dataclass
from fractions import Fraction
from typing import List
from tokenizing.token_scanning import *


@dataclass
class NumLiteral:
    value: float

    # def __init__(self, *args):
    #     self.value = Fraction(*args)


@dataclass
class BoolLiteral:
    value: bool


@dataclass
class BinOp:
    left: 'AST'
    op: str
    right: 'AST'


@dataclass
class Identifier:
    name: str


@dataclass
class UnOp:
    op: str
    right: 'AST'


@dataclass
class Variable:
    name: str
    value: 'AST'


@dataclass
class Let:
    var: "AST"
    e1: "AST"
    e2: "AST"


@dataclass
class If:
    condition: 'AST'
    ifPart: 'AST'
    elsePart: 'AST'


@dataclass
class StrLiteral:
    value: str


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


@dataclass
class Expression:
    expr: 'AST'


@dataclass
class Echo:
    expr: 'AST'

@dataclass
class Seq:
    things: List['AST']


AST = NumLiteral | BinOp | UnOp | Variable | Identifier | Let | BoolLiteral | If | Loop | StrLiteral | Expression | Seq | None

Value = Fraction | bool | int | str | None
