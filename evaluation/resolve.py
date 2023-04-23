from tokenizing.token_scanning import *
from datatypes.datatypes import *
from errors.error import *
from .eval import *
import sys
sys.setrecursionlimit(10000)


def resolution(program: AST, environment: Scope = Scope()):
    if program is None:
        return None
    match program:
        case NumLiteral(value, line) as n:
            return n
        case IntLiteral(value, line) as i:
            return i
        case BoolLiteral(value, line) as b:
            return b
        case StrLiteral(value, line) as s:
            return s
        case Assignment(Identifier(name) as iden, value, line, declaration):
            value = resolution(value, environment)
            if declaration:
                environment.set(name, iden, line, True)
                return Assignment(Identifier(name, iden.line, iden.isconst, iden.uid), value, line, declaration)
            else:
                reiden = environment.get(name, line)
                return Assignment(Identifier(name, iden.line, reiden.isconst, reiden.uid), value, line, declaration)
        case ParallelAssignment(list_identifiers, list_values, line, declaration):
            for i in range(len(list_values)):
                list_values[i] = resolution(list_values[i], environment)
            if declaration:
                for i in list_identifiers:
                    environment.set(i.name, i, line, True)
            else:
                for i in list_identifiers:
                    reiden = environment.get(i.name, line)
                    environment.set(i.name, Identifier(i.name, i.line, reiden.isconst, reiden.uid), line, True)
            return ParallelAssignment(list_identifiers, list_values, line, declaration)
        
        case Identifier(name, line) as iden:
            reiden = environment.get(name, line)
            return Identifier(name, iden.line, reiden.isconst, reiden.uid)
        case Seq(things):
            output = []
            for thing in things:
                output.append(resolution(thing, environment))
            return Seq(output)
        case Echo(expr, line):
            elem_resolve = []
            for elem in expr:
                elem_resolve.append(resolution(elem, environment))
            return Echo(elem_resolve, line)
        case Return(expr, line):
            return Return(resolution(expr, environment), line)
        case Stop(line):
            return Stop(line)
        case BinOp(left, op, right, line):
            return BinOp(resolution(left, environment), op, resolution(right, environment), line)
        case UnOp(op, right, line):
            return UnOp(op, resolution(right, environment), line)
        case ListLiteral(elements, length, line):
            output = []
            for i in elements:
                output.append(resolution(i, environment))
            return ListLiteral(output, length, line)
        case DictLiteral(elements, length, line):
            for i in elements.keys():
                elements[i] = resolution(elements[i], environment)
            return DictLiteral(elements, length, line)
        case Lambda(Identifier(name), e1, e2, line):
            e1 = resolution(e1, environment)
            newEnv = Scope(environment)
            newIden = Identifier(name, line, True)
            newEnv.set(name, newIden, line, True)
            # print(newEnv)
            e2 = resolution(e2, newEnv)
            del newEnv
            return Lambda(newIden, e1, e2, line)
        case ParallelLambda(list_identifiers, list_expressions, e2, line):
            
            for i in range(len(list_expressions)):
                list_expressions[i] = resolution(list_expressions[i], environment)
            
            newEnv = Scope(environment)
            newIden =[]

            for i in list_identifiers:
                newIden.append(Identifier(i.name, line, True))
                newEnv.set(i.name, newIden[-1], line, True)
            
            e2 = resolution(e2, newEnv)
            del newEnv
            return ParallelLambda(newIden, list_expressions, e2, line)
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
        case Iterate(iterable, condition, increment, body):
            iterable = resolution(iterable, environment)
            condition = resolution(condition, environment)
            increment = resolution(increment, environment)
            newEnv = Scope(environment)
            body = resolution(body, newEnv)
            del newEnv
            return Iterate(iterable, condition, increment, body)
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
        case Abort(msg, line):
            return Abort(msg, line)
        case Capture(msg, line):
            return Capture(msg, line)

    print(program)
    raise InvalidProgram()
