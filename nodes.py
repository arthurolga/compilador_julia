import sys
import re
import copy
from typing import List
from dataclasses import dataclass
from symbols import *

# Symbol Table
# symbolTable = SymbolTable()
functions = SymbolTable()


@dataclass
class Token:
    value: str
    type: str = ""


class Node:
    def __init__(self, value=None, children=None):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable):
        pass

    # def __str__(self):
    #     return ("Node:{} Children:{}".format(
    #         self.value,
    #         str(self.children) if self.children else "No Children"))


class BinOp(Node):
    # Binary Operation. Contem 2 filhos
    def __init__(self, value: str, children: List[Node]):
        if value not in binOperators:
            raise ValueError(
                "<ERROR> BinOp value should be one of {}".format(binOperators))
        self.value = value
        self.children = children

    def evaluate(self, symbolTable):
        # Int to Int Operations
        if self.value == "+":
            return self.children[0].evaluate(
                symbolTable) + self.children[1].evaluate(symbolTable)
        elif self.value == "-":
            return self.children[0].evaluate(
                symbolTable) - self.children[1].evaluate(symbolTable)
        elif self.value == "/":
            return self.children[0].evaluate(
                symbolTable) // self.children[1].evaluate(symbolTable)
        elif self.value == ">":
            return self.children[0].evaluate(
                symbolTable) > self.children[1].evaluate(symbolTable)
        elif self.value == "<":
            return self.children[0].evaluate(
                symbolTable) < self.children[1].evaluate(symbolTable)
        elif self.value == "<":
            return self.children[0].evaluate(
                symbolTable) < self.children[1].evaluate(symbolTable)
        # Bool to int, or bool to bool
        elif self.value == "*":
            if isinstance(self.children[0].evaluate(symbolTable),
                          str) or isinstance(
                              self.children[1].evaluate(symbolTable), str):
                return str(self.children[0].evaluate(symbolTable)) + str(
                    self.children[1].evaluate(symbolTable))
            else:
                return self.children[0].evaluate(
                    symbolTable) * self.children[1].evaluate()
        elif self.value == "&&":
            return self.children[0].evaluate(
                symbolTable) and self.children[1].evaluate(symbolTable)
        elif self.value == "||":
            return self.children[0].evaluate(
                symbolTable) or self.children[1].evaluate(symbolTable)
        elif self.value == "==":
            return self.children[0].evaluate(
                symbolTable) == self.children[1].evaluate(symbolTable)


class UnOp(Node):
    # Unary Operation. Contem um filho
    def evaluate(self, symbolTable):
        if self.value == "+":
            return self.children[0].evaluate(symbolTable)
        elif self.value == "-":
            return -self.children[0].evaluate(symbolTable)
        elif self.value == "!":
            return not self.children[0].evaluate(symbolTable)


class IntVal(Node):
    def __init__(self, value: str, children=None):
        self.value = int(value)
        if children: raise ValueError("<ERROR> IntVal should have no children")

    # Integer value. Não contem filhos
    def evaluate(self, symbolTable):
        return int(self.value)


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
    def evaluate(self, symbolTable):
        return self.value


class StringVal(Node):
    def __init__(self, value: str, children=None):
        self.value = value
        if children:
            raise ValueError("<ERROR> StringVal should have no children")

    # Integer value. Não contem filhos
    def evaluate(self, symbolTable):
        return self.value


class NoOp(Node):
    #  No Operation (Dummy). Não contem filhos
    def evaluate(self, symbolTable):
        pass


class Identifier(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, symbolTable):
        return symbolTable._get(self.value).value


class Declare(Node):
    def evaluate(self, symbolTable):
        if len(self.children) == 2:
            # Creates empty symbol
            if self.children[1] in availableSymbolTypes:
                _symbol = Symbol(name=self.children[0],
                                 symbolType=self.children[1],
                                 value=None)
                symbolTable._set(self.children[0], _symbol)
            else:
                raise ValueError("<ERROR> Unrecognized symbol {}".format(
                    self.children[1]))
        else:
            raise ValueError("<ERROR> Declare should have 2 children")


