class Symbol:
    def __init__(self, address, v_type):
        self.address = address
        self.type = v_type

    def to_tuple(self):
        return (self.address, self.type, self)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.address == other.address

class FunctionSymbol(Symbol):
    symbol_type = 'function'
    is_callable = True
    def __init__(self, address, v_type, params):
        Symbol.__init__(self, address, v_type)
        self.params = params
        self.param_types = list(map(lambda x: x[1], params))
    
    def accepts_arguments(self, argument_types):
        return self.param_types == argument_types

class VariableSymbol(Symbol):
    symbol_type = 'variable'
    is_callable = False
    
    def __init__(self, address, v_type, attrs = None):
        Symbol.__init__(self, address, v_type)
        self.attrs = attrs
    
    def is_class_instance(self):
        return not self.type in ['int','float','str','stack','bool']

    def get_attribute(self, name):
        if not self.attrs:
            return False
        if not name in self.attrs:
            return False
        return self.attrs[name]

class ClassSymbol(Symbol):
    symbol_type = 'class'
    is_callable = False
    def __init__(self, address, v_type, parent, params):
        '''
        Parent: Name of parent it inherits from -if-
        Quad number: Number of quad where the class starts
        '''
        Symbol.__init__(self, address, v_type)
        self.parent = parent
        self.params = params
        self.param_types = list(map(lambda x: x[1], params))
    
    def accepts_arguments(self, argument_types):
        return self.param_types == argument_types
    
class StackSymbol(Symbol):
    pass