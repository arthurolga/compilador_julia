import sys
import re
import copy
from typing import List
from dataclasses import dataclass
from symbols import *
from compiler import compiler

# Symbol Table
symbolTable = SymbolTable()


@dataclass
class Token:
    value: str
    type: str = ""


class Node:
    
    i=0

    def __init__(self, value=None, children=None):
        self.value = value
        self.children = children
        self.i = Node.newId()


    def evaluate(self):
        pass

    def __str__(self):
        return ("Node:{} Children:{}".format(str(self.value), str(self.children)))

    @staticmethod
    def newId():
        Node.i +=1
        return Node.i


class BinOp(Node):
    # Binary Operation. Contem 2 filhos
    def __init__(self, value: str, children: List[Node]):
        if value not in binOperators:
            raise ValueError(
                "<ERROR> BinOp value should be one of {}".format(binOperators))
        self.value = value
        self.children = children

    def evaluate(self):
        # Int to Int Operations
        if self.value == "+":
            #return self.children[0].evaluate() + self.children[1].evaluate()
            self.children[0].evaluate()
            compiler.writeLine("PUSH EBX")
            self.children[1].evaluate()
            compiler.writeLine("POP EAX")
            compiler.writeLine("ADD EAX, EBX")
            compiler.writeLine("MOV EBX, EAX")

        elif self.value == "-":
            #return self.children[0].evaluate() - self.children[1].evaluate()
            self.children[0].evaluate()
            compiler.writeLine("PUSH EBX")
            self.children[1].evaluate()
            compiler.writeLine("POP EAX")
            compiler.writeLine("SUB EAX, EBX")
            compiler.writeLine("MOV EBX, EAX")

        elif self.value == "/":
            #return self.children[0].evaluate() // self.children[1].evaluate()
            self.children[0].evaluate()
            compiler.writeLine("PUSH EBX")
            self.children[1].evaluate()
            compiler.writeLine("POP EAX")
            compiler.writeLine("DIV EAX, EBX")
            compiler.writeLine("MOV EBX, EAX")

        elif self.value == ">":
            #return self.children[0].evaluate() > self.children[1].evaluate()
            self.children[0].evaluate()
            compiler.writeLine("PUSH EBX")
            self.children[1].evaluate()
            compiler.writeLine("POP EAX")
            compiler.writeLine("CMP EAX, EBX")
            compiler.writeLine("CALL binop_jg")

        elif self.value == "<":
            #return self.children[0].evaluate() < self.children[1].evaluate()
            self.children[0].evaluate()
            compiler.writeLine("PUSH EBX")
            self.children[1].evaluate()
            compiler.writeLine("POP EAX")
            compiler.writeLine("CMP EAX, EBX")
            compiler.writeLine("CALL binop_jl")

        # Bool to int, or bool to bool
        elif self.value == "*":
            # if isinstance(self.children[0].evaluate(), str):
            #     return self.children[0].evaluate() + str(
            #         self.children[1].evaluate())
            # else:
            #return self.children[0].evaluate() * self.children[1].evaluate()
            self.children[0].evaluate()
            compiler.writeLine("PUSH EBX")
            self.children[1].evaluate()
            compiler.writeLine("POP EAX")
            compiler.writeLine("IMUL EBX")
            compiler.writeLine("MOV EBX, EAX")

        elif self.value == "&&":
            #return self.children[0].evaluate() and self.children[1].evaluate()
            self.children[0].evaluate()
            compiler.writeLine("PUSH EBX")
            self.children[1].evaluate()
            compiler.writeLine("POP EAX")
            compiler.writeLine("AND EAX, EBX")
            compiler.writeLine("MOV EBX, EAX")

        elif self.value == "||":
            #return self.children[0].evaluate() or self.children[1].evaluate()
            self.children[0].evaluate()
            compiler.writeLine("PUSH EBX")
            self.children[1].evaluate()
            compiler.writeLine("POP EAX")
            compiler.writeLine("OR EAX, EBX")
            compiler.writeLine("MOV EBX, EAX")
            
        elif self.value == "==":
            #return self.children[0].evaluate() == self.children[1].evaluate()
            self.children[0].evaluate()
            compiler.writeLine("PUSH EBX")
            self.children[1].evaluate()
            compiler.writeLine("POP EAX")
            compiler.writeLine("CMP EAX, EBX")
            compiler.writeLine("CALL binop_je")


class UnOp(Node):
    # Unary Operation. Contem um filho
    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate()
        elif self.value == "-":
            return -self.children[0].evaluate()
        elif self.value == "!":
            return not self.children[0].evaluate()


class IntVal(Node):
    def __init__(self, value: str, children=None):
        self.value = int(value)
        if children: raise ValueError("<ERROR> IntVal should have no children")

    # Integer value. Não contem filhos
    def evaluate(self):
        #return int(self.value)
        compiler.writeLine(f'MOV EBX, {self.value}')
        #MOV EBX, 3 


class BoolVal(Node):
    def __init__(self, value: str, children=None):
        if value == "true":
            self.value = True
        elif value == "false":
            self.value = False
        else:
            raise ValueError(
                "<ERROR> BoolVal should be true of false, instead assigned:{}".
                format(value))
        if children:
            raise ValueError("<ERROR> BoolVal should have no children")

    # Bool value. Não contem filhos
    def evaluate(self):
        if self.value:
            compiler.writeLine('CALL binop_true')
        else:
            compiler.writeLine('CALL binop_true')
        #return self.value


class StringVal(Node):
    def __init__(self, value: str, children=None):
        self.value = value
        if children:
            raise ValueError("<ERROR> StringVal should have no children")

    # Integer value. Não contem filhos
    def evaluate(self):
        return self.value