class Assignment(Node):
    def evaluate(self, symbolTable):
        if len(self.children) == 2:
            # e.g. symbolTable["test"] = 10
            value = self.children[1].evaluate(symbolTable)
            isInt = isinstance(value, int)
            isBool = isinstance(value, bool)
            isString = isinstance(value, str)
            if self.children[0] in symbolTable.symbols:
                tableValueType = symbolTable._get(self.children[0]).type
                # Regular type
                if (isInt and tableValueType
                        == "Int") or (isBool and tableValueType == "Bool") or (
                            isString and tableValueType == "String"):
                    symbolTable._setOnlyValue(self.children[0], value)
                # Int with Bool
                elif (isInt and tableValueType == "Bool"):
                    symbolTable._setOnlyValue(self.children[0], bool(value))

                else:
                    raise ValueError(
                        "<ERROR> Unexpected Type of Value of {}".format(value))
            else:
                # if isInt:
                #     valueType = "Int"
                # elif isBool:
                #     valueType = "Bool"
                # elif isString:
                #     valueType = "String"
                # else:
                #     raise ValueError(
                #         "<ERROR> Unexpected Type of Value of {}".format(value))
                # _symbol = Symbol(name=self.children[0],
                #                  symbolType=valueType,
                #                  value=value)
                # symbolTable._set(self.children[0], _symbol)
                raise ValueError("<ERROR> Not declared at assignment")

        else:
            raise ValueError("<ERROR> Assignment should have 2 children")


class Statement(Node):
    def evaluate(self, symbolTable):
        for child in self.children:
            child.evaluate(symbolTable)
            isReturn = isinstance(child, ReturnOp)
            if isReturn:
                break


class Print(Node):
    # println operation
    def evaluate(self, symbolTable):
        print(self.children[0].evaluate(symbolTable))


class Readline(Node):
    # readline operation
    def evaluate(self, symbolTable):
        res = int(input())
        return res


class WhileOp(Node):
    def __init__(self, value: str, children=None):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable):
        while (self.children[0].evaluate(symbolTable)):
            self.children[1].evaluate(symbolTable)


class IfOp(Node):
    def evaluate(self, symbolTable):
        value = self.children[0].evaluate(symbolTable)
        if (isinstance(value, str)):
            raise ValueError("<ERROR> Can't check strings as bool")

        if (value):
            self.children[1].evaluate(symbolTable)
        else:
            if len(self.children) == 3:
                self.children[2].evaluate(symbolTable)


class ReturnOp(Node):
    def __init__(self, command):
        self.command = command

    def evaluate(self, symbolTable: SymbolTable):
        _node = self.command
        res = _node.evaluate(symbolTable)
        _type = None
        if isinstance(res, str):
            _type = "String"
        elif isinstance(res, bool):
            _type = "Bool"
        elif isinstance(res, int):
            _type = "Int"

        symb = Symbol(name="return", symbolType=_type, value=res)
        symbolTable._set_return(symb)


class FuncDec(Node):
    def __init__(self, name, arguments, symbolType, commands):
        self.children = arguments
        self.name = name
        self.symbolType = symbolType
        self.commands = commands

    def evaluate(self, symbolTable):
        funcSymbol = Symbol(self.name, self.symbolType, self)
        functions._def(self.name, funcSymbol)

    def __str__(self):
        return 'Name: {} Children: {} symbolType: {}'.format(
            self.name, self.children, self.symbolType)


class CallFunc(Node):
    def __init__(self, value, arguments):
        self.value = value
        self.children = arguments

    def evaluate(self, symbolTable):
        function = functions._get_function(self.value)
        functionNode = function.value

        funcSymbolTable = SymbolTable()

        if (len(functionNode.children) == len(self.children)):
            i = 0
            for var in functionNode.children:
                symb = Symbol(var.children[0], var.children[1],
                              self.children[i].evaluate(symbolTable))
                funcSymbolTable._set(var.children[0], symb)
                i += 1
        else:
            raise ValueError("<ERROR> Wrong number of arguments")
        # print(functionNode)
        # print(len(functionNode.children))
        # print("mamus")

        functionNode.commands.evaluate(funcSymbolTable)
        result = funcSymbolTable._get_return()
        if (result.type == function.type):
            return result.value
        else:
            raise ValueError("<ERROR> Wrong type of return at {}".format(
                function.name))


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


if __name__ == "__main__":
    main()
