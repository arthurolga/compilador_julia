availableSymbolTypes = ["Int", "Bool", "String"]
# _TYPES = {isInt: "Int", isBool: "Bool", isString: "String"}


class Symbol:
    def __init__(self, name, symbolType, value=None):
        self.name = name
        self.type = symbolType
        self.value = value

    def setValue(self, value):
        self.value = value

    def __str__(self):
        return "Name:{} Type:{} value:{}".format(self.name, self.type,
                                                 self.value)


class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def _get(self, symbol):
        return self.symbols[symbol]

    def _set(self, symbol, value):
        self.symbols[symbol] = value

    def _setOnlyValue(self, symbol, value):
        self.symbols[symbol].value = value

    # Functions
    def _def(self, symbol, function):
        if symbol not in self.symbols:
            self.symbols[symbol] = function
        else:
            raise ValueError("<ERROR> Function already declared")

    def _set_return(self, value):
        self.symbols['return'] = value

    def _get_return(self):
        return self.symbols['return']

    def _get_function(self, symbol):
        if symbol in self.symbols:
            return self.symbols[symbol]
        else:
            raise ValueError(
                "<ERROR> unknown function called {}".format(symbol))

    def __str__(self):
        return str(self.symbols)
