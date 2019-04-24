class ClassSymbol:
    symbol_type = 'class'
    is_callable = False
    def __init__(self, parent):
        self.parent = parent