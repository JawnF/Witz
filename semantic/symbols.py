class FunctionSymbol:
    symbol_type = 'function'
    is_callable = True
    def __init__(self, return_type, params):
        self.params = params
        self.param_type = list(map(lambda x: x[1], params))
        self.return_type = return_type

class VariableSymbol:
    symbol_type = 'variable'
    is_callable = False
    def __init__(self, var_type):
        self.var_type = var_type
    
    def is_class_instance(self):
        return not self.var_type in ['int','float','str','stack','bool']

class ClassSymbol:
    symbol_type = 'class'
    is_callable = False
    def __init__(self, parent, quad_number):
        '''
        Parent: Name of parent it inherits from -if-
        Quad number: Number of quad where the class starts
        '''
        self.parent = parent
        self.quad_number = quad_number
    