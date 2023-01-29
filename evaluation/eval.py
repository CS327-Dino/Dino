from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping


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


# AST = Union(NumLiteral, BinOp)
AST = NumLiteral | BinOp | Variable | Let | BoolLiteral | UnOp | If

Value = Fraction | bool | int


class InvalidProgram(Exception):
    pass


def evaluate(program: AST, environment: Mapping[str, Value] = {}) -> Value:
    match program:
        case Variable(name):
            if name in environment:
                return environment[name]
            raise InvalidProgram()
        case Let(Variable(name), e1, e2):
            v1 = evaluate(e1, environment)
            return evaluate(e2, environment | {name: v1})
        case If(e0, e1, e2):
            return evaluate(e1) if evaluate(e0) else evaluate(e2)
        case NumLiteral(value):
            return value
        case BoolLiteral(value):
            return value
        case BinOp("+", left, right):
            return evaluate(left, environment) + evaluate(right, environment)
        case BinOp("-", left, right):
            return evaluate(left, environment) - evaluate(right, environment)
        case BinOp("*", left, right):
            return evaluate(left, environment) * evaluate(right, environment)
        case BinOp("/", left, right):
            return Fraction(evaluate(left, environment), evaluate(right, environment))
        case BinOp(">", left, right):
            return evaluate(left, environment) > evaluate(right, environment)
        case BinOp("<", left, right):
            return evaluate(left, environment) < evaluate(right, environment)
        case BinOp("!=", left, right):
            return evaluate(left, environment) != evaluate(right, environment)
        case BinOp("==", left, right):
            return evaluate(left, environment) == evaluate(right, environment)
        case UnOp("!", right):
            return not evaluate(right, environment)
        case UnOp("++", right):
            return evaluate(right, environment) + 1
        case UnOp("--", right):
            return evaluate(right, environment) - 1

    raise InvalidProgram()
