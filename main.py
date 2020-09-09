import sys
import re
import copy
from dataclasses import dataclass


@dataclass
class Token:
    value: str

# Available Operations
termOperators = ("/","*")
operators = ("+", "-","/","*")
eof = 'eof'


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

            self.actual = Token(eof)
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
                pass
            elif current_c in operators:
                self.actual = Token(current_c)
                return self.actual
            # Ints
            elif current_c.isdigit():
                pre_token += current_c
                if not next_c or not next_c.isdigit():
                    self.actual = Token(pre_token)
                    return self.actual
            else:
                raise ValueError("<ERROR> Unindentified character: {}".format(current_c))


class Parser:
    @staticmethod
    def parseTerm(tokenizer: Tokenizer):
        if tokenizer.actual.value.isdigit():
            result = int(tokenizer.actual.value)
            tokenizer.selectNext()
            while tokenizer.actual.value in termOperators :
             
                if tokenizer.actual.value == '*':
                    next_token = tokenizer.selectNext()
                    if not next_token or not next_token.value.isdigit():
                        raise ValueError("<ERROR> Missing expected integer after operator")
                    result*=int(next_token.value)

                elif tokenizer.actual.value == '/':
                    next_token = tokenizer.selectNext()
                    if not next_token or not next_token.value.isdigit():
                        raise ValueError("<ERROR> Missing expected integer after operator")
                    result/=int(next_token.value)
            
                tokenizer.selectNext()
        else:
            raise ValueError("<ERROR> First character expected to be integer: {}".format(tokenizer.actual.value))
        
        
        return int(result)

    @staticmethod
    def parseExpression(tokenizer: Tokenizer):
        result = Parser.parseTerm(tokenizer)
        while tokenizer.actual.value != eof:
            if tokenizer.actual.value == '+':
                tokenizer.selectNext()
                next_token = Parser.parseTerm(tokenizer)
                result+=int(next_token)

            elif tokenizer.actual.value == '-':
                tokenizer.selectNext()
                next_token = Parser.parseTerm(tokenizer)
                result-=int(next_token)
            else:
                raise ValueError("<ERROR> Character not expected: {}".format(tokenizer.actual.value))
        return result

    @staticmethod
    def run(code: str):
        expression = PrePro.filter(code)
        tokenizer = Tokenizer(expression)
        result = Parser.parseExpression(tokenizer)
        sys.stdout.write(str(result)+ '\n')


def main():
    expression = sys.argv[1]
    Parser.run(expression)


if __name__ == "__main__":
    main()
