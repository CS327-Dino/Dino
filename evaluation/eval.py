from fractions import Fraction
from typing import Mapping
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
        case Loop(condition, body):
            iter = 0
            n = 10
            while (evaluate(condition) and iter<n):
                evaluate(body, environment)
                iter+=1
            if(iter == n):
                print("Ran out of maximum iterations")
            return ""
        case NumLiteral(value):
            return value
        case BoolLiteral(value):
            return value
        case StrLiteral(value):
            return value
        case BinOp(left, "+", right):
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
                    case "-": return evaluate(left, environment) - evaluate(right, environment)
                    case "*": return evaluate(left, environment) * evaluate(right, environment)
                    case "/": return evaluate(left, environment) / evaluate(right, environment)
            except TypeError:
                print("TypeError: Operation not valid for non numeric values")
                return ""
            except ZeroDivisionError:
                print("ZeroDivisionError: Division by Zero is not allowed")
                return ""
            try:
                match op:
                    case ">": return evaluate(left, environment) > evaluate(right, environment)
                    case "<": return evaluate(left, environment) < evaluate(right, environment)
                    case "!=": return evaluate(left, environment) != evaluate(right, environment)
                    case "==": return evaluate(left, environment) == evaluate(right, environment)
            except TypeError:
                print("TypeError: Comparison of numeric and non mumeric types")
                return ""
        case UnOp(op, right):
            try:
                match op:
                    case "!": return not evaluate(right, environment)
                    case "-": return -evaluate(right, environment)
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
