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
class Expression:
    expr: 'AST'

@dataclass
class Seq:
    things: List['AST'] 

@dataclass 
class ListLiteral:
    elements: list()
    length: int


AST = NumLiteral | BinOp | UnOp | Variable | Identifier | Let | BoolLiteral | If | Loop | StrLiteral | Expression | Seq | ListLiteral |None

Value = Fraction | bool | int | str | None