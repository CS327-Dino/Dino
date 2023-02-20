from fractions import Fraction
from typing import Mapping
from tokenizing.token_scanning import *
from datatypes.datatypes import *
from errors.error import *

def report_runtime_error(linenum, message):
    print("Runtime Error at", linenum, ":", message)
    exit()

class InvalidProgram(Exception):
    pass

class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}

    def get(self, name, line):
        if name in self.variables:
            return self.variables[name]
        if self.parent:
            return self.parent.get(name, line)
        report_runtime_error(line, f"Variable {name} not found")

    def set(self, name, value, line, declaration=False):
        if declaration:
            if name in self.variables:
                report_runtime_error(line, f"Variable {name} already exists")
            self.variables[name] = value
            return
        else:
            if name in self.variables:
                self.variables[name] = value
                return
            if self.parent:
                self.parent.set(name, value, line)
                return
            report_runtime_error(line, f"Variable {name} not found")

    def __repr__(self):
        return f"Scope({self.variables})"

def evaluate(program: AST, environment: Scope = Scope()):
    match program:
        case Assignment(Identifier(name), value, line, declaration):
            # environment.set(name, value, line, declaration)
            environment.set(name, evaluate(value, environment), line, declaration)
            return None
        case Identifier(name, line):
            return environment.get(name, line)
        case ListLiteral(elements, length, line):
            output = []
            for i in elements:
                output.append(evaluate(i,environment))
            return output
        case Let(Identifier(name), e1, e2, line):
            v1 = evaluate(e1, environment)
            newEnv = Scope(environment)
            newEnv.set(name, v1, line, True)
            v2 = evaluate(e2, newEnv)
            del newEnv
            return v2
        case If(e0, e1, e2):
            return evaluate(e1) if evaluate(e0) else evaluate(e2)
        case Loop(condition, body):
            output = None
            while evaluate(condition, environment):
                bodyEnv = Scope(environment)
                output = evaluate(body, bodyEnv)
                del bodyEnv
            return output
        case NumLiteral(value, line):
            return value
        case BoolLiteral(value, line):
            return value
        case StrLiteral(value, line):
            return value
        case BinOp(left, TokenType.PLUS, right, line):
            evaled_left = evaluate(left, environment)
            evaled_right = evaluate(right, environment)
            if(type(evaled_left) == float or type(evaled_right) == int):
                if(type(evaled_right) == float or type(evaled_right) == int):
                    return evaluate(left, environment) + evaluate(right, environment)
                else:
                    report_runtime_error(line, "Error: '+' operation valid only for two strings or two numerical values")
                    return ""
            else:
                if(type(evaled_right)==str):
                    return evaluate(left, environment) + evaluate(right, environment)
                else:
                    report_runtime_error(line, "Error: '+' operation valid only for two strings or two numerical values")
                    return ""
        case BinOp(left, op, right, line):
            try:
                match op:
                    case TokenType.MINUS: return evaluate(left, environment) - evaluate(right, environment)
                    case TokenType.STAR: return evaluate(left, environment) * evaluate(right, environment)
                    case TokenType.SLASH: return evaluate(left, environment) / evaluate(right, environment)
                    case TokenType.EXPONENT: return evaluate(left, environment) ** evaluate(right, environment)
            except TypeError:
                report_runtime_error(line, "TypeError: Operation not valid for non numeric values")
                return ""
            except ZeroDivisionError:
                report_runtime_error(line, "ZeroDivisionError: Division by Zero is not allowed")
                return ""
            try:
                match op:
                    case TokenType.GREATER: return evaluate(left, environment) > evaluate(right, environment)
                    case TokenType.LESS: return evaluate(left, environment) < evaluate(right, environment)
                    case TokenType.LESS_EQUAL: return evaluate(left, environment) <= evaluate(right, environment)
                    case TokenType.GREATER_EQUAL: return evaluate(left, environment) <= evaluate(right, environment)
                    case TokenType.BANG_EQUAL: return evaluate(left, environment) != evaluate(right, environment)
                    case TokenType.EQUAL_EQUAL: return evaluate(left, environment) == evaluate(right, environment)
            except TypeError:
                report_runtime_error(line, "TypeError: Comparison of numeric and non mumeric types")
                return ""
        case UnOp(op, right, line):
            try:
                match op:
                    case TokenType.BANG: return not evaluate(right, environment)
                    case TokenType.MINUS: return -evaluate(right, environment)
                    case "++": return evaluate(right, environment) + 1
                    case "--": return evaluate(right, environment) - 1
            except TypeError:
                report_runtime_error(line, "TypeError: Operation not valid for non numeric values")
                return ""
        case Seq(things):
            output = None
            for thing in things:
                output = evaluate(thing, environment)
            return output
        case StrLiteral(value, line):
            return value
        case Echo(expr, line):
            print(evaluate(expr, environment))
            return ""

    print(program)
    raise InvalidProgram()
