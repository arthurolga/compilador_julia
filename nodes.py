import sys
import re
import copy
from typing import List
from dataclasses import dataclass


@dataclass
class Token:
    value: str
    type: str = ""


class Node:
    def __init__(self, value=None, children=None):
        self.value = value
        self.children = children

    def evaluate(self):
        pass

    def __str__(self):
        return ("Node:{} Children:{}".format(self.value, str(self.children)))


class BinOp(Node):
    # Binary Operation. Contem 2 filhos
    def __init__(self, value: str, children: List[Node]):
        if value not in binOperators:
            raise ValueError(
                "<ERROR> BinOp value should be one of {}".format(binOperators))
        self.value = value
        self.children = children

    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate() + self.children[1].evaluate()
        elif self.value == "-":
            return self.children[0].evaluate() - self.children[1].evaluate()
        elif self.value == "/":
            return self.children[0].evaluate() // self.children[1].evaluate()
        elif self.value == "*":
            return self.children[0].evaluate() * self.children[1].evaluate()


class UnOp(Node):
    # Unary Operation. Contem um filho
    def evaluate(self):
        if self.value == "+":
            return self.children[0].evaluate()
        elif self.value == "-":
            return -self.children[0].evaluate()


class IntVal(Node):
    def __init__(self, value: str, children=None):
        self.value = int(value)
        if children: raise ValueError("<ERROR> IntVal should have no children")

    # Integer value. Não contem filhos
    def evaluate(self):
        return int(self.value)


class NoOp(Node):
    #  No Operation (Dummy). Não contem filhos
    def evaluate(self):
        pass


# Available Operations
TERM_OP = "TERM_OP"
termOperators = ("/", "*")
EXP_OP = "EXP_OP"
expOperators = ("+", "-")
FACT_OP = "FACT_OP"
factOperators = ("(", ")")

binOperators = ("+", "-", "*", "/")  #Ex: 1+1
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
