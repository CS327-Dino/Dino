from fractions import Fraction
from typing import Mapping
from tokenizing.token_scanning import *
from datatypes.datatypes import *

class InvalidProgram(Exception):
    pass


def evaluate(program: AST, environment: Mapping[str, Value] = {}):
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
        case ListLiteral(elements, length):
            return elements
        case BinOp(left, TokenType.PLUS, right):
            return evaluate(left, environment) + evaluate(right, environment)
        case BinOp(left, TokenType.MINUS, right):
            return evaluate(left, environment) - evaluate(right, environment)
        case BinOp(left, TokenType.STAR, right):
            return evaluate(left, environment) * evaluate(right, environment)
        case BinOp(left, TokenType.SLASH, right):
            return Fraction(evaluate(left, environment), evaluate(right, environment))
        case BinOp(left, TokenType.GREATER, right):
            return evaluate(left, environment) > evaluate(right, environment)
        case BinOp(left, TokenType.LESS, right):
            return evaluate(left, environment) < evaluate(right, environment)
        case BinOp(left, TokenType.LESS_EQUAL, right):
            return evaluate(left, environment) <= evaluate(right, environment)
        case BinOp(left, TokenType.GREATER_EQUAL, right):
            return evaluate(left, environment) >= evaluate(right, environment)
        case BinOp(left, TokenType.BANG_EQUAL, right):
            return evaluate(left, environment) != evaluate(right, environment)
        case BinOp(left , TokenType.EQUAL_EQUAL, right):
            return evaluate(left, environment) == evaluate(right, environment)
        case UnOp(TokenType.BANG, right):
            return not evaluate(right, environment)
        case UnOp("++", right):
            return evaluate(right, environment) + 1
        case UnOp("--", right):
            return evaluate(right, environment) - 1
        case Loop(condition, body):
            while evaluate(condition, environment):
                evaluate(body, environment)
        case Seq(things):
            output = None
            for thing in things:
                output = evaluate(thing, environment)
            return output
        case StrLiteral(value):
            return value

    raise InvalidProgram()
