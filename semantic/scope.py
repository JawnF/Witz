class Scope:

    def __init__(self, parent, scope_type):
        self.type = scope_type
        self.parent = parent
        self.symbols = {}
