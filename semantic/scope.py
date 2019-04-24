class Scope:

    def __init__(self, parent, scope_type, symbol):
        '''
        Scope types: 
            Global, Function, Class
        Parent: 
            if class: Inheritance
            if function: class or global
        Symbol:
            Symbols declared in the scope (Variable, Function, Class, Inherit)
        '''
        self.type = scope_type
        self.parent = parent
        self.symbol = symbol
        self.symbols = {}
