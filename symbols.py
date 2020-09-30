class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def _get(self, symbol):
        return self.symbols[symbol]

    def _set(self, symbol, value):
        self.symbols[symbol] = value

    def __str__(self):
        return str(self.symbols)
