from fractions import Fraction
from typing import Mapping
from tokenizing.token_scanning import *
from datatypes.datatypes import *
from errors.error import *
import sys
sys.setrecursionlimit(10000)


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
            if type(value) == str or type(value) == int or type(value) == float or type(value) == bool:
                environment.set(v, value, line, declaration)
            else:
                environment.set(v, evaluate(
                    value, environment), line, declaration)
            return None
        case ParallelAssignment(list_identifiers, list_expressions, line, declaration):

            for i in range(len(list_identifiers)):

                environment.set(list_identifiers[i], evaluate(
                    list_expressions[i], environment), line, declaration)
            return None

        case Identifier(name, line) as v:
            return environment.get(v, line)

        case ListLiteral(elements, length, line):
            output = []
            for i in elements:
                output.append(evaluate(i, environment))

            return ListLiteral(output, length, line)

        case DictLiteral(elements, length, line):
            output = {}
            for i in elements.keys():
                if type(elements[i]) == Identifier:
                    output[i] = elements[i]
                elif type(elements[i]) == StrLiteral:
                    output[i] = elements[i].value
                else:
                    output[i] = evaluate(elements[i], environment)

            return DictLiteral(output, length, line)

        case MethodLiteral(name, args, line):
            method_name = name
            arguments = []
            for arg in args:
                # if type(arg) is Identifier:
                # print(arg)
                # arguments.append(arg)
                if type(arg) is StrLiteral:
                    arguments.append(arg.value)
                else:
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

        case ParallelLambda(list_identifiers, list_expressions, e2, line):
            # list_identifiers is a list of identifiers
            # list_expressions is a list of expressions
            # For example in case of lambda x=2 and y=3 in x+y, list_identifiers will be [x,y] and list_expressions will be [2,3]
            newEnv = Scope(environment)
            for i in range(len(list_identifiers)):
                v1 = evaluate(list_expressions[i], environment)
                newEnv.set(list_identifiers[i], v1, line, True)
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
                for ast in body.things:
                    output = evaluate(ast, bodyEnv)
                    if "stop" in bodyEnv.variables:
                        return
                del bodyEnv
            return output
        case Iterate(iterable, condition, increment, body):
            output = None
            # environment.set(iterable.var, evaluate(iterable.value, environment), iterable.line, True)
            # while(evaluate(condition, environment)):
            #     bodyEnv = Scope(environment)
            #     output = evaluate(body, bodyEnv)
            #     evaluate(increment, bodyEnv)
            #     del bodyEnv
            if iterable.declaration:
                environment.set(iterable.var, evaluate(
                    iterable.value, environment), iterable.line, True)
                while (evaluate(condition, environment)):
                    bodyEnv = Scope(environment)
                    output = evaluate(body, bodyEnv)
                    evaluate(increment, bodyEnv)
                    del bodyEnv
            else:
                while (evaluate(condition, environment)):
                    bodyEnv = Scope(environment)
                    output = evaluate(body, bodyEnv)
                    evaluate(increment, environment)
                    del bodyEnv
            return output
        case IntLiteral(value, line):
            return value
        case NumLiteral(value, line):
            return value
        case BoolLiteral(value, line):
            return value
        case StrLiteral(value, line) as v:
            return v
            # return value
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
                e_left = evaluate(left, environment)
                e_right = evaluate(right, environment)
                if type(e_left) == StrLiteral:
                    e_left = e_left.value
                if type(e_right) == StrLiteral:
                    e_right = e_right.value
                if type(e_left) == Identifier:
                    e_left = evaluate(e_left, environment)
                if type(e_right) == Identifier:
                    e_right = evaluate(e_right, environment)
                match op:
                    case TokenType.GREATER: return e_left > e_right
                    case TokenType.LESS: return e_left < e_right
                    case TokenType.LESS_EQUAL: return e_left <= e_right
                    case TokenType.GREATER_EQUAL: return e_left >= e_right
                    case TokenType.BANG_EQUAL: return e_left != e_right
                    case TokenType.EQUAL_EQUAL: return e_left == e_right
                    
            except TypeError:
                report_runtime_error(
                    line, "TypeError: Comparison of numeric and non mumeric types")
                return ""
            try:
                match op:
                    case TokenType.DOT:
                        val = evaluate(left, environment)
                        method, arguments, line = evaluate(right, environment)
                        # print(val)
                        # print(arguments)
                        # if (type(val) is list):
                        match val:
                            case ListLiteral(elements, length, line):
                                # method = right.name
                                match method:
                                    case "in_list":
                                        assert len(
                                            arguments) == 1, "Expected 1 argument"
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
                                            if (type(arguments[0]) is Identifier):
                                                arguments[0] = evaluate(
                                                    arguments[0], environment)
                                            if (type(arguments[1]) is Identifier):
                                                arguments[1] = evaluate(
                                                    arguments[1], environment)
                                            sliced_list = elements[arguments[0]                                                                   : arguments[1]]
                                        except:
                                            report_runtime_error(
                                                line, "List index is out of range")
                                        return ListLiteral(sliced_list, len(sliced_list), line)
                                    case "add":
                                        assert len(
                                            arguments) == 1, "Expected 1 argument"

                                        if (type(arguments[0]) is Identifier):
                                            elements.append(
                                                evaluate(arguments[0], environment))
                                        else:
                                            elements.append(arguments[0])
                                        length += 1
                                        environment.set(left, ListLiteral(
                                            elements, length, line), line, False)
                                        return None
                                    case "at":
                                        assert len(
                                            arguments) == 1, "Expected 1 argument"
                                        try:
                                            ret = arguments[0]

                                            if (type(ret) is Identifier):
                                                return elements[evaluate(ret, environment)]
                                            match ret:
                                                case ListLiteral(elements, length, line):
                                                    return ListLiteral(elements[:], length, line)
                                            return elements[arguments[0]]
                                        except:
                                            report_runtime_error(
                                                line, "Invalid Index")
                                    case "copy":
                                        assert len(
                                            arguments) == 0, "No arguments are expected"
                                        return ListLiteral(elements[:], length, line)
                                    case "pop":
                                        assert len(
                                            arguments) == 1, "Expected 1 argument"
                                        try:
                                            popped = elements.pop(arguments[0])
                                            match popped:
                                                case ListLiteral(elements, length, line):
                                                    return ListLiteral(elements[:], length, line)
                                            return popped
                                        except:
                                            report_runtime_error(
                                                line, "Invalid expression")
                                    case "update":
                                        assert len(
                                            arguments) == 2, "Expected 2 arguments"
                                        try:
                                            if (type(arguments[0]) is Identifier):
                                                arguments[0] = evaluate(arguments[0], environment)
                                            if (type(arguments[1]) is Identifier):
                                                arguments[1] = evaluate(arguments[1], environment)
                                            elements[arguments[0]] = arguments[1]
                                            
                                            return None
                                        except:
                                            report_runtime_error(
                                                line, "Invalid Expression")
                                    case "sort":
                                        assert len(
                                            arguments) == 0, "No arguments are expected"
                                        elements.sort()
                                        return None
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
                                        sliced_str = value[arguments[0]                                                           : arguments[1]]
                                        return StrLiteral(sliced_str, line)
                                    case "at":
                                        assert len(
                                            arguments) == 1, "Expected 1 argument"
                                        try:
                                            ret = arguments[0]
                                            if (type(ret) is Identifier):
                                                arg = evaluate(
                                                    ret, environment)
                                                return value[arg]
                                            # return StrLiteral(value[arguments[0]], line)
                                            return value[arguments[0]]
                                        except:
                                            report_runtime_error(
                                                line, "Invalid index")
                                    case "to_int":
                                        assert len(
                                            arguments) == 0, "No arguments are expected"
                                        try:
                                            return int(value)
                                        except:
                                            report_runtime_error(
                                                line, "Invalid expression")
                                    case "to_float":
                                        assert len(
                                            arguments) == 0, "No arguments are expected"
                                        try:
                                            return float(value)
                                        except:
                                            report_runtime_error(
                                                line, "Invalid expression")
                                    case "to_bool":
                                        assert len(
                                            arguments) == 0, "No arguments are expected"
                                        if (value == "true"):
                                            return True
                                        elif (value == "false"):
                                            return False
                                        else:
                                            report_runtime_error(
                                                line, "Invalid expression")
                                    case "to_list":
                                        assert len(
                                            arguments) == 0, "No arguments are expected"
                                        # Split the string at spaces
                                        # and convert it to a list
                                        return ListLiteral(value.split(), len(value.split()), line)
                                    case "reverse":
                                        assert (len(arguments) == 0), "No arguments are expected" 
                                        return StrLiteral(value[::-1], line)

                                    case _:
                                        report_runtime_error(
                                            line, "Invalid method: string does not have any method: {}".format(method))
                            case DictLiteral(elements, length, line):
                                match method:
                                    case "in_dict":
                                        assert len(
                                            arguments) == 1, "Expected 1 argument"
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
                                        assert len(
                                            arguments) == 2, "Expected 2 arguments"
                                        l = 0
                                        if (arguments[0] not in elements.keys()):
                                            l = 1
                                        elements[arguments[0]] = arguments[1]
                                        environment.set(left, DictLiteral(
                                            elements, length + l, line), line, False)
                                        return None
                                    case "at":
                                        assert len(
                                            arguments) == 1, "Expected 1 argument"
                                        try:
                                            # print(type(elements[arguments[0]]))
                                            ret = elements[arguments[0]]
                                            if (type(ret) is Identifier):
                                                return evaluate(ret, environment)
                                            return ret
                                        except:
                                            report_runtime_error(
                                                line, "Invalid key")
                                    case "update":
                                        assert len(
                                            arguments) == 2, "Expected 2 arguments"
                                        try:
                                            l = 0
                                            if (arguments[0] not in elements.keys()):
                                                l = 1
                                            elements[arguments[0]
                                                     ] = arguments[1]
                                            environment.set(left, DictLiteral(
                                                elements, length + l, line), line, False)
                                            return None
                                        except:
                                            report_runtime_error(
                                                line, "Invalid Expression")
                                    case _:
                                        report_runtime_error(
                                            line, "Invalid method: dict does not have any method: {}".format(method))
                        if type(val) == int:
                            match method:
                                case "to_string":
                                    assert len(
                                        arguments) == 0, "No arguments are expected"
                                    return StrLiteral(str(val), line)
                        if type(val) == str:
                            match method:
                                case "to_int":
                                    assert len(
                                        arguments) == 0, "No arguments are expected"
                                    try:
                                        return int(val)
                                    except:
                                        report_runtime_error(
                                            line, "Invalid expression")
                                case "to_float":
                                    assert len(
                                        arguments) == 0, "No arguments are expected"
                                    try:
                                        return float(val)
                                    except:
                                        report_runtime_error(
                                            line, "Invalid expression")
                                case "to_bool":
                                    assert len(
                                        arguments) == 0, "No arguments are expected"
                                    if (val == "true"):
                                        return True
                                    elif (val == "false"):
                                        return False
                                    else:
                                        report_runtime_error(
                                            line, "Invalid expression")
                                case "to_list":
                                    assert len(
                                        arguments) == 0, "No arguments are expected"
                                    # Split the string at spaces
                                    # and convert it to a list
                                    return ListLiteral(val.split(), len(val.split()), line)

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
            for elem in print_elem:
                print(elem, end="")
            print()
            return None
        case Return(expr, line):
            environment.set("return", evaluate(expr, environment), line, True)
            return ""
        case Stop(line):
            environment.set("stop", 0, line, True)
            return None
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
                        else:
                            return StrLiteral(input_val, line)
                        return input_val
            except:
                report_runtime_error(
                    line, "Error: Invalid input")
    print(program)
    raise InvalidProgram()
