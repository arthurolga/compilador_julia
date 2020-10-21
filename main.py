import sys
import re
import copy
from dataclasses import dataclass
import nodes
from symbols import *
import os


@dataclass
class Token:
    value: str
    type: str = ""


# Available Operations
TERM_OP = "TERM_OP"
termOperators = ("/", "*", "&&")
EXP_OP = "EXP_OP"
expOperators = ("+", "-", "||")
FACT_OP = "FACT_OP"
factOperators = ("(", ")")
factBeginningOperators = ("!", "+", "-")
REL_OP = "REL_OP"
relatOperators = (">", "<")
allOperators = termOperators + expOperators + factOperators + relatOperators
endLine = "\n"
assignment = "="
_println = "println"
_while = "while"
_end = "end"
_readline = "readline"
_if = "if"
_else = "else"
_elseif = "elseif"

# FLAGS
NUMBER = "NUMBER"
VARIABLE = "VARIABLE"
EOF = 'EOF'
END_LINE = 'END_LINE'
ASSIGN = 'ASSIGN'
PRINT = "PRINT"
WHILE = "WHILE"
END = "END"
READLINE = "READLINE"
IF = "IF"
ELSE = "ELSE"
ELSE_IF = "ELSE_IF"


class PrePro:
    @staticmethod
    def filter(expression: str):
        text = re.sub('(#=)((.|\n)*?)(=#)', '', expression)
        text = os.linesep.join([s for s in text.splitlines() if s])
        return text


class Tokenizer:
    def __init__(self, origin: str, position: int = 0):
        self.origin = origin
        self.position = position
        self.actual = self.selectNext()

    def selectNext(self):

        maxLen = len(self.origin)

        if self.position == maxLen:

            self.actual = Token(EOF, EOF)
            return

        pre_token = ""

        while self.position < maxLen:
            current_c = self.origin[self.position]
            if self.position + 1 < maxLen:
                next_c = self.origin[self.position + 1]
            else:
                next_c = None

            self.position += 1

            if current_c == " ":
                if self.position >= maxLen:
                    self.actual = Token(EOF, EOF)
                    return self.actual
                pass
            # + -
            elif current_c in expOperators:
                self.actual = Token(current_c, EXP_OP)
                return self.actual
            # !
            elif current_c == "!":
                self.actual = Token(current_c, EXP_OP)
                return self.actual
            # * /
            elif current_c in termOperators:
                self.actual = Token(current_c, TERM_OP)
                return self.actual
            # < >
            elif current_c in relatOperators:
                self.actual = Token(current_c, REL_OP)
                return self.actual
            # = and ==
            elif current_c == "=":
                current_c = next_c
                self.position += 1
                if self.position < maxLen:
                    next_c = self.origin[self.position]
                else:
                    next_c = None
                if current_c == "=":
                    if next_c != "=":
                        self.actual = Token("==", TERM_OP)
                        return self.actual
                    else:
                        raise ValueError("<ERROR> Unexpected operand ===")
                else:
                    self.position -= 1
                    self.actual = Token("=", ASSIGN)
                    return self.actual
            # &&
            elif current_c == "&":
                current_c = next_c
                self.position += 1
                if self.position < maxLen:
                    next_c = self.origin[self.position]
                else:
                    next_c = None
                if current_c == "&":
                    if next_c != "&":
                        self.actual = Token("&&", TERM_OP)
                        return self.actual
                    else:
                        raise ValueError("<ERROR> Unexpected operand &&&")
                else:
                    raise ValueError(
                        "<ERROR> Unexpected character {} after &".format(
                            current_c))
            # ||
            elif current_c == "|":
                current_c = next_c
                self.position += 1
                if self.position < maxLen:
                    next_c = self.origin[self.position]
                else:
                    next_c = None
                if current_c == "|":
                    if next_c != "|":
                        self.actual = Token("||", TERM_OP)
                        return self.actual
                    else:
                        raise ValueError("<ERROR> Unexpected operand |||")
                else:
                    raise ValueError(
                        "<ERROR> Unexpected character {} after |".format(
                            current_c))

            # ( )
            elif current_c in factOperators:
                self.actual = Token(current_c, FACT_OP)
                return self.actual

            # \n
            elif current_c == endLine:
                self.actual = Token(current_c, END_LINE)
                return self.actual

            # variables and functions
            elif current_c.isalpha():
                pre_token += current_c
                while next_c and (next_c.isalpha() or next_c.isdigit()
                                  or next_c == "_"):
                    current_c = next_c
                    pre_token += current_c
                    self.position += 1
                    if self.position < maxLen:
                        next_c = self.origin[self.position]
                    else:
                        next_c = None
                # println
                if pre_token == _println:
                    self.actual = Token(pre_token, PRINT)
                    return self.actual
                # while
                elif pre_token == _while:
                    self.actual = Token(pre_token, WHILE)
                    return self.actual
                # if
                elif pre_token == _if:
                    self.actual = Token(pre_token, IF)
                    return self.actual
                # else
                elif pre_token == _else:
                    self.actual = Token(pre_token, ELSE)
                    return self.actual
                # elseif
                elif pre_token == _elseif:
                    self.actual = Token(pre_token, ELSE_IF)
                    return self.actual
                # end
                elif pre_token == _end:
                    self.actual = Token(pre_token, END)
                    return self.actual
                # readline()
                elif pre_token == _readline:
                    self.actual = Token(pre_token, READLINE)
                    if next_c and next_c == "(":
                        self.position += 1
                        if self.position < maxLen:
                            next_c = self.origin[self.position]
                        else:
                            next_c = None
                        if next_c and next_c == ")":
                            return self.actual
                        else:
                            raise ValueError("<ERROR> Unclosed parenthesis")
                    else:
                        raise ValueError("<ERROR> parenthesis on readline")

                else:
                    self.actual = Token(pre_token, VARIABLE)
                return self.actual

            # Ints
            elif current_c.isdigit():
                pre_token += current_c
                if not next_c or not next_c.isdigit():
                    self.actual = Token(int(pre_token), NUMBER)
                    return self.actual

            else:
                raise ValueError(
                    "<ERROR> Unindentified character: {}".format(current_c))


