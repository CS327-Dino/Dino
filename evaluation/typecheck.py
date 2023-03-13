from tokenizing.token_scanning import *
from datatypes.datatypes import *
from errors.error import *
from .eval import *
from enum import Enum

class LiteralType(Enum):
    INT = 1
    FLOAT = 2
    BOOL = 3
    NULL = 4
    STR = 5
    LIST = 6

# def typechecking(program: AST, typeerror: DinoError = DinoError()):
#     typecheck(program, Scope(), typeerror)

def typecheck(program: AST, environment: Scope = Scope(), typeerror: DinoError = DinoError()):
    def _type(program):
        return typecheck(program, environment, typeerror)
    if program is None:
        return None
    match program:
        case NumLiteral(value, line):
            return LiteralType.FLOAT
        case IntLiteral(value, line):
            return LiteralType.INT
        case BoolLiteral(value, line):
            return LiteralType.BOOL
        case StrLiteral(value, line):
            return LiteralType.STR
        case ListLiteral(elements, length, line):
            for i in elements:
                _type(i)
            return LiteralType.LIST
        case Assignment(Identifier(name) as iden, value, line, declaration):
            value = _type(value)
            if declaration:
                environment.set(name, value, line, declaration)
            elif iden.isconst == True:
                # print("HIii")
                typeerror.line = line
                typeerror.message = "TypeError: Cannot reassign a constant"
                typeerror.triggered = True
                report_error(typeerror)
            return value
        case Identifier(name, line) as iden:
            return environment.get(name, line)
        case Seq(things):
            output = None
            for thing in things:
                output = _type(thing)
            return output
        case Echo(expr, line):
            return _type(expr)
        case Return(expr, line):
            return _type(expr)
        case BinOp(left, op, right, line):
            typedLeft = _type(left)
            typedRight = _type(right)
            if typedLeft == LiteralType.INT and typedRight == LiteralType.INT:
                match op:
                    case TokenType.MINUS | TokenType.PLUS | TokenType.STAR | TokenType.SLASH | TokenType.EXPONENT | TokenType.BIT_AND | TokenType.BIT_OR: return LiteralType.INT
                    case TokenType.EQUAL_EQUAL | TokenType.BANG_EQUAL | TokenType.GREATER | TokenType.GREATER_EQUAL | TokenType.LESS | TokenType.LESS_EQUAL: return LiteralType.BOOL
                    case _: 
                        print("Error: Invalid operation on INT")
                        return None
            elif (typedLeft == LiteralType.FLOAT or typedLeft == LiteralType.INT)  and (typedRight == LiteralType.FLOAT or typedRight == LiteralType.INT):
                match op:
                    case TokenType.MINUS | TokenType.PLUS | TokenType.STAR | TokenType.SLASH | TokenType.EXPONENT: return LiteralType.FLOAT
                    case TokenType.EQUAL_EQUAL | TokenType.BANG_EQUAL | TokenType.GREATER | TokenType.GREATER_EQUAL | TokenType.LESS | TokenType.LESS_EQUAL: return LiteralType.BOOL
                    case _: 
                        print("Error: Invalid operation on float")
                        return None
        
            elif typedLeft == LiteralType.BOOL and typedRight == LiteralType.BOOL:
                match op:
                    case TokenType.EQUAL_EQUAL | TokenType.BANG_EQUAL | TokenType.OR | TokenType.AND: return LiteralType.BOOL
                    case _: 
                        print("Error: Invalid operation on Bool")
                        return None
            elif typedLeft == LiteralType.STR and typedRight == LiteralType.STR:
                match op:
                    case TokenType.PLUS: return LiteralType.STR
                    case _:
                        print("Error: Invalid operation on String")
                        return None

            elif typedLeft == LiteralType.LIST:
                return LiteralType.LIST
            else:
                typeerror.line = line
                typeerror.message = "TypeError: Cannot perform operation on incompatible types"
                typeerror.triggered = True
                report_error(typeerror)
            return None
                
        case UnOp(op, right, line):
            typedRight = _type(right)
            if typedRight == LiteralType.INT:
                match op:
                    case TokenType.INCREMENT | TokenType.DECREMENT | TokenType.MINUS: return LiteralType.INT
                    case _: 
                        print("Error: Invalid operation on INT")
                        return None
            elif typedRight == LiteralType.FLOAT:
                match op:
                    case TokenType.INCREMENT | TokenType.DECREMENT | TokenType.MINUS: return LiteralType.FLOAT
                    case _: 
                        print("Error: Invalid operation on float")
                        return None
            elif typedRight == LiteralType.BOOL:
                match op:
                    case TokenType.BANG: return LiteralType.BOOL
                    case _: 
                        print("Error: Invalid operation on float")
                        return None

            else:
                typeerror.line = line
                typeerror.message = "TypeError: Cannot perform operation on incompatible types"
                typeerror.triggered = True
        case Lambda(Identifier(name), e1, e2, line):
            e1 = _type(e1)
            newEnv = Scope(environment)
            newEnv.set(name, e1, line, True)
            # print(newEnv)
            e2 = typecheck(e2, newEnv, typeerror)
            del newEnv
            return e2
        case If(e0, e1, e2):
            line = e0.line
            e0 = _type(e0)
            if e0 != LiteralType.BOOL:
                typeerror.line = line
                typeerror.message = "TypeError: Conditional in IF must have bool type"
                typeerror.triggered = True
                report_error(typeerror)
            newEnv = Scope(environment)
            e1 = typecheck(e1, newEnv, typeerror)
            del newEnv
            newEnv = Scope(environment)
            e2 = typecheck(e2, newEnv, typeerror)
            del newEnv
            if e1 != e2:
                typeerror.line = line
                typeerror.message = "TypeError: Both IF branches must have same type"
                typeerror.triggered = True
                report_error(typeerror)
            return e1
        case Loop(condition, body):
            line = condition.line
            condition = _type(condition)
            if condition != LiteralType.BOOL:
                typeerror.line = line
                typeerror.message = "TypeError: Conditional in LOOP must have bool type"
                typeerror.triggered = True
                report_error(typeerror)
            newEnv = Scope(environment)
            body = typecheck(body, newEnv, typeerror)
            del newEnv
            return body
        case Function(name, args, body, line):
            environment.set(name.name, name, line, True)
            newEnv = Scope(environment)
            for i in args:
                newEnv.set(i.name, i, line, True)
            body = typecheck(body, newEnv, typeerror)
            del newEnv
            return Function(name, args, body, line)
        case Call(name, args, line):
            args = [_type(i) for i in args]
            return Call(_type(name), args, line)
        case MethodLiteral(name, args, line):
            args = [_type(i) for i in args]
            return MethodLiteral(name, args, line)
        case Abort(msg, line):
            return Abort(msg, line)
        case Capture(msg, line):
            return Capture(msg, line)

    print(program)
    raise InvalidProgram()
    