import sys
import re
import copy
from dataclasses import dataclass
import nodes


@dataclass
class Token:
    value: str
    type: str = ""


# Available Operations
TERM_OP = "TERM_OP"
termOperators = ("/", "*")
EXP_OP = "EXP_OP"
expOperators = ("+", "-")
FACT_OP = "FACT_OP"
factOperators = ("(", ")")
allOperators = termOperators + expOperators + factOperators
# Number
NUMBER = "NUMBER"

EOF = 'EOF'


class PrePro:
    @staticmethod
    def filter(expression: str):
        result = re.sub('(#=)((.|\n)*?)(=#)', '', expression)
        return result


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
            # * /
            elif current_c in termOperators:
                self.actual = Token(current_c, TERM_OP)
                return self.actual
            # ( )
            elif current_c in factOperators:
                self.actual = Token(current_c, FACT_OP)
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

        if tokenizer.actual.type == EXP_OP:
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

        elif tokenizer.actual.value == "(":
            tokenizer.selectNext()
            result = Parser.parseExpression(tokenizer)
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
        # print(tokenizer.actual.value)
        result = Parser.parseFactor(tokenizer)
        while tokenizer.actual.type == TERM_OP:

            result = nodes.BinOp(tokenizer.actual.value, [result])
            tokenizer.selectNext()
            result.children.append(Parser.parseFactor(tokenizer))

            # if tokenizer.actual.value == '*':
            #     tokenizer.selectNext()
            #     next_token = Parser.parseFactor(tokenizer)
            #     result *= int(next_token)

            # elif tokenizer.actual.value == '/':
            #     tokenizer.selectNext()
            #     next_token = Parser.parseFactor(tokenizer)
            #     result //= int(next_token)
            # else:
            # raise ValueError("<ERROR> Character not expected: {}".format(
            #     tokenizer.actual.value))

        return result

    @staticmethod
    def parseExpression(tokenizer: Tokenizer):
        # print(tokenizer.actual.value)
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
    def run(code: str):
        expression = PrePro.filter(code)
        tokenizer = Tokenizer(expression)
        result = Parser.parseExpression(tokenizer).evaluate()
        if tokenizer.actual.type != EOF:
            raise ValueError("<ERROR> Ended before EOF")
        sys.stdout.write(str(int(result)) + '\n')


def main():
    path = sys.argv[1]
    f = open(path, "r")
    expression = f.read()
    Parser.run(expression)


if __name__ == "__main__":
    main()
