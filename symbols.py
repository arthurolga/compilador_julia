availableSymbolTypes = ["Int", "Bool", "String"]
# _TYPES = {isInt: "Int", isBool: "Bool", isString: "String"}


class Symbol:
    def __init__(self, name, symbolType, value=None):
        self.name = name
        self.type = symbolType
        self.value = value

    def setValue(self, value):
        self.value = value


class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def _get(self, symbol):
        return self.symbols[symbol]

    def _set(self, symbol, value):
        self.symbols[symbol] = value

    def _setOnlyValue(self, symbol, value):
        self.symbols[symbol].value = value

    def __str__(self):
        return str(self.symbols)
