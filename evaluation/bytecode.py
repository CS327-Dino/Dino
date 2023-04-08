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
    LOAD = 28
    STORE = 29

    def __repr__(self):
        return f"{self.name}"

class I:
    @dataclass
    class Push:
        value: int
    
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
        def gen_(program):
            self.bytecode_generator(program)

        match prog:
            case IntLiteral(value) | NumLiteral(value) | StrLiteral(value) | BoolLiteral(value) | NullLiteral(value):
                self.emit(I.Push(value))
            case BinOp(left, op, right) if op in simpleOP:
                gen_(left)
                gen_(right)
                self.emit(simpleOP[op])
            case BinOp(left, TokenType.AND, right):
                gen_(left)
                else_label = self.label()
                self.emit(I.JmpIfFalseOrPop(else_label))
                gen_(right)
                self.emit_label(else_label)
            case BinOp(left, TokenType.OR, right):
                gen_(left)
                else_label = self.label()
                self.emit(I.JmpIfTrueOrPop(else_label))
                gen_(right)
                self.emit_label(else_label)
            case If(condition, then, else_):
                gen_(condition)
                else_label = self.label()
                self.emit(I.JmpIfFalse(else_label))
                gen_(then)
                end_label = self.label()
                self.emit(I.Jmp(end_label))
                self.emit_label(else_label)
                gen_(else_)
                self.emit_label(end_label)
            case Seq(things):
                for thing in things:
                    gen_(thing)
