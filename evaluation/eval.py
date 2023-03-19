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
                report_runtime_error(line, f"Variable '{name}' already exists")
            self.variables[name] = value
            return
        else:
            if name in self.variables:
                self.variables[name] = value
                return
            if self.parent:
                self.parent.set(name, value, line)
                return
            report_runtime_error(line, f"Variable '{name}' not found")

    def __repr__(self):
        return f"Scope({self.variables})"

    def check(self, name, line):
        '''To check whether a variable is already declared or not'''
        if name in self.variables:
            return True
        if self.parent:
            return self.parent.check(name, line)
        return False


def evaluate(program: AST, environment: Scope = Scope()):
    if program is None:
        return None
    match program:
        case Assignment(Identifier(name, _, isconst) as v, value, line, declaration):
            # environment.set(name, value, line, declaration)
            # if isconst and not declaration:
            #     report_runtime_error(line, f"Variable {name} is constant")
            environment.set(v, evaluate(value, environment), line, declaration)
            return None
        case Identifier(name, line) as v:
            return environment.get(v, line)

        case ListLiteral(elements, length, line):
            output = []
            for i in elements:
                output.append(evaluate(i, environment))
            return output

        case MethodLiteral(name, args, line):
            method_name = name
            arguments = []
            for arg in args:
                arguments.append(evaluate(arg))
            return method_name, arguments, line

        case Lambda(Identifier(name) as iden, e1, e2, line):
            v1 = evaluate(e1, environment)
            newEnv = Scope(environment)
            newEnv.set(iden, v1, line, True)
            if e2 is None:
                return v1
            v2 = evaluate(e2, newEnv)
            del newEnv
            return v2

        case If(e0, e1, e2):
            return evaluate(e1, environment) if evaluate(e0, environment) else evaluate(e2, environment)
        case Loop(condition, body):
            output = None
            while evaluate(condition, environment):
                bodyEnv = Scope(environment)
                output = evaluate(body, bodyEnv)
                del bodyEnv
            return output
        case IntLiteral(value, line):
            return value
        case NumLiteral(value, line):
            return value
        case BoolLiteral(value, line):
            return value
        case StrLiteral(value, line):
            return value
        case BinOp(left, TokenType.PLUS, right, line):
            evaled_left = evaluate(left, environment)
            evaled_right = evaluate(right, environment)
            if (type(evaled_left) == float or type(evaled_left) == int):
                if (type(evaled_right) == float or type(evaled_right) == int):
                    return evaluate(left, environment) + evaluate(right, environment)
                else:
                    report_runtime_error(line, "Error: '+' operation valid only for two strings or two numerical values")
            else:
                if (type(evaled_right) == str):
                    return evaluate(left, environment) + evaluate(right, environment)
                else:
                    report_runtime_error(
                        line, "Error: '+' operation valid only for two strings or two numerical values")
        case BinOp(left, op, right, line):
            try:
                match op:
                    case TokenType.MINUS: return evaluate(left, environment) - evaluate(right, environment)
                    case TokenType.STAR: return evaluate(left, environment) * evaluate(right, environment)
                    case TokenType.SLASH: 
                        if evaluate(right, environment) == 0:
                            report_runtime_error(line, "ZeroDivisionError: Division by zero")
                        return evaluate(left, environment) / evaluate(right, environment)
                    case TokenType.MOD: return evaluate(left, environment) % evaluate(right, environment)
                    case TokenType.EXPONENT: return evaluate(left, environment) ** evaluate(right, environment)
                    case TokenType.OR: return bool(evaluate(left, environment) or evaluate(right, environment))
                    case TokenType.AND: return bool(evaluate(left, environment) and evaluate(right, environment))
                    case TokenType.BIT_OR:
                        try:
                            return evaluate(left, environment) | (evaluate(right, environment))
                        except TypeError:
                            report_runtime_error(line, "TypeError: Bitwise-OR only applicable on integers")
                    case TokenType.BIT_AND:
                        try:
                            return evaluate(left, environment) & evaluate(right, environment)
                        except TypeError:
                            report_runtime_error(line, "TypeError: Bitwise-AND only applicable on integers")
            except TypeError:
                report_runtime_error(line, "TypeError: Operation not valid for non numeric values")
            except ZeroDivisionError:
                report_runtime_error(line, "ZeroDivisionError: Division by Zero is not allowed")
            try:
                match op:
                    case TokenType.GREATER: return evaluate(left, environment) > evaluate(right, environment)
                    case TokenType.LESS: return evaluate(left, environment) < evaluate(right, environment)
                    case TokenType.LESS_EQUAL: return evaluate(left, environment) <= evaluate(right, environment)
                    case TokenType.GREATER_EQUAL: return evaluate(left, environment) <= evaluate(right, environment)
                    case TokenType.BANG_EQUAL: return evaluate(left, environment) != evaluate(right, environment)
                    case TokenType.EQUAL_EQUAL: return evaluate(left, environment) == evaluate(right, environment)
                    # case TokenType.DOT:
            except TypeError:
                report_runtime_error(line, "TypeError: Comparison of numeric and non mumeric types")
                return ""
            try:
                match op:
                    case TokenType.DOT:
                        val = evaluate(left)
                        method, arguments, line = evaluate(right)
                        # print(arguments)
                        if (type(val) is list):
                            # method = right.name
                            match method:
                                case "length":
                                    return len(val)
                                case "head":
                                    return val[0]
                                case "tail":
                                    return val[1:]
                                case "slice":
                                    assert len(arguments) == 2
                                    return val[int(arguments[0]): int(arguments[1])]
                                case _:
                                    report_runtime_error(line, "Invalid method: list does not have any method: {}".format(method))
                        elif (type(val) is str):
                            match method:
                                case "slice":
                                    assert len(arguments) == 2
                                    return val[int(arguments[0]): int(arguments[1])]
                                case _:
                                    report_runtime_error(line, "Invalid method: string does not have any method: {}".format(method))
            except TypeError:
                report_runtime_error(line, "Invalid syntax")
                return ""
        case UnOp(op, right, line):
            try:
                match op:
                    case TokenType.BANG: return not evaluate(right, environment)
                    case TokenType.MINUS: return -evaluate(right, environment)
                    case TokenType.INCREMENT: return evaluate(right, environment) + 1
                    case TokenType.DECREMENT: return evaluate(right, environment) - 1
            except TypeError:
                report_runtime_error(line, "TypeError: Operation not valid for non numeric values")
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
        case Return(expr, line):
            environment.set("return", evaluate(expr, environment), line, True)
            return ""
        case Function(name, parameters, body, line) as f:
            # f = Function(name, parameters, body, line)
            environment.set(name, f, line, True)
            return ""
        case Call(callee, arguments, line):
            f = environment.get(callee, line)
            newEnv = Scope(environment)
            for i in range(0, len(f.parameters)):
                newEnv.set(f.parameters[i], evaluate(
                    arguments[i], newEnv), f.line, True)
            for ast in f.body.things:
                output = evaluate(ast, newEnv)
                if "return" in newEnv.variables:
                    return newEnv.get("return", line)
            del newEnv
            return None

        case NullLiteral(line):
            return None
        case Abort(msg):
            print(msg)
            exit()
        case Capture(msg, line):
            try:
                # Try block checks if the input is valid or not
                input_val = input(msg)
                try:
                    # The subsequent try-except blocks identify the datatype of the input
                    # and return the value accordingly
                    if (int(input_val)):
                        return int(input_val)
                except:
                    try:
                        if (float(input_val)):
                            return float(input_val)
                    except:
                        if (input_val == "True" or input_val == "False"):
                            return bool(input_val)
                        return input_val
            except:
                report_runtime_error(
                    line, "Error: Invalid input")
    print(program)
    raise InvalidProgram()
