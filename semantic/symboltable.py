from .scope import Scope
from .symbols import VariableSymbol
from .symbols import ClassSymbol
#python
import copy

class SymbolTable:
    root = 'global'
    current_scope = root
    search_scope = root
    table = {}

    def __init__(self):
        self.table[self.root] = Scope(None, 'global', None) 

    def root_scope(self):
        return self.table[self.root]


    def scope(self):
        return self.table[self.current_scope]

    def s_scope(self):
        return self.table[self.search_scope]
                        
    def store(self, name, symbol, scope_type = None):
        '''
            Creates a new scope and stores it in the symbol table
        '''
        # Add symbol to current scope
        self.table[self.current_scope].symbols[name] = symbol
        # If not a variable symbol
        if scope_type:
            # Creates a new scope given the name and the type (function or class)
            self.create_new_scope(name, scope_type, symbol)
            if scope_type == 'function':
                self.store_params(symbol)
            
    def get_method_scope(self, class_name, function_name):
        return class_name+'_'+function_name

    def store_with_parent_symbols(self, parent, id, symbol, scope_type):
        '''
            Copies all the elements stored in a parent into a child
            Used for class inheritance
        '''
        # Stores the element first
        self.table[self.current_scope].symbols[id] = symbol
        # Fetches the parent symbols
        parent_symbols = self.table[parent].symbols
        # Creates a new scope with the new class
        self.create_new_scope(id, scope_type, symbol)
        # Stores the parents attributes into the current class scope
        self.table[self.current_scope].symbols = copy.deepcopy(parent_symbols)
    
    def lookup(self, name):
        '''Recibe el nombre del ID a buscar, regresa true si
        lo encontro en el scope actual de la semantica,
        '''
        exist = self.look_current_search_scope(name)
        # if not exist:
        #     raise Exception('Value doesn\'t exist')
        return exist
    
    def neg_lookup(self, name):
        '''
        Receibes the name of the ID, returns false if the
        value was not found in the current scope. 
        Works for when wanting to create variables with the same name
        '''
        self.search_scope = self.current_scope
        exist = self.look_current_search_scope(name)
        return exist

    def create_new_scope(self, name, scope_type, symbol):
        '''
        Creates a new scope based on the current scope
        if the current scope is global, new scope could be a function or class
        if the current scope is class, new scope would be classname_id 
        Stores this new scope in the table of symbols 
        '''
        current_scope = self.current_scope
        if self.currently_in_class():
            new_scope = self.get_method_scope(current_scope, name)
        else:
            new_scope = name
        self.table[new_scope] = Scope(current_scope, scope_type, symbol)
        self.current_scope = new_scope
    
    def store_params(self, symbol):
        '''
        Stores the parameters in the function symbol
        '''
        for param in symbol.params:
            self.store(param[0], VariableSymbol(param[1], True), False)

    def currently_in_class(self):
        return self.scope().type == 'class'

    def get_class(self, class_name):
        '''
            Function that returns a class (symbol) if it exists
            or raises exception if it doesn't
        '''
        exists = self.root_scope().symbols.get(class_name)
        if not isinstance(exists, ClassSymbol):
            raise Exception('\''+class_name+'\' is not a class.')
        return exists
    
    def close_scope(self):  
        '''
            Assigns the scope to the parent of the current scope
        '''
        self.current_scope = self.scope().parent

    # ###
    # def set_constructor(self, name, symbol):
    #     if name == self.current_scope:
    #         self.store(name, symbol, 'function')
    #     else:
    #         raise Exception('Constructor must have the same name as the class')
    
    def look_current_search_scope(self, name):
        self.set_search_scope()
        while self.search_scope:
            if name in self.s_scope().symbols:
                return self.s_scope().symbols[name]
            if self.search_scope == self.root:
                return False
            self.search_scope = self.scope().parent

    def replace_symbol(self, to_replace, new_symbol):
        self.set_search_scope()
        while self.search_scope:
            for name,symbol in self.s_scope().symbols.items():
                if symbol == to_replace:
                    self.s_scope().symbols[name] = new_symbol
                    return new_symbol 
            self.search_scope = self.s_scope().parent
        raise Exception('Error while assigning object of type '+to_replace.type+'.')
    
    def local_neg_lookup(self, name):
        '''
            Makes sure there isn't another symbol with the same name in the current scope
        '''
        if name in self.scope().symbols:
            raise Exception('Value '+name+' already exists!')
        return False

    # ###
    # def check_new(self, constructor, var_type):
    #     if not constructor == var_type:
    #         raise Exception('Constructor doesn\'t match variable type')
    #     return True

    def check_class_scope(self):
        self.set_search_scope()
        return self.search_class_scope()

    def search_class_scope(self):
        '''
            Function that checks if the current scope is inside a class
            If it is inside a function, it checks its parent class
        '''
        if self.search_scope == self.root:
            return False
        elif self.s_scope().type == 'class':
            return self.search_scope
        self.search_scope = self.scope().parent
        return self.search_class_scope()
    
    def check_class_property(self, name):
        current_class = self.current_class()
        if not current_class or not name in current_class.symbols:
            return False
        else:
            return current_class.symbols[name]

    def current_class(self):
        self.set_search_scope()
        while self.search_scope:
            if self.s_scope().type == 'class':
                return self.s_scope()
            self.search_scope = self.s_scope().parent  
        return False

    def set_search_scope(self):
        self.search_scope = self.current_scope

    # ###
    # def check_variable(self, name):
    #     self.set_search_scope()
    #     while self.search_scope:
    #         exist = name in self.s_scope().symbols
    #         if exist and exist.symbol_type == 'variable':
    #             return self.s_scope().symbols[name]
    #         self.search_scope = self.s_scope().parent
    #         return False

    # def has_property(self, symbol, name):
    #     if not symbol.is_class_instance():
    #         raise Exception('No member property of non-class variable')
    #     object_class = symbol.var_type
    #     class_scope = self.table[object_class]
    #     if not name in class_scope.symbols:
    #         raise Exception('Variable has no property '+name)
    #     return class_scope.symbols[name]

    def check_property(self, name):
        value = self.lookup(name)
        if value.symbol_type == 'class':
            return False
        else:
            return value

    def check_return(self, ret_type):
        '''
            Function that checks that the current's scope return 
            type is the same as the one that is being passed
        '''
        if self.scope().symbol.type != ret_type:
            return False
        return True

    # ###
    # def check_stack(self, name):
    #     var_type = self.get_type(name)
    #     if var_type != 'stack':
    #         raise Exception('Variable '+name+' must be of type stack')

    # ###
    # def get_type(self, name):
    #     variable = self.check_variable(name)
    #     return variable.var_type

    # ###
    # def check_params(self, symbol, args):
    #     if not symbol.is_callable:
    #         raise Exception('Attempting to call a non-callable attribute')
    #     if symbol.param_types != args:
    #         raise Exception('Arguments do not match function')
    #     return symbol

    # ###
    # def check_variable_symbol(self, sym):
    #     if not isinstance(sym, VariableSymbol):
    #         raise Exception('Cannot assign value to non-variable symbol')
        