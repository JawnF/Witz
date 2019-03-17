#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from scope import Scope
from variablesymbol import VariableSymbol
class SymbolTable:
    root = 'global'
    current_scope = root
    search_scope = root
    table = {}

    def __init__(self):
        self.table[self.root] = Scope(None, 'global') 
    
    def lookup(self, name):
        '''Recibe el nombre del ID a buscar, regresa true si
           lo encontró en el scope actual de la semántica,
        '''
        self.set_search_scope()
        exist = self.look_current_search_scope(name)
        if not exist:
            raise Exception('Value doesn\'t exist')
        return exist
    
    def neg_lookup(self, name):
        '''Recibe el nombre del ID a buscar, regresa false si
           no lo encontró en el scope actual de la semántica,
        '''
        self.search_scope = self.current_scope
        exist = self.look_current_search_scope(name)
        if exist:
            raise Exception('Value already exists')
        return False

    def store(self, id, symbol, scope_type):
        '''
        Crea un símbolo apartir del token que es pasado por el parser.
        '''
        self.table[self.current_scope].symbols[id] = symbol
        if scope_type:
            self.create_new_scope(id, scope_type)
            if scope_type == 'function':
                self.store_params(symbol)

    def create_new_scope(self, name, scope_type):
        current_scope = self.current_scope
        if self.currently_in_class():
            new_scope = current_scope + '_' + name
        else:
            new_scope = name
        self.table[new_scope] = Scope(current_scope, scope_type)
        self.current_scope = new_scope
    
    def store_params(self, symbol):
        for param in symbol.params:
            self.store(param[0], VariableSymbol(param[1], True), False)

    def currently_in_class(self):
        return self.scope().type == 'class'

    def scope(self):
        return self.table[self.current_scope]

    def close_scope(self):
        self.current_scope = self.scope().parent

    def check_class(self, class_name):
        exists = self.table[self.root].symbols.get(class_name)
        if not exists:
            raise Exception('Class doesn\'t exist')
    
    def set_constructor(self, name, symbol):
        if name == self.current_scope:
            self.store(name, symbol, 'function')
        else:
            raise Exception('Constructor must have the same name as the class')
    
    def look_current_search_scope(self, name):
        self.set_search_scope()
        while self.search_scope:
            if name in self.table[self.search_scope].symbols:
                return self.table[self.search_scope].symbols[name]
            if self.search_scope == 'global':
                return False
            self.search_scope = self.scope().parent

    def local_neg_lookup(self, name):
        if name in self.scope().symbols:
            raise Exception('Value '+name+' already exists!')
        return False

    def check_new(self, constructor, var_type):
        if not constructor == var_type:
            raise Exception('Constructor doesn\'t match variable type')
        return True
    
    def check_class_scope(self):
        self.set_search_scope()
        self.search_class_scope()
    
    def search_class_scope(self):
        if self.search_scope == self.root:
            raise Exception('Not in a class scope')
        elif self.table[self.search_scope].type == 'class':
            return True
        self.search_scope = self.scope().parent
        self.search_class_scope()
    
    def check_class_property(self, name):
        current_class = self.current_class()
        if not current_class or not name in current_class.symbols:
            raise Exception('Property does not exist.')
        else:
            return True

    def current_class(self):
        self.set_search_scope()
        while self.search_scope:
            if self.table[self.search_scope].type == 'class':
                return self.table[self.search_scope]
            self.search_scope = self.table[self.search_scope].parent  
        return False

    def set_search_scope(self):
        self.search_scope = self.current_scope

    def check_variable(self, name):
        self.set_search_scope()
        while self.search_scope:
            exist = self.table[self.search_scope].symbols[name]
            if exist and exist.symbol_type == 'variable':
                return exist
            self.search_scope = self.table[self.search_scope].parent

    def has_property(self, symbol, name):
        if not symbol.is_class_instance():
            return False
        object_class = symbol.var_type
        class_scope = self.table[object_class]
        if not name in class_scope.symbols:
            raise Exception('Variable has no property '+name)
        return True

    def check_property(self, name):
        value = self.lookup(name)
        if value.symbol_type == 'class':
            raise Exception('Invalid use of class '+name)
        else:
            return value