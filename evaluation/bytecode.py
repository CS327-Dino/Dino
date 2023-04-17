from tokenizing.token_scanning import *
from datatypes.datatypes import *
from errors.error import *
from enum import Enum
from dataclasses import dataclass
from typing import List


class Op(Enum):
    ADD = 1
    SUB = 2
    MUL = 3
    DIV = 4
    MOD = 5
    NEG = 6
    NOT = 7
    AND = 8
    OR = 9
    XOR = 10
    EQUAL = 11
    NOT_EQUAL = 12
    GREATER = 13
    GREATER_EQUAL = 14
    LESS = 15
    LESS_EQUAL = 16
    POW = 19
    POP = 23
    RETURN = 24

    def __repr__(self):
        return f"{self.name}"


class I:
    @dataclass
    class Push:
        value: int

    @dataclass
    class List:
        value: int

    @dataclass
    class PushFN:
        index: int
        address: int

    @dataclass
    class Call:
        index: int

    @dataclass
    class Load:
        index: int

    @dataclass
    class Store:
        index: int

    @dataclass
    class Jmp:
        address: int

    @dataclass
    class JmpIfFalse:
        address: int

    @dataclass
    class JmpIfTrue:
        address: int

    @dataclass
    class JmpIfFalseOrPop:
        address: int

    @dataclass
    class JmpIfTrueOrPop:
        address: int

    def __repr__(self):
        return f"{self.name}"


@dataclass
class Label:
    address: int


simpleOP = {
    TokenType.PLUS: Op.ADD,
    TokenType.MINUS: Op.SUB,
    TokenType.STAR: Op.MUL,
    TokenType.SLASH: Op.DIV,
    TokenType.MOD: Op.MOD,
    TokenType.EQUAL_EQUAL: Op.EQUAL,
    TokenType.BANG_EQUAL: Op.NOT_EQUAL,
    TokenType.GREATER: Op.GREATER,
    TokenType.GREATER_EQUAL: Op.GREATER_EQUAL,
    TokenType.LESS: Op.LESS,
    TokenType.LESS_EQUAL: Op.LESS_EQUAL,
    TokenType.BANG: Op.NOT,
}


@dataclass
class Bytecode:
    def __init__(self):
        self.code = []

    def label(self):
        return Label(-1)

    def emit(self, instruction: I):
        self.code.append(instruction)

    def emit_label(self, label: Label):
        label.address = len(self.code)

    def bytecode_generator(self, prog):
        match prog:
            case IntLiteral(value) | NumLiteral(value) | StrLiteral(value) | BoolLiteral(value) | NullLiteral(value):
                self.emit(I.Push(value))
            case BinOp(left, op, right) if op in simpleOP:
                self.bytecode_generator(left)
                self.bytecode_generator(right)
                self.emit(simpleOP[op])
            case BinOp(left, TokenType.AND, right):
                self.bytecode_generator(left)
                else_label = self.label()
                self.emit(I.JmpIfFalseOrPop(else_label))
                self.bytecode_generator(right)
                self.emit_label(else_label)
            case BinOp(left, TokenType.OR, right):
                self.bytecode_generator(left)
                else_label = self.label()
                self.emit(I.JmpIfTrueOrPop(else_label))
                self.bytecode_generator(right)
                self.emit_label(else_label)
            case If(condition, then, else_):
                self.bytecode_generator(condition)
                else_label = self.label()
                self.emit(I.JmpIfFalse(else_label))
                self.bytecode_generator(then)
                end_label = self.label()
                self.emit(I.Jmp(end_label))
                self.emit_label(else_label)
                self.bytecode_generator(else_)
                self.emit_label(end_label)
            case Seq(things):
                for thing in things[:-1]:
                    self.bytecode_generator(thing)
                    # self.emit(I.POP)
                    self.emit(Op.POP)
                self.bytecode_generator(things[-1])
            case Assignment(name, value):
                self.bytecode_generator(value)
                # self.emit(I.Store(name))
                self.emit(I.Store(name.uid))
                self.emit(I.Push(None))
            case ListLiteral(elements, length, line):
                for element in elements:
                    self.bytecode_generator(element)
                self.emit(I.List(length))
            case Identifier(_) as iden:
                # self.emit(I.Load(iden))
                self.emit(I.Load(iden.uid))
            case Loop(condition, body):
                condition_label = self.label()
                self.emit_label(condition_label)
                self.bytecode_generator(condition)
                end_label = self.label()
                self.emit(I.JmpIfFalse(end_label))
                self.bytecode_generator(body)
                self.emit(I.Jmp(condition_label))
                self.emit_label(end_label)
            case Function(name, _, body):
                FBEGIN = self.label()
                FEND = self.label()
                self.emit(I.Jmp(FEND))
                self.emit_label(FBEGIN)
                self.bytecode_generator(body)
                self.emit(Op.RETURN)
                self.emit_label(FEND)
                self.emit(I.PushFN(name.uid, FBEGIN.address))
                # self.emit(I.Store(name))
                # self.emit(I.Store(name.uid))
                self.emit(I.Push(None))
            case Call(name, _):
                self.emit(I.Call(name.uid))


