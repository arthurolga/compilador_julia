availableSymbolTypes = ["Int", "Bool", "String"]
# _TYPES = {isInt: "Int", isBool: "Bool", isString: "String"}


class Symbol:
    def __init__(self, name, symbolType, size,value=None):
        self.name = name
        self.type = symbolType
        self.value = value
        self.size = size
        self.pos = None

    def setValue(self, value):
        self.value = value


class SymbolTable:
    pos = 0

    def __init__(self):
        self.symbols = {}

    def _get(self, symbol):
        return self.symbols[symbol]

    def _set(self, symbolId, symbol):
        SymbolTable.pos += symbol.size
        self.symbols[symbolId] = symbol
        self.symbols[symbolId].pos = SymbolTable.pos


    def _setOnlyValue(self, symbol, value):
        self.symbols[symbol].value = value

    def __str__(self):
        return str(self.symbols)
