from fractions import Fraction
from typing import Mapping
from tokenizing.token_scanning import *
from datatypes.datatypes import *


class InvalidProgram(Exception):
    pass

# class evaluator():


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
        case Loop(condition, body):
            while (evaluate(condition)):
                evaluate(body, environment)
        case NumLiteral(value):
            return value
        case BoolLiteral(value):
            return value
        case StrLiteral(value):
            return value
        case BinOp(left, TokenType.PLUS, right):
            if(type(left.value) == float or type(left.value) == int):
                if(type(right.value) == float or type(right.value) == int):
                    return evaluate(left, environment) + evaluate(right, environment)
                else:
                    print("Error: '+' operation valid only for two strings or two numerical values")
                    return ""
            else:
                if(type(right.value)==str):
                    return evaluate(left, environment) + evaluate(right, environment)
                else:
                    print("Error: '+' operation valid only for two strings or two numerical values")
                    return ""
        case BinOp(left, op, right):
            try:
                match op:
                    case TokenType.MINUS: return evaluate(left, environment) - evaluate(right, environment)
                    case TokenType.STAR: return evaluate(left, environment) * evaluate(right, environment)
                    case TokenType.SLASH: return evaluate(left, environment) / evaluate(right, environment)
            except TypeError:
                print("TypeError: Operation not valid for non numeric values")
                return ""
            except ZeroDivisionError:
                print("ZeroDivisionError: Division by Zero is not allowed")
                return ""
            try:
                match op:
                    case TokenType.GREATER: return evaluate(left, environment) > evaluate(right, environment)
                    case TokenType.LESS: return evaluate(left, environment) < evaluate(right, environment)
                    case TokenType.BANG_EQUAL: return evaluate(left, environment) != evaluate(right, environment)
                    case TokenType.EQUAL_EQUAL: return evaluate(left, environment) == evaluate(right, environment)
            except TypeError:
                print("TypeError: Comparison of numeric and non mumeric types")
                return ""
        case UnOp(op, right):
            try:
                match op:
                    case TokenType.BANG: return not evaluate(right, environment)
                    case TokenType.MINUS: return -evaluate(right, environment)
                    case "++": return evaluate(right, environment) + 1
                    case "--": return evaluate(right, environment) - 1
            except TypeError:
                print("TypeError: Operation not valid for non numeric values")
                return ""
        case Seq(things):
            output = None
            for thing in things:
                output = evaluate(thing, environment)
            return output
        case Echo(expr):
            print(evaluate(expr))
            return ""

    raise InvalidProgram()