@dataclass
class Frame:
    def __init__(self, retaddr=-1, parent=None):
        MAX_LOCALS = 32
        self.locals = [None] * MAX_LOCALS
        self.retaddr = retaddr
        self.parent = parent


class VM:
    def __init__(self, code) -> None:
        self.code = code
        self.stack = []
        self.Frame = Frame()
        self.ip = 0

    def run(self):
        while self.ip < len(self.code):
            # print(self.stack)
            match self.code[self.ip]:
                case I.List(length):
                    temp = []
                    for _ in range(length):
                        temp.append(self.stack.pop())
                    self.stack.append(temp[::-1])
                    self.ip += 1
                case I.Push(value):
                    self.stack.append(value)
                    self.ip += 1
                case I.PushFN(index, address):
                    self.Frame.locals[index] = address
                    # self.stack.append(address.address)
                    self.ip += 1
                case I.Call(index):
                    jmpip = self.Frame.locals[index]
                    self.Frame = Frame(self.ip + 1, self.Frame)
                    self.ip = jmpip
                case Op.RETURN:
                    self.ip = self.Frame.retaddr
                    self.Frame = self.Frame.parent
                case I.Load(index):
                    self.stack.append(self.Frame.locals[index])
                    # print("L", self.Frame.locals[index])
                    self.ip += 1
                case I.Store(index):
                    self.Frame.locals[index] = self.stack.pop()
                    # print("L", self.Frame.locals[index])
                    self.ip += 1
                case I.Jmp(address):
                    self.ip = address.address
                case I.JmpIfFalse(address):
                    if not self.stack.pop():
                        self.ip = address.address
                    else:
                        self.ip += 1
                case I.JmpIfTrue(address):
                    if self.stack.pop():
                        self.ip = address.address
                    else:
                        self.ip += 1
                case I.JmpIfFalseOrPop(address):
                    if not self.stack.pop():
                        self.ip = address.address
                    else:
                        self.stack.pop()
                        self.ip += 1
                case I.JmpIfTrueOrPop(address):
                    if self.stack.pop():
                        self.ip = address.address
                    else:
                        self.stack.pop()
                        self.ip += 1
                case Op.ADD:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left + right)
                    self.ip += 1
                case Op.SUB:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left - right)
                    self.ip += 1
                case Op.MUL:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left * right)
                    self.ip += 1
                case Op.DIV:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left / right)
                    self.ip += 1
                case Op.MOD:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left % right)
                    self.ip += 1
                case Op.NEG:
                    self.stack.append(-1*self.stack.pop())
                    self.ip += 1
                case Op.NOT:
                    self.stack.append(not self.stack.pop())
                    self.ip += 1
                case Op.AND:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left and right)
                    self.ip += 1
                case Op.OR:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left or right)
                    self.ip += 1
                case Op.XOR:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left ^ right)
                    self.ip += 1
                case Op.EQUAL:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left == right)
                    self.ip += 1
                case Op.NOT_EQUAL:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left != right)
                    self.ip += 1
                case Op.GREATER:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left > right)
                    self.ip += 1
                case Op.GREATER_EQUAL:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left >= right)
                    self.ip += 1
                case Op.LESS:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left < right)
                    self.ip += 1
                case Op.LESS_EQUAL:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left <= right)
                    self.ip += 1
                case Op.POW:
                    right = self.stack.pop()
                    left = self.stack.pop()
                    self.stack.append(left ** right)
                    self.ip += 1
                case Op.POP:
                    self.stack.pop()
                    self.ip += 1
        return self.stack.pop()
