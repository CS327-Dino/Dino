from fractions import Fraction
from typing import Mapping
from tokenizing.token_scanning import *
from datatypes.datatypes import *
from errors.error import *


def report_runtime_error(linenum, message):
    print("Runtime Error at", linenum, ":", message)
    # exit()
    raise SystemExit


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
            # return output
            return ListLiteral(output, length, line)

        case DictLiteral(elements, length, line):
            output = {}
            for i in elements.keys():
                # print(type(i))
                new_s = IntLiteral(i, line)
                output[evaluate(new_s, environment)] = evaluate(elements[i], environment)
            # return output
            return DictLiteral(output, length, line)

        case MethodLiteral(name, args, line):
            method_name = name
            arguments = []
            for arg in args:
                arguments.append(evaluate(arg, environment))
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
        case StrLiteral(value, line) as s:
            return s
        case BinOp(left, TokenType.PLUS, right, line):
            evaled_left = evaluate(left, environment)
            evaled_right = evaluate(right, environment)
            if (type(evaled_left) == float or type(evaled_left) == int):
                if (type(evaled_right) == float or type(evaled_right) == int):
                    return evaluate(left, environment) + evaluate(right, environment)
                else:
                    report_runtime_error(
                        line, "Error: '+' operation valid only for two strings or two numerical values or lists")
            else:
                # print(evaled_right)
                match evaled_right:
                    case StrLiteral(value, line):
                        # if ((evaled_right) == StrLiteral):
                        # return evaluate(left, environment).value + evaluate(right, environment).value
                        __concat_str = evaluate(
                            left, environment).value + evaluate(right, environment).value
                        return StrLiteral(__concat_str, line) 
                    case ListLiteral(value, length, line): 
                        __concat_list = evaluate(
                            left, environment).elements + evaluate(right, environment).elements 
                        return ListLiteral(__concat_list, len(__concat_list), line)
                    case _:
                        report_runtime_error(
                            line, "Error: '+' operation valid only for two strings or two numerical values or lists")
        case BinOp(left, op, right, line):
            try:
                match op:
                    case TokenType.MINUS: return evaluate(left, environment) - evaluate(right, environment)
                    case TokenType.STAR: return evaluate(left, environment) * evaluate(right, environment)
                    case TokenType.SLASH:
                        if evaluate(right, environment) == 0:
                            report_runtime_error(
                                line, "ZeroDivisionError: Division by zero")
                        return evaluate(left, environment) / evaluate(right, environment)
                    case TokenType.SLASH_SLASH: return evaluate(left, environment) // evaluate(right, environment)
                    case TokenType.MOD: return evaluate(left, environment) % evaluate(right, environment)
                    case TokenType.EXPONENT: return evaluate(left, environment) ** evaluate(right, environment)
                    case TokenType.OR: return bool(evaluate(left, environment) or evaluate(right, environment))
                    case TokenType.AND: return bool(evaluate(left, environment) and evaluate(right, environment))
                    case TokenType.BIT_OR:
                        try:
                            return evaluate(left, environment) | (evaluate(right, environment))
                        except TypeError:
                            report_runtime_error(
                                line, "TypeError: Bitwise-OR only applicable on integers")
                    case TokenType.BIT_AND:
                        try:
                            return evaluate(left, environment) & evaluate(right, environment)
                        except TypeError:
                            report_runtime_error(
                                line, "TypeError: Bitwise-AND only applicable on integers")
            except TypeError:
                report_runtime_error(
                    line, "TypeError: Operation not valid for non numeric values")
            except ZeroDivisionError:
                report_runtime_error(
                    line, "ZeroDivisionError: Division by Zero is not allowed")
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
                report_runtime_error(
                    line, "TypeError: Comparison of numeric and non mumeric types")
                return ""
            try:
                match op:
                    case TokenType.DOT:
                        val = evaluate(left, environment)
                        method, arguments, line = evaluate(right, environment)
                        # print(left)
                        # print(arguments)
                        # if (type(val) is list):
                        match val:
                            case ListLiteral(elements, length, line):
                                # method = right.name
                                match method:
                                    case "in_list":
                                        assert len(arguments) == 1, "Expected 1 argument"
                                        # print(arguments[0])
                                        return arguments[0] in elements
                                    case "length":
                                        # return len(val)
                                        assert len(
                                            arguments) == 0, "No arguments are expected"
                                        return length
                                    case "head":
                                        # return val[0]
                                        assert len(
                                            arguments) == 0, "No arguments are expected"
                                        if (length > 0):
                                            return elements[0]
                                        else:
                                            report_runtime_error(
                                                line, "The list has no elements")
                                    case "tail":
                                        # return val[1:]
                                        # return elements[1:]
                                        assert len(
                                            arguments) == 0, "No arguments are expected"
                                        return ListLiteral(elements[1:], length - 1, line)
                                    case "slice":
                                        assert len(
                                            arguments) == 2, "Expected 2 arguments"
                                        # return val[int(arguments[0]): int(arguments[1])]
                                        # return elements[arguments[0] : arguments[1]]
                                        try:
                                            sliced_list = elements[arguments[0]: arguments[1]]
                                        except:
                                            report_runtime_error(
                                                line, "List index is out of range")
                                        return ListLiteral(sliced_list, len(sliced_list), line)
                                    case "add":
                                        assert len(
                                            arguments) == 1, "Expected 1 argument"
                                        elements.append(arguments[0])
                                        length += 1
                                        environment.set(left, ListLiteral(
                                            elements, length, line), line, False)
                                        return None
                                    case "at":
                                        assert len(
                                            arguments) == 1, "Expected 1 argument"
                                        try:
                                            e = elements[arguments[0]]
                                            match e:
                                                case ListLiteral(elements, length, line):
                                                    return ListLiteral(elements[:], length, line)
                                            return e
                                        except:
                                            report_runtime_error(
                                                line, "Invalid Index")
                                    case "copy":
                                        assert len(
                                            arguments) == 0, "No arguments are expected"
                                        return ListLiteral(elements[:], length, line)
                                    case "pop":
                                        assert len(arguments) == 1, "Expected 1 argument" 
                                        try:
                                            popped = elements.pop(arguments[0]) 
                                            match popped:
                                                case ListLiteral(elements, length, line):
                                                    return ListLiteral(elements[:], length, line)
                                            return popped 
                                        except:
                                            report_runtime_error(line, "Invalid expression") 
                                    case "update":
                                        assert len(
                                            arguments) == 2, "Expected 2 arguments"
                                        try:
                                            elements[arguments[0]
                                                     ] = arguments[1]
                                            return None
                                        except:
                                            report_runtime_error(
                                                line, "Invalid Expression")
                                    case _:
                                        report_runtime_error(
                                            line, "Invalid method: list does not have any method: {}".format(method))
                            case StrLiteral(value, line):
                                match method:
                                    case "length":
                                        assert len(
                                            arguments) == 0, "No arguments are expected"
                                        return len(value)
                                    case "slice":
                                        assert len(
                                            arguments) == 2, "Expected 2 arguments"
                                        sliced_str = value[arguments[0]: arguments[1]]
                                        return StrLiteral(sliced_str, line)
                                    case "at":
                                        assert len(
                                            arguments) == 1, "Expected 1 argument"
                                        try:
                                            return value[arguments[0]]
                                        except:
                                            report_runtime_error(
                                                line, "Invalid index")
                                    case _:
                                        report_runtime_error(
                                            line, "Invalid method: string does not have any method: {}".format(method))
                            case DictLiteral(elements, length, line):
                                match method:
                                    case "in_dict":
                                        assert len(arguments) == 1, "Expected 1 argument"
                                        # print(arguments[0])
                                        return arguments[0] in elements.keys()
                                    case "length":
                                        assert len(
                                            arguments) == 0, "No arguments are expected"
                                        return length
                                    case "keys":
                                        assert len(
                                            arguments) == 0, "No arguments are expected"
                                        return ListLiteral(list(elements.keys()), length, line)
                                    case "values":
                                        assert len(
                                            arguments) == 0, "No arguments are expected"
                                        return ListLiteral(list(elements.values()), length, line)
                                    case "add":
                                        assert len(arguments) == 2, "Expected 2 arguments"
                                        l = 0
                                        if (arguments[0] not in elements.keys()):
                                            l = 1
                                        elements[arguments[0]] = arguments[1]
                                        environment.set(left, DictLiteral(elements, length + l, line), line, False)
                                        return None
                                    case "at":
                                        assert len(
                                            arguments) == 1, "Expected 1 argument"
                                        try:
                                            # print(type(elements[arguments[0]]))
                                            return elements[arguments[0]]
                                        except:
                                            report_runtime_error(
                                                line, "Invalid key")
                                    case "update": 
                                        assert len(arguments) == 2, "Expected 2 arguments" 
                                        try:
                                            l = 0
                                            if (arguments[0] not in elements.keys()):
                                                l = 1 
                                            elements[arguments[0]] = arguments[1]
                                            environment.set(left, DictLiteral(elements, length + l, line), line, False)
                                            return None
                                        except: 
                                            report_runtime_error(line, "Invalid Expression")
                                    case _:
                                        report_runtime_error(
                                            line, "Invalid method: dict does not have any method: {}".format(method))
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
                report_runtime_error(
                    line, "TypeError: Operation not valid for non numeric values")
        case Seq(things):
            output = None
            for thing in things:
                output = evaluate(thing, environment)
            return output
        case StrLiteral(value, line):
            return value
        case Echo(expr, line):
            print_elem = []
            for elem in expr:
                expr_eval = evaluate(elem, environment)
                if (isinstance(expr_eval, StrLiteral)):
                    print_elem.append(expr_eval.value)
                elif (isinstance(expr_eval, ListLiteral)):
                    print_elem.append(expr_eval.elements)
                else:
                    print_elem.append(expr_eval)
            # expr_eval = evaluate(expr, environment)
            # if(isinstance(expr_eval, StrLiteral)):
            #     print(expr_eval.value)
            # elif(isinstance(expr_eval, ListLiteral)):
            #     print(expr_eval.elements)
            # else:
            #     print(expr_eval)
            # print(evaluate(expr, environment))
            for elem in print_elem:
                print(elem, end="")
            print()
            return None
        case Return(expr, line):
            environment.set("return", evaluate(expr, environment), line, True)
            return ""
        case Function(name, parameters, body, line) as f:
            environment.set(name, f, line, True)
            return None
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
