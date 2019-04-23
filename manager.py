from semantic.symboltable import SymbolTable
from semantic.variablesymbol import VariableSymbol
from semantic.classsymbol import ClassSymbol
from semantic.functionsymbol import FunctionSymbol
from semantic.cube import SemanticCube
from quads.temp import Temp
from quads.quad_generator import QuadGenerator
from quads.flow_manager import FlowManager

class StatementManager:
    def __init__(self):
        self.table = SymbolTable()
        self.oracle = SemanticCube()
        self.quads = QuadGenerator()
        self.flow = FlowManager(quads)

    def declare(self, var_tuple):
        var_name = var_tuple[0]
        var_type = var_tuple[1]
        # Call table and check if exists, return direction
        # return var_dir;

    def instantiate(self, class_name):
        # Return temporal direction of instance

    def end_class_scope(self):
        # Doesn't return anything, it just ends the scope
    
    def start_class_scope(self, class_name, parent_name):

    def close_constructor_scope(self):
    
    def add_constructor(self, constructor_name, parameters):

    def close_constructor_scope(self):
    
    def assign(self, value, var_address):
    
    def this_property(self, var_id):
        # returns the address of the attribute 
    
    def var_property(self, var_id, property_id):

    def property(self,property_id):

    def print(self, expression):
    
    def return_value(self, return_value):
    
    def return_void(self):

    def float_constant(self, value):

    def int_constant(self, value):
    
    def string_constant(self, value):

    def free_temp_memory(self, memory_address):

    def read(self):
        #Return temporal

    def operate(self, operator, left_op, right_op):
