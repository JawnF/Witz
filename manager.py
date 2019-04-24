from semantic.symboltable import SymbolTable
from semantic.variablesymbol import VariableSymbol
from semantic.classsymbol import ClassSymbol
from semantic.functionsymbol import FunctionSymbol
from semantic.cube import SemanticCube
from quads.temp import Temp
from quads.quad_generator import QuadGenerator
from quads.flow_manager import FlowManager
from memory.memory import Memory

class StatementManager:
    current_scope = ['global']

    # global, class, function, temporal
    def __init__(self):
        self.table = SymbolTable()
        self.oracle = SemanticCube()
        self.quads = QuadGenerator()
        self.flow = FlowManager(quads)
        self.memory = Memory()

    def declare(self, var_tuple):
        var_name = var_tuple[0]
        var_type = var_tuple[1]
        variable_exists = table.lookup(var_name)
        if not variable_exists:
            table.store(var_name, VariableSymbol(var_type), False)
            scope = self.current_scope[-1]
            address = memory.get_address(scope, var_type)
            return address
        raise Exception('Variable '+var_name+' is already assigned')

    def instantiate(self, class_name, args):
        # Return temporal direction of instance


    def end_class_scope(self):
        # Doesn't return anything, it just ends the scope
        self.table.close_scope()
        self.current_scope.pop()
    
    def start_class_scope(self, class_name, parent_name):
        self.table.store(class_name, ClassSymbol(class_name, parent_name))
        self.current_scope.append('class')

    def start_constructor_scope(self, constructor_name, parameters):
        self.table.set_constructor(constructor_name, FunctionSymbol(constructor_name, parameters))
        self.current_scope.append('function')

    def close_constructor_scope(self):
        self.table.close_scope()
        self.current_scope.pop()

    def assign(self, value, var_address):
        # check if exp is a tuple, check that it is the same type 
    
    def this_property(self, var_id):
        # returns tuple with the address of the attribute and str of type
    
    def var_property(self, var_id, property_id):
        # returns tuple with the address of the attribute and str of type

    def id_property(self,property_id):
        # returns tuple with the address of the attribute and str of type

    def print_output(self, expression):
    
    def return_value(self, return_value):
    
    def return_void(self):

    def float_constant(self, value):

    def int_constant(self, value):
    
    def string_constant(self, value):

    def free_temp_memory(self, memory_address):

    def read(self):
        #Return temporal

    def operate(self, operator, left_op, right_op):
        # liberar memoria temporal de left_op y right_op

    def check_variable_exists(self, variable):

    def check_call_validity(self, property_name, arguments):

    def is_stack_type(self, variable):

    def start_function_scope(self, function_name, return_type, parameters):
    
    def check_class_exists(self, class_name):
    
    def id_does_not_exist(self, identifier):