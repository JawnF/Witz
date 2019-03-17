class VariableSymbol:
    symbol_type = 'variable'
    is_callable = False
    def __init__(self, var_type, assigned):
        self.var_type = var_type
        self.assigned = assigned
    
    def is_class_instance(self):
        return not self.var_type in ['int','float','str','stack','bool']

    
