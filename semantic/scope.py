class Scope:

    def __init__(self, parent, scope_type, symbol):
        self.type = scope_type
        self.parent = parent
        self.symbol = symbol
        self.symbols = {}
