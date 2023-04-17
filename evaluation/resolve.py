from tokenizing.token_scanning import *
from datatypes.datatypes import *
from errors.error import *
from .eval import *

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