import sys
from dataclasses import dataclass


@dataclass
class Token:
    value: str

# Available Operations
operators = ("+", "-","/","*")

class Tokenizer:
    def __init__(self, origin: str, position: int = 0):
        self.origin = origin
        self.position = position
        self.actual = self.selectNext() #Token(self.origin[0])

    def selectNext(self):

        maxLen = len(self.origin)

        if self.position == maxLen:

            self.actual = None
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
    def parseExpression(tokenizer: Tokenizer, expression: str):
        if tokenizer.actual.value.isdigit():
            result = int(tokenizer.actual.value)
            while tokenizer.selectNext() is not None:
                if tokenizer.actual.value == '+':
                    next_token = tokenizer.selectNext()
                    if not next_token or not next_token.value.isdigit():
                        raise ValueError("<ERROR> Missing expected integer after operator")
                    result+=int(next_token.value)

                elif tokenizer.actual.value == '-':
                    next_token = tokenizer.selectNext()
                    if not next_token or not next_token.value.isdigit():
                        raise ValueError("<ERROR> Missing expected integer after operator")
                    result-=int(next_token.value)

                elif tokenizer.actual.value == '*':
                    next_token = tokenizer.selectNext()
                    if not next_token or not next_token.value.isdigit():
                        raise ValueError("<ERROR> Missing expected integer after operator")
                    result*=int(next_token.value)

                elif tokenizer.actual.value == '/':
                    next_token = tokenizer.selectNext()
                    if not next_token or not next_token.value.isdigit():
                        raise ValueError("<ERROR> Missing expected integer after operator")
                    result/=int(next_token.value)

                else:
                    raise ValueError("<ERROR> Character not expected: {}".format(tokenizer.actual.value))
        else:
            raise ValueError("<ERROR> First character expected to be integer: {}".format(tokenizer.actual.value))

        return result

    @staticmethod
    def run(code: str):
        tokenizer = Tokenizer(code)
        result = Parser.parseExpression(tokenizer, code)
        sys.stdout.write(str(result)+ '\n')


def main():
    expression = sys.argv[1]
    Parser.run(expression)


if __name__ == "__main__":
    main()
