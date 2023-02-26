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

def resolution(program: AST, environment: Scope = Scope()):
    if program is None:
        return None
    match program:
        case NumLiteral(value, line) as n:
            return n
        case BoolLiteral(value, line) as b:
            return b
        case Assignment(Identifier(name) as iden, value, line, declaration):
            value = resolution(value, environment)
            if declaration:
                environment.set(name, iden, line, True)
                return Assignment(Identifier(name, iden.line, iden.isconst, iden.uid), value, line, declaration)
            else:
                reiden = environment.get(name, line)
                return Assignment(Identifier(name, iden.line, reiden.isconst, reiden.uid), value, line, declaration)
        case Identifier(name, line) as iden:
            reiden = environment.get(name, line)
            return Identifier(name, iden.line, reiden.isconst, reiden.uid)
        case Seq(things):
            output = []
            for thing in things:
                output.append(resolution(thing, environment))
            return Seq(output)
        case Echo(expr, line):
            return Echo(resolution(expr, environment), line)
        case BinOp(left, op, right, line):
            return BinOp(resolution(left, environment), op, resolution(right, environment), line)
        case UnOp(op, right, line):
            return UnOp(op, resolution(right, environment), line)
        case ListLiteral(elements, length, line):
            output = []
            for i in elements:
                output.append(resolution(i, environment))
            return ListLiteral(output, length, line)
        case Lambda(Identifier(name), e1, e2, line):
            e1 = resolution(e1, environment)
            newEnv = Scope(environment)
            newIden = Identifier(name, line, True)
            newEnv.set(name, newIden, line, True)
            # print(newEnv)
            e2 = resolution(e2, newEnv)
            del newEnv
            return Lambda(newIden, e1, e2, line)
        case If(e0, e1, e2):
            e0 = resolution(e0, environment)
            newEnv = Scope(environment)
            e1 = resolution(e1, newEnv)
            del newEnv
            newEnv = Scope(environment)
            e2 = resolution(e2, newEnv)
            del newEnv
            return If(e0, e1, e2)
        case Loop(condition, body):
            condition = resolution(condition, environment)
            newEnv = Scope(environment)
            body = resolution(body, newEnv)
            del newEnv
            return Loop(condition, body)
        case StrLiteral(value, line):
            return StrLiteral(value, line)
        case Function(name, args, body, line):
            environment.set(name.name, name, line, True)
            newEnv = Scope(environment)
            for i in args:
                newEnv.set(i.name, i, line, True)
            body = resolution(body, newEnv)
            del newEnv
            return Function(name, args, body, line)
        case Call(name, args, line):
            args = [resolution(i, environment) for i in args]
            return Call(resolution(name, environment), args, line)
        case MethodLiteral(name, args, line):
            args = [resolution(i, environment) for i in args]
            return MethodLiteral(name, args, line)

    
    print(program)
    raise InvalidProgram()


def evaluate(program: AST, environment: Scope = Scope()):
    if program is None:
        return None
    match program:
        case Assignment(Identifier(name, _, isconst) as v, value, line, declaration):
            # environment.set(name, value, line, declaration)
            if isconst and not declaration:
                report_runtime_error(line, f"Variable {name} is constant")
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
        case NumLiteral(value, line):
            return value
        case BoolLiteral(value, line):
            return value
        case StrLiteral(value, line):
            return value
        case BinOp(left, TokenType.PLUS, right, line):
            evaled_left = evaluate(left, environment)
            evaled_right = evaluate(right, environment)
            if (type(evaled_left) == float or type(evaled_right) == int):
                if (type(evaled_right) == float or type(evaled_right) == int):
                    return evaluate(left, environment) + evaluate(right, environment)
                else:
                    report_runtime_error(
                        line, "Error: '+' operation valid only for two strings or two numerical values")
                    return ""
            else:
                if (type(evaled_right) == str):
                    return evaluate(left, environment) + evaluate(right, environment)
                else:
                    report_runtime_error(
                        line, "Error: '+' operation valid only for two strings or two numerical values")
                    return ""
        case BinOp(left, op, right, line):
            try:
                match op:
                    case TokenType.MINUS: return evaluate(left, environment) - evaluate(right, environment)
                    case TokenType.STAR: return evaluate(left, environment) * evaluate(right, environment)
                    case TokenType.SLASH: return evaluate(left, environment) / evaluate(right, environment)
                    case TokenType.EXPONENT: return evaluate(left, environment) ** evaluate(right, environment)
                    case TokenType.OR: return bool(evaluate(left, environment) or evaluate(right, environment) )
                    case TokenType.AND: return bool(evaluate(left, environment) and evaluate(right, environment)) 
                    case TokenType.BIT_OR: 
                        try: return evaluate(left, environment)|(evaluate(right, environment))
                        except TypeError:report_runtime_error(line, "TypeError: Bitwise-OR only applicable on integers")
                    case TokenType.BIT_AND: 
                        try: return evaluate(left, environment) & evaluate(right, environment)
                        except TypeError:report_runtime_error(line, "TypeError: Bitwise-AND only applicable on integers")
            except TypeError:
                report_runtime_error(
                    line, "TypeError: Operation not valid for non numeric values")
                return ""
            except ZeroDivisionError:
                report_runtime_error(
                    line, "ZeroDivisionError: Division by Zero is not allowed")
                return ""
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
                                    assert len(arguments) ==2 
                                    return val[int(arguments[0]): int(arguments[1]) ]
                                case _:
                                    report_runtime_error(line, "Invalid method: list does not have any method: {}".format(method))
                        elif(type(val) is str):
                            match method:
                                case "slice":
                                    assert len(arguments) ==2 
                                    return val[int(arguments[0]): int(arguments[1]) ]
                                case _:
                                    report_runtime_error(line, "Invalid method: string does not have any method: {}".format(method))                   
            except TypeError:
                report_runtime_error(
                    line, "Invalid syntax")
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
        case Function(name, parameters, body, line) as f:
            # f = Function(name, parameters, body, line)
            environment.set(name, f, line, True)
            return ""
        case Call(callee, arguments, line):
            f = environment.get(callee, line)
            newEnv = Scope(environment)
            for i in range(0 , len(f.parameters)):
                newEnv.set(f.parameters[i] , evaluate(arguments[i] , newEnv) , f.line , True)
            v = evaluate(f.body, newEnv)
            del newEnv
            return v
        case NullLiteral(line):
            return None

    print(program)
    raise InvalidProgram()