class Parser:
    @staticmethod
    def parseFactor(tokenizer: Tokenizer):

        result = 0

        if tokenizer.actual.value in factBeginningOperators:
            #  -2  +1
            result = nodes.UnOp(tokenizer.actual.value, [result])
            tokenizer.selectNext()
            result.children[0] = Parser.parseFactor(tokenizer)

            # if tokenizer.actual.value == '+':
            #     tokenizer.selectNext()
            #     return Parser.parseFactor(tokenizer)
            # if tokenizer.actual.value == '-':
            #     tokenizer.selectNext()
            #     return -Parser.parseFactor(tokenizer)
        elif tokenizer.actual.type == NUMBER:
            result = nodes.IntVal(tokenizer.actual.value)
            tokenizer.selectNext()

        elif tokenizer.actual.type == VARIABLE:
            result = nodes.Identifier(tokenizer.actual.value)
            tokenizer.selectNext()

        elif tokenizer.actual.value == "(":
            tokenizer.selectNext()
            result = Parser.parseRelational(tokenizer)
            if tokenizer.actual.value == ")":
                tokenizer.selectNext()
                return result
            else:
                raise ValueError("<ERROR> Missing closing brackets")

        elif tokenizer.actual.value == ")":
            raise ValueError("<ERROR> Unexpected closing brackets")

        else:
            raise ValueError("<ERROR> Invalid operand at this point")

        return result

    @staticmethod
    def parseTerm(tokenizer: Tokenizer):
        # #print(tokenizer.actual.value)
        result = Parser.parseFactor(tokenizer)
        while tokenizer.actual.type == TERM_OP:

            result = nodes.BinOp(tokenizer.actual.value, [result])
            tokenizer.selectNext()
            result.children.append(Parser.parseFactor(tokenizer))

        return result

    @staticmethod
    def parseCommand(tokenizer: Tokenizer):
        if tokenizer.actual.type == IF:
            ifNode = nodes.IfOp(None, [])
            tokenizer.selectNext()
            condition = Parser.parseRelational(tokenizer)
            ifNode.children.append(condition)
            if tokenizer.actual.type == END_LINE:
                tokenizer.selectNext()
                block = Parser.parseBlock(tokenizer)
                ifNode.children.append(block)
                if tokenizer.actual.type == ELSE:
                    tokenizer.selectNext()
                    block = Parser.parseBlock(tokenizer)
                    ifNode.children.append(block)

            else:
                raise ValueError(
                    "<ERROR> Unexpected operation {}, expected a NEW_LINE".
                    format(tokenizer.actual))
            return ifNode

        if tokenizer.actual.type == WHILE:
            whileNode = nodes.WhileOp(None, [])
            tokenizer.selectNext()
            condition = Parser.parseRelational(tokenizer)
            whileNode.children.append(condition)
            if tokenizer.actual.type == END_LINE:
                tokenizer.selectNext()
                block = Parser.parseBlock(tokenizer)
                whileNode.children.append(block)
                return whileNode

            else:
                raise ValueError(
                    "<ERROR> Unexpected operation {}, expected a NEW_LINE".
                    format(tokenizer.actual))
        elif tokenizer.actual.type == VARIABLE:
            varName = tokenizer.actual.value
            tokenizer.selectNext()
            if tokenizer.actual.type == ASSIGN:
                tokenizer.selectNext()
                if tokenizer.actual.type == READLINE:
                    result = nodes.Readline()
                    tokenizer.selectNext()
                    tokenizer.selectNext()
                else:
                    result = Parser.parseRelational(tokenizer)

                final_node = nodes.Assignment("=",
                                              [varName, result])  #.evaluate()
                return final_node
                #print(nodes.symbolTable)
        elif tokenizer.actual.type == PRINT:

            tokenizer.selectNext()
            if tokenizer.actual.value == "(":
                tokenizer.selectNext()
                result = Parser.parseRelational(tokenizer)
                if tokenizer.actual.value == ")":
                    tokenizer.selectNext()
                    final_node = nodes.Print(PRINT, [result])  #.evaluate()
                    return final_node

            # if tokenizer.actual.value == "(":
            #     tokenizer.selectNext()
            #     result = Parser.parseRelational(tokenizer)
            #     if tokenizer.actual.value == ")":
            #         tokenizer.selectNext()
            #         final_node = nodes.Print(PRINT, [result])  #.evaluate()
            #         return final_node

        elif tokenizer.actual.type == END_LINE or tokenizer.actual.type == EOF:
            pass
        else:
            raise ValueError("<ERROR> Unexpected operation {}".format(
                tokenizer.actual))

        return nodes.NoOp()

    @staticmethod
    def parseBlock(tokenizer: Tokenizer):
        stmt = nodes.Statement(None, [])
        #while tokenizer.actual.type != EOF and tokenizer.actual.type != END and tokenizer.actual.type != END:
        while tokenizer.actual.type not in (EOF, END, ELSE):
            line_node = Parser.parseCommand(tokenizer)
            stmt.children.append(line_node)
            if tokenizer.actual.type == END_LINE:
                #print("Nova linha")
                tokenizer.selectNext()
        if tokenizer.actual.type in (END):
            tokenizer.selectNext()
        return stmt

    @staticmethod
    def parseExpression(tokenizer: Tokenizer):
        # #print(tokenizer.actual.value)
        result = Parser.parseTerm(tokenizer)
        while tokenizer.actual.type == EXP_OP:
            if tokenizer.actual.value == '+' or tokenizer.actual.value == '-':
                result = nodes.BinOp(tokenizer.actual.value, [result])
                tokenizer.selectNext()
                result.children.append(Parser.parseTerm(tokenizer))

            # if tokenizer.actual.value == '+':
            #     tokenizer.selectNext()
            #     next_token = Parser.parseTerm(tokenizer)
            #     result += int(next_token)

            # elif tokenizer.actual.value == '-':
            #     tokenizer.selectNext()
            #     next_token = Parser.parseTerm(tokenizer)
            #     result -= int(next_token)
            else:
                raise ValueError("<ERROR> Character not expected: {}".format(
                    tokenizer.actual.value))
        return result

    @staticmethod
    def parseRelational(tokenizer: Tokenizer):
        # #print(tokenizer.actual.value)
        result = Parser.parseExpression(tokenizer)
        while tokenizer.actual.type == REL_OP:
            if tokenizer.actual.value == '>' or tokenizer.actual.value == '<':
                result = nodes.BinOp(tokenizer.actual.value, [result])
                tokenizer.selectNext()
                result.children.append(Parser.parseTerm(tokenizer))

            else:
                raise ValueError("<ERROR> Character not expected: {}".format(
                    tokenizer.actual.value))
        return result

    @staticmethod
    def run(code: str):
        expression = PrePro.filter(code)
        tokenizer = Tokenizer(expression)
        Parser.parseBlock(tokenizer).evaluate(
        )  #Parser.parseExpression(tokenizer).evaluate()
        if tokenizer.actual.type != EOF:
            raise ValueError("<ERROR> Ended before EOF")
        #sys.stdout.write(str(int(result)) + '\n')


def main():
    path = sys.argv[1]
    f = open(path, "r")
    expression = f.read()
    Parser.run(expression)


if __name__ == "__main__":
    main()
