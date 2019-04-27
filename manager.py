from semantic.symboltable import SymbolTable
from semantic.symbols import VariableSymbol
from semantic.symbols import ClassSymbol
from semantic.symbols import FunctionSymbol
from semantic.symbols import StackSymbol
from semantic.cube import SemanticCube
from quads.temp import Temp
from quads.quad_generator import QuadGenerator
from quads.flow_manager import FlowManager
from memory.memory import Memory
from quads.opids import OpIds
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
        class_symbol = self.table.check_class(class_name)
        class_scope = self.table.table[class_name]
        class_attributes = [(name,symbol) for name, symbol in class_scope.symbols if ininstance(symbol, VariableSymbol)]
        symbol_attributes = {}
        for (name,symbol) in class_attributes:
            symbol_attributes[name] = (symbol.address, self.memory.get_address('instance', attr.type))
        argument_types = list(map(lambda x: x[1], args))
        accepts = class_symbol.accepts_arguments(argument_types)
        if not accepts:
            raise Exception('Arguments do not match constructor')
        new_address = self.memory.get_address('temp', 'obj')
        symbol = VariableSymbol(new_address, class_name, symbol_attributes)
        return symbol.to_tuple()

    def end_class_scope(self):
        '''
        Function that closes a class scope, by default it returns
        a quad of type RETURN 
        '''
        self.table.close_scope()
        self.quads.generate('RETURN', 0, 0, 0)

    def assign(self, variable, value):
        if len(value) == 3 and isinstance(value[3], VariableSymbol):
            value[3].address = variable[0]
            self.table.replace(variable[3], value[3])
        self.oracle.is_valid(variable[1], value[1])
        self.quads.generate(OpIds.assign, value[0], 0, variable[0])
        return variable
                        
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
                if isinstance(class_has_property, StackSymbol):
                    raise Exception('Cannot use stack '+prop_id+' outside a stack call.')
                
                # Returns the symbol
                return class_has_property
            else:
                raise Exception('Property '+prop_id+' does not exist in class '+in_class_scope+'.')
        # If we are not inside a class scope, then the keyword this is not available
        else:
            raise Exception('Keyword this is not available outside a class scope')
            
    def var_property(self, var_id, property_id):
        '''
        Function that handles the id.id functionallity
        '''
        variable_exists = self.id_property(var_id)
        if isinstance(variable_exists, FunctionSymbol):
            raise Exception('Cannot access property of function '+var_id+'.')
        if variable_exists:
            symbol = variable_exists.get_attribute(property_id)
            if not symbol:
                raise Exception('Variable '+var_id+' does not have attribute '+property_id+'.')
            return symbol.to_tuple()

    def id_property(self,property_id):
        class_property = self.table.check_property(property_id)
        if isinstance(class_property, StackSymbol):
            raise Exception('Cannot use stack '+property_id+' outside a stack call.')
        if class_property:
            return class_property.to_tuple()
        else:
            raise Exception('Variable '+property_id+' is not defined.')

    def print_output(self, expression):
        x = 20
    
    def return_value(self, return_value):
        # Validates that the return object is the same type as the function return type
        has_correct_return = self.table.check_return(return_value)
        if has_correct_return:
            x = 20
        else:
            # TODO verify Exception message
            raise Exception('Cannot return '+return_value+' in function of type '+self.table.scope().symbol.return_type) 
    
    def return_void(self):
        self.table.check_return('void')
        
        x = 20

    def float_constant(self, value):
        address = self.memory.get_constant_address('float', value)
        # TODO check if tuple is needed
        return address

    def int_constant(self, value):
        address = self.memory.get_constant_address('int', value)
        return address
                        
    def string_constant(self, value):
        address = self.memory.get_constant_address('str', value)
        return address

    def free_temp_memory(self, memory_address):
        self.memory.free_if_temp(memory_address)

    def read(self):
        #Return temporal

        x = 20

    def operate(self, operator, left_op, right_op):
        # left_op & right_op = tuple(address, type)
        res_type = self.oracle.is_valid(operator, left_op, right_op)
        new_address = self.memory.get_address('temp', res_type)
        self.quads.generate(OpIds.get(operator), left_op[0], right_op[0], new_address)
        # liberar memoria temporal de left_op y right_op
        self.memory.free_if_temp(left_op[0])
        self.memory.free_if_temp(right_op[0])
        return (new_address, res_type)

    def check_id_exists(self, id):
        '''
        Function that checks if an id exists
        '''
        return self.table.lookup(id)

    def check_call_validity(self, property, arguments):
        symbol = property[3]
        argument_types = list(map(lambda x: x[1], arguments))
        if not symbol.is_callable:
            raise Exception('Cannot call a non callable object')
        if not symbol.accepts_arguments(argument_types):
            raise Exception('Arguments do not match function parameters.')
        new_address = self.memory.get_address('temp', symbol.type)
        return (new_address, symbol.type)
 
    def call_stack(self, stack_symbol, call):
        if call[0] == 'push':
            return self.push_stack(stack_symbol, call[1])
        elif call[0] == 'peek':
            return self.peek_stack(stack_symbol)
        else:
            return self.pop_stack(stack_symbol)

    def push_stack(self, symbol, tuple_expr):
        if symbol.type != tuple_expr[1]:
            raise Exception('Cannot push element of type '+tuple_expr[1]+' into a stack of type '+symbol.type)
        self.quads.generate(OpIds.push, tuple_expr[0], 0, symbol.address)
        return tuple_exp

    def pop_stack(self, symbol):
        new_addres = self.memory.get_address('temp', symbol.type)
        self.quads.generate(OpIds.pop, symbol.address, 0, new_address)
        return (new_address, symbol.type)
    
    def peek_stack(self, symbol):
        new_addres = self.memory.get_address('temp', symbol.type)
        self.quads.generate(OpIds.peek, symbol.address, 0, new_address)
        return (new_address, symbol.type)

    def is_stack_type(self, variable):
        symbol = self.table.lookup(variable)
        if not isinstance(symbol, StackSymbol):
            raise Exception('Cannot perform stack methods on non-stack property '+variable+''.')
        return symbol

    def id_does_not_exist(self, identifier):
        id_exist = self.table.lookup(identifier)
        if id_exist:
            raise Exception('Identifier '+identifier + ' already exists')

    def create_quads_txt(self):
        file = open("quads.txt","w+")
        for quad in self.quads.quads:
            file.write(str(quad)+'\n')
        file.close()
    