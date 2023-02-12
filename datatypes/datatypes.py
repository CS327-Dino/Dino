from dataclasses import dataclass
from fractions import Fraction
from typing import List

@dataclass
class NumLiteral:
    value: Fraction

    def __init__(self, *args):
        self.value = Fraction(*args)

@dataclass
class BoolLiteral:
    value: bool

@dataclass
class BinOp:
    operator: str
    left: "AST"
    right: "AST"

@dataclass
class Identifier:
    name: str

@dataclass
class UnOp:
    operator: str
    right: "AST"

@dataclass
class Variable:
    name: str

@dataclass
class Let:
    var: "AST"
    e1: "AST"
    e2: "AST"

@dataclass
class If:
    var: "AST"
    e1: "AST"
    e2: "AST"

@dataclass
class StrLiteral:
    value: str

@dataclass
class Loop:
    condition: 'AST'
    body: 'AST'

@dataclass
class Seq:
    things: List['AST']


AST = NumLiteral | BinOp | UnOp | Variable | Identifier | Let | BoolLiteral | If | Loop | StrLiteral | Seq | None

Value = Fraction | bool | int | str | None