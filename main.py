from dataclasses import dataclass


@dataclass
class Token:
    value: str


operators = ("+", "-")


class Tokenizer:
    def __init__(self, origin: str, position: int = 0):
        self.origin = origin
        self.position = position
        self.actual = 0  # self.selectNext()

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

            if current_c in operators:
                self.actual = Token(current_c)
                return self.actual

            # Ints
            if current_c.isdigit():
                pre_token += current_c
                if not next_c or not next_c.isdigit():
                    self.actual = Token(pre_token)
                    return self.actual


class Parser:
    @staticmethod
    def parseExpression(tokenizer: Tokenizer, expression: str):
        element1 = None
        element2 = None
        operation = None
        while tokenizer.selectNext() is not None:

            if tokenizer.actual.value in operators:
                operation = tokenizer.actual.value

            if tokenizer.actual.value.isdigit():
                if element1:
                    element2 = int(tokenizer.actual.value)
                else:
                    element1 = int(tokenizer.actual.value)
            if element1 and operation and element2:
                if operation == "+":
                    element1 = element1 + element2
                if operation == "-":
                    element1 = element1 - element2
                element2 = None
                operation = None

        print(element1)

    @staticmethod
    def run(code: str):
        tokenizer = Tokenizer(code)
        Parser.parseExpression(tokenizer, code)


def main():
    expression = sys.argv[1]
    Parser.run(expression)


if __name__ == "__main__":
    # Only imports if main
    import sys

    main()
