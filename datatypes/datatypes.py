from dataclasses import dataclass, field
from fractions import Fraction
from typing import List
from errors.error import *
from tokenizing.token_scanning import *
from itertools import count

@dataclass
class IntLiteral:
    value: int
    line: int = 0

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
class NullLiteral:
    line: int = 0

@dataclass
class BinOp:
    left: 'AST'
    op: TokenType
    right: 'AST'
    line: int = 0


@dataclass(frozen=True)
class Identifier:
    name: str
    line: int = field(default=0, hash=False, compare=False)
    isconst: bool = False
    uid: int = field(default_factory=count().__next__)

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
class Lambda:
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
    callee: Identifier
    # paren: Token
    arguments: List['AST']
    line: int = 0


@dataclass
class Function:
    name: Identifier
    parameters: List['AST']
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
    '''
    datatype to store lists 
    elements -> elements of 'Dino' list stored as a 'python' list
    length -> length of the list
    line -> line no. in source code
    '''
    elements: List
    length: int
    line: int

@dataclass 
class MethodLiteral:
    '''
    All the methods of the datatypes (e.g. lists, strings, etc.) are of this type.
    name -> name of the method (e.g. 'slice')
    args -> arguments for calling the method as a list
    line -> line no. in the source code
    '''
    name: str 
    args: List
    line: int = 0

@dataclass
class Abort:
    msg: str
    line: int = 0

@dataclass
class Capture:
    msg: str
    line: int = 0

AST = IntLiteral | NumLiteral | NullLiteral | BinOp | UnOp | Identifier | BoolLiteral | ListLiteral | If | Loop | StrLiteral | Expression | Seq | Assignment | Echo | Function | Call | Capture | MethodLiteral | Lambda | None

Value =  float | bool | int | str | None | AST

all_methods = ["length", "head", "tail", "slice", "cons"]