class NoOp(Node):
    #  No Operation (Dummy). Não contem filhos
    def evaluate(self):
        pass


class Identifier(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        #return symbolTable._get(self.value).value
        pos = symbolTable._get(self.value).pos
        compiler.writeLine(f"MOV EBX, [EBP-{pos}]")


class Declare(Node):
    def evaluate(self):
        if len(self.children) == 2:
            # Creates empty symbol
            if self.children[1] in availableSymbolTypes:
                _symbol = Symbol(name=self.children[0],
                                 symbolType=self.children[1],
                                 size=4,
                                 value=None)
                symbolTable._set(self.children[0], _symbol)

                compiler.writeLine("PUSH DWORD 0")
            else:
                raise ValueError("<ERROR> Unrecognized symbol {}".format(
                    self.children[1]))
        else:
            raise ValueError("<ERROR> Declare should have 2 children")


class Assignment(Node):
    def evaluate(self):
        if len(self.children) == 2:
            self.children[1].evaluate()
            # if self.children[0] not in symbolTable.symbols:
            #     _symbol = Symbol(name=self.children[0],
            #                      symbolType=None,
            #                      size=4,
            #                      value=None)
            #     symbolTable._set(self.children[0], _symbol)

            #     compiler.writeLine("PUSH DWORD 0")
            #print(symbolTable)
            pos = symbolTable._get(self.children[0]).pos
            compiler.writeLine(f"MOV [EBP-{pos}], EBX")
            # # e.g. symbolTable["test"] = 10
            # value = self.children[1].evaluate()
            # isInt = isinstance(value, int)
            # isBool = isinstance(value, bool)
            # isString = isinstance(value, str)
            # if self.children[0] in symbolTable.symbols:
            #     tableValueType = symbolTable._get(self.children[0]).type
            #     # Regular type
            #     if (isInt and tableValueType
            #             == "Int") or (isBool and tableValueType == "Bool") or (
            #                 isString and tableValueType == "String"):
            #         symbolTable._setOnlyValue(self.children[0], value)
            #     # Int with Bool
            #     elif (isInt and tableValueType == "Bool"):
            #         symbolTable._setOnlyValue(self.children[0], bool(value))

            #     else:
            #         raise ValueError(
            #             "<ERROR> Unexpected Type of Value of {}".format(value))
            # else:
            #     if isInt:
            #         valueType = "Int"
            #     elif isBool:
            #         valueType = "Bool"
            #     elif isString:
            #         valueType = "String"
            #     else:
            #         raise ValueError(
            #             "<ERROR> Unexpected Type of Value of {}".format(value))
            #     _symbol = Symbol(name=self.children[0],
            #                      symbolType=valueType,
            #                      value=value)
            #     symbolTable._set(self.children[0], _symbol)

        else:
            raise ValueError("<ERROR> Assignment should have 2 children")


class Statement(Node):
    def evaluate(self):
        for child in self.children:
            child.evaluate()


class Print(Node):
    # println operation
    def evaluate(self):
        #print(self.children[0].evaluate())
        self.children[0].evaluate()
        compiler.writeLine("PUSH EBX ")
        compiler.writeLine("CALL print ")
        compiler.writeLine("POP EBX ")


class Readline(Node):
    # readline operation
    def evaluate(self):
        res = int(input())
        return res


class WhileOp(Node):
    def __init__(self, value: str, children=None):
        self.value = value
        self.children = children

    def evaluate(self):
        # while (self.children[0].evaluate()):
        #     self.children[1].evaluate()
        compiler.writeLine(f"LOOP_{self.i}:")
        self.children[0].evaluate()
        #print(self.children[0])
        compiler.writeLine("CMP EBX, False ")
        compiler.writeLine(f"JE EXIT_{self.i}")
        self.children[1].evaluate()
        #print(self.children[1])
        compiler.writeLine(f"JMP LOOP_{self.i}")
        compiler.writeLine(f"EXIT_{self.i}: ")



class IfOp(Node):
    def evaluate(self):
        self.children[0].evaluate()
        compiler.writeLine("CMP EBX, False ")
        compiler.writeLine(f"JE EXIT_{self.i}")
        self.children[1].evaluate()
        compiler.writeLine(f"EXIT_{self.i}: ")

        if len(self.children) > 2 and self.children[2]:
            self.children[0].evaluate()
            compiler.writeLine("CMP EBX, False ")
            compiler.writeLine(f"JE EXIT_ELSE_{self.i}")
            self.children[2].evaluate()
            compiler.writeLine(f"EXIT_ELSE_{self.i}: ")

        # if (self.children[0].evaluate()):
        #     self.children[1].evaluate()
        # else:
        #     if len(self.children) == 3:
        #         self.children[2].evaluate()


# Available Operations
TERM_OP = "TERM_OP"
termOperators = ("/", "*")
EXP_OP = "EXP_OP"
expOperators = ("+", "-")
FACT_OP = "FACT_OP"
factOperators = ("(", ")")

binOperators = ("+", "-", "*", "/", ">", "<", "&&", "||", "==")  #Ex: 1+1
unOperators = ("+", "-")  #-1
allOperators = termOperators + expOperators + factOperators
# Number
NUMBER = "NUMBER"

EOF = 'EOF'


def main():
    A = IntVal(1)
    B = IntVal(2)
    BIN_1 = BinOp("*", [A, B])
    BIN_2 = BinOp("/", [A, B])
    BIN_3 = BinOp("+", [BIN_1, BIN_2])
    print(BIN_3.evaluate())


if __name__ == "__main__":
    main()
