from semantic.symboltable import SymbolTable
from semantic.symbols import VariableSymbol
from semantic.symbols import ClassSymbol
from semantic.symbols import FunctionSymbol
from semantic.cube import SemanticCube
from quads.temp import Temp
from quads.quad_generator import QuadGenerator
from quads.flow_manager import FlowManager
from memory.memory import Memory
#   Python 
import sys
#sys.tracebacklimit = 0

class StatementManager:
    in_local_scope = False

    def __init__(self):
        self.table = SymbolTable()
        self.oracle = SemanticCube()
        self.quads = QuadGenerator()
        self.flow = FlowManager(self.quads)
        self.memory = Memory()
        # Creating the quad for the initial functions jump
        self.create_initial_jump()

    def create_initial_jump(self):
        '''
            Function that creates the initial jump where 
            the main functions are being executed
        '''
        # We create a new GOTO quad
        self.quads.generate('GOTO', 0, 0, 0, True)
        # Current index quad is at 2, we store the previous quad by adding -1
        self.quads.store_jump(-1)
    
    def start_class_scope(self, class_name, parent_name):
        '''
        Function that starts a new class scope
        '''
        # We first have be sure that the class isn't already defined
        class_exists = self.check_id_exists(class_name)
        if not class_exists: 
            # Fetching the current number index of the quad
            quad_number = self.quads.current_index
            # Checks if it has a parent, if it does then it copies every attribute and function from it
            if parent_name:
                self.table.store_with_parent_symbols(parent_name, class_name, ClassSymbol(parent_name, quad_number), 'class')
            else:
                # Store the class symbol in the symbol table
                self.table.store(class_name, ClassSymbol(parent_name, quad_number), 'class')
        else:
            raise Exception('Class name already defined')

    def check_class_exists(self, class_name):
        '''
        Function that checks if a class that is 
        being inherited from exists, if it doesn't it throws
        and exception
        '''
        class_exists = self.table.check_class(class_name)
        if not class_exists:
            raise Exception('Class doesn\'t exist')

    def store_class_attributes(self, attributes):
        '''
        Function that will store the current class scope attributes in its
        corresponding key at symbol table
        '''
        for attribute in attributes:
            # Each attribute is stored in a tuple
            attribute_name = attribute[0]
            attribute_type = attribute[1]
            # Check if attribute exists
            attribute_exists = self.table.neg_lookup(attribute_name)
            if not attribute_exists:
                self.table.store(attribute_name, VariableSymbol(attribute_type), False)
            else :
                raise Exception('Attribute already exists')

    def start_function_scope(self, function_name, return_type, parameters):
        # Stores the function element
        self.table.store(function_name, FunctionSymbol(return_type, parameters), 'function')
    
    def close_function_scope(self):
        '''
        Function that closes a function scope
        '''
        self.table.close_scope()
        self.quads.generate('RETURN', None, None, None)

    def declare(self, var_tuple):
        var_name = var_tuple[0]
        var_type = var_tuple[1]
        variable_exists = self.table.lookup(var_name)
        if not variable_exists:
            self.table.store(var_name, VariableSymbol(var_type), False)
            scope = self.current_scope[-1]
            address = self.memory.get_address(scope, var_type)
            return address
        raise Exception('Variable '+var_name+' is already assigned')

    def instantiate(self, class_name, args):
        # Return temporal direction of instance
        x = 20

    def end_class_scope(self):
        '''
        Function that closes a class scope, by default it returns
        a quad of type RETURN 
        '''
        self.table.close_scope()
        self.quads.generate('RETURN', None, None, None)

    def assign(self, value, var_address):
        # check if exp is a tuple, check that it is the same type 
        x = 20
    
    def this_property(self, prop_id):
        '''
        Function that handles the this.property functionallity
        '''
        # returns tuple with the address of the attribute and str of type
        # First we check if user is in a class scope
        in_class_scope = self.table.check_class_scope()
        # We are in a class scope
        if in_class_scope:
            class_has_property = self.table.check_class_property(prop_id)
            if class_has_property:
                #Do something
                x = 20
            else:
                raise Exception('Property does not exist')
        # If we are not inside a class scope, then the keyword this is not available
        else:
            raise Exception('Keyword this is not available outside a class scope')
            
    def var_property(self, var_id, property_id):
        '''
        Function that handles the id.id functionallity
        '''
        # returns tuple with the address of the attribute and str of type
        variable_exists = self.table.check_variable(var_id)
        if variable_exists:
            self.table.has_property(var_id, property_id)
        else:
            raise Exception('Variable '+ var_id + ' is not defined.')

    def id_property(self,property_id):
        # returns tuple with the address of the attribute and str of type
        class_property = self.table.check_property(property_id)
        if class_property:
            x = 20
        else:
            raise Exception('Invalid use of name '+property_id)

    def print_output(self, expression):
        x = 20
    
    def return_value(self, return_value):
        x = 20
    
    def return_void(self):
        x = 20

    def float_constant(self, value):
        x = 20

    def int_constant(self, value):
        x = 20
    
    def string_constant(self, value):
        x = 20

    def free_temp_memory(self, memory_address):
        x = 20

    def read(self):
        #Return temporal
        x = 20

    def operate(self, operator, left_op, right_op):
        # liberar memoria temporal de left_op y right_op
        x = 20

    def check_id_exists(self, id):
        '''
        Function that checks if an id exists
        '''
        return self.table.lookup(id)

    def check_call_validity(self, property_name, arguments):
        x = 20

    def is_stack_type(self, variable):
        x = 20

    def id_does_not_exist(self, identifier):
        id_exist = self.table.lookup(identifier)
        if id_exist:
            raise Exception('Identifier '+identifier + ' already exists')

    def create_quads_txt(self):
        file = open("quads.txt","w+")
        for quad in self.quads.quads:
            file.write(str(quad)+'\n')
        file.close()
    