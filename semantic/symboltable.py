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
        if self.table[self.current_scope].symbols[name]:
            raise Exception('Symbol already exists')

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