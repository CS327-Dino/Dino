from dataclasses import dataclass
from fractions import Fraction
from typing import List
from tokenizing.token_scanning import TokenType
from errors.error import *

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
    op: TokenType
    right: 'AST'

@dataclass
class Identifier:
    name: str

@dataclass
class UnOp:
    op: str
    right: 'AST'

# @dataclass
# class Variable:
#     name: str
#     value: 'AST'

@dataclass
class Assignment:
    var: "Identifier"
    value: "AST"
    declaration: bool = False

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

class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}

    def get(self, name):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name)
        raise Exception(f"Variable {name} not found")

    def set(self, name, value, declaration=False):
        if declaration:
            if name in self.variables:
                raise Exception(f"Variable {name} already exists")
            self.variables[name] = value
            return
        else:
            if name in self.variables:
                self.variables[name] = value
                return
            if self.parent:
                self.parent.set(name, value)
                return
            raise Exception(f"Variable {name} not found")

    def __repr__(self):
        return f"Scope({self.variables})"


AST = NumLiteral | BinOp | UnOp | Identifier | Let | BoolLiteral | If | Loop | StrLiteral | Expression | Seq | Assignment | None

Value = Fraction | bool | int | str | None