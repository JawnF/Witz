## Symbol Table
from semantic.symboltable import SymbolTable
from semantic.symbols import VariableSymbol
from semantic.symbols import ClassSymbol
from semantic.symbols import FunctionSymbol
from semantic.symbols import StackSymbol
from semantic.cube import SemanticCube
## Quads
from quads.temp import Temp
from quads.quad_generator import QuadGenerator
from quads.flow_manager import FlowManager
from quads.opids import OpIds
## Memory
from memory.memory import Memory
from memory.addressresolver import AddressResolver as ranges
#   Python 
import copy
import sys
#sys.tracebacklimit = 0

# pendientes
#   imprimir constantes a archivo

class StatementManager:
	in_local_scope = False

	def __init__(self):
		self.table = SymbolTable()
		self.oracle = SemanticCube()
		self.quads = QuadGenerator()
		self.memory = Memory()
		self.flow = FlowManager(self.quads, self.memory)
		# Creating the quad for the initial functions jump
		self.create_initial_jump()

	def get_symbol_from_name(self, id):
		'''
			Function that checks if an id exists in current scope or above
		'''
		return self.table.lookup(id)

	def create_initial_jump(self):
		'''
			Function that creates the initial jump where 
			the main functions are being executed
		'''
		# We create a new GOTO quad
		self.quads.store_jump()
		# Current index quad is at 2, we store the previous quad by adding -1
		self.flow.generate_goto()
	
	def start_class_scope(self, class_name, parent_name, params):
		'''
			Function that starts a new class scope in symbol table and enters it
		'''
		# We first have be sure that the class isn't already defined
		class_exists = self.get_symbol_from_name(class_name)
		# Cannot redeclare class
		if class_exists:
			raise Exception('Class name already defined')
		# Fetching the current number index of the quad
		quad_number = self.quads.current_index
		# Checks if it has a parent, if it does then it copies every attribute and function from it
		if parent_name:
			# Get parent address from symbol
			parent_symbol = self.table.get_class(parent_name)
			p_addr = parent_symbol.address
			# Storing the class in the symbol table and creating scope
			self.table.store_with_parent_symbols(parent_name, class_name, ClassSymbol(quad_number, class_name, parent_name, params), 'class')
			# Generating the quad
			self.quads.generate(OpIds.inherit, 0, 0, p_addr)
		else:
			# Store the class symbol in the symbol table and creating scope
			self.table.store(class_name, ClassSymbol(quad_number, class_name, parent_name, params), 'class')
		# Add params to new scope
		self.store_params(params, 'instance', OpIds.attr)
		# Creating a quad that indicates that its the end of the class' attributes
		self.quads.generate(OpIds.endattr, 0, 0, 0)

	def store_params(self, params, address_type, operation):
		'''
			Function that stores the params with a VariableSymbol that contains its 
			address type -instace, local-
		'''
		for param in params:
			# Assigns a new address for the current param
			new_address = self.memory.get_address(address_type, param[1])
			# Stores the variable symbol in the symbol table
			self.table.store(param[0], VariableSymbol(new_address, param[1]))
			# Generates a new quad with the given operation and the new address
			self.quads.generate(operation, 0, 0, new_address)

	def check_class_exists(self, class_name):
		'''
			Function that checks if a class, that is 
			being inherited from, exists, if it doesn't it throws
			and exception
		'''
		class_exists = self.table.get_class(class_name)
		if not class_exists:
			raise Exception('Class '+class_name+' doesn\'t exist')

	def start_function_scope(self, function_name, return_type, parameters):
		# Stores the function element
		self.memory.locals.expand()
		self.table.store(function_name, FunctionSymbol(self.quads.current_index, return_type, parameters), 'function')
		self.in_local_scope = True
		self.store_params(parameters, 'local', OpIds.grab)
	
	def close_function_scope(self):
		'''
		Function that closes a function scope
		'''
		self.memory.locals.end_function()
		self.table.close_scope()
		self.in_local_scope = False
		self.quads.generate(OpIds.func_return, 0, 0, 0)

	def get_attrs_dict_for_class(self, class_name, args):
		# Gets symbol of the class
		class_symbol = self.table.get_class(class_name)
		# Make sure args are same type as params
		argument_types = list(map(lambda x: x[1], args))
		accepts = class_symbol.accepts_arguments(argument_types)
		if not accepts:
			raise Exception('Arguments do not match constructor for class \''+class_name+'\'.')
		attrs = {}
		# Matches class param with passed args
		class_attributes = zip(class_symbol.params, args)
		for (param, arg) in class_attributes:
			attrs[param[0]] = arg
			# if len(arg) == 3:
			# 	symbol_attributes[param[0]] = arg[2]
			# else:
			# 	new_addr = self.memory.get_address('temp', param[1])
			# 	symbol_attributes[param[0]] = VariableSymbol(new_addr, param[1])
		return attrs

######################################################################################################################################### Vamos aquii,
	def instantiate(self, class_name, args):
		attrs = self.get_attrs_dict_for_class(class_name, args)
		obj = self.new_var_of_type(class_name, 'temp', attrs)
		# self.quads.generate(OpIds.instance, class_symbol.address, 0, new_address)
		# symbol = VariableSymbol(new_address, class_name, symbol_attributes)
		self.foo = obj
		return obj.to_tuple()

	def end_class_scope(self):
		'''
			Function that closes a class scope, by default it returns
			a quad of type RETURN 
		'''
		self.table.close_scope()

	def assign(self, variable, value):
		# Make sure value can be assigned to variable
		self.oracle.can_assign(variable[1], value[1])
		
		# If trying to copy existing variable
		if len(value) == 3 and isinstance(value[2], VariableSymbol):
			new_symbol = copy.deepcopy(value[2])
			new_attrs = self.copy_attributes(new_symbol) 
			new_symbol.address = variable[0]
			for name,attr in new_symbol.attrs.items():
				new_address = self.memory.get_address('local' if self.in_local_scope else 'global', attr.type)
			self.table.replace_symbol(variable[2], new_symbol)

		self.quads.generate(OpIds.assign, value[0], 0, variable[0])
		self.free_temp_memory(value[0])
		return variable
						
	def copy_attributes(self, symbol):
		# If it's an object instance
		for key, attr in symbol.attrs.items():
			if isinstance(attr, VariableSymbol):
				prev = attr.address
				new = attr.address = self.memory.get_address('local' if self.in_local_scope else 'global', attr.type)
				self.quads.generate(OpIds.assign, prev, 0, new)
				if attr.type not in ['int', 'float', 'bool', 'str']:
					self.copy_attributes_aux(attr)

	def copy_attributes_aux(self, symbol):
		symbol.address = self.memory.get_address('local' if self.in_local_scope else 'global', symbol.type)
		
		for key, attr in symbol.attrs.items():
			if isinstance(attr, VariableSymbol):
				prev = attr.address
				new = attr.address = self.memory.get_address('local' if self.in_local_scope else 'global', attr.type)
				self.quads.generate(OpIds.assign, prev, 0, new)
				if attr.type not in ['int', 'float', 'bool', 'str']:
					self.copy_attributes_aux(attr)

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
				return class_has_property.to_tuple()
			else:
				raise Exception('Property '+prop_id+' does not exist in class '+in_class_scope+'.')
		# If we are not inside a class scope, then the keyword this is not available
		else:
			raise Exception('Keyword this is not available outside a class scope')
			
	def var_property(self, var_id, property_id):
		'''
		Function that handles the id.id functionallity
		'''
		variable_exists = self.id_property(var_id)[2]
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
		self.quads.generate(OpIds.io_print, 0, 0, expression[0])
		self.free_temp_memory(expression[0])
		return expression
	
	def return_value(self, return_value):
		# Validates that the return object is the same type as the function return type
		has_correct_return = self.table.check_return(return_value[1])
		if has_correct_return:
			self.quads.generate(OpIds.func_return, 0, 0, return_value[0])
		else:
			raise Exception('Cannot return '+return_value[1]+' in function of type '+self.table.scope().symbol.type) 
	
	def return_void(self):
		has_correct_return = self.table.check_return('void')
		if has_correct_return:
			self.quads.generate(OpIds.func_return, 0, 0, 0)
		else:
			raise Exception('Cannot return void in function of type '+self.table.scope().symbol.type) 
	
	def float_constant(self, value):
		address = self.memory.get_constant_address('float', value)
		return (address, 'float')

	def int_constant(self, value):
		address = self.memory.get_constant_address('int', value)
		return (address, 'int')
						
	def string_constant(self, value):
		address = self.memory.get_constant_address('str', value)
		return (address, 'str')

	def free_temp_memory(self, memory_address):
		self.memory.free_if_temp(memory_address)

	def read(self):
		#Return temporal
		temp_addr = self.memory.get_address('temp', 'str')
		self.quads.generate(OpIds.io_read, 0, 0, temp_addr)
		return(temp_addr, 'str')

	def operate(self, operator, left_op, right_op):
		# left_op & right_op = tuple(address, type)
		res_type = self.oracle.is_valid(operator, left_op, right_op)
		new_address = self.memory.get_address('temp', res_type)
		self.quads.generate(OpIds.get(operator), left_op[0], right_op[0], new_address)
		# liberar memoria temporal de left_op y right_op
		self.memory.free_if_temp(left_op[0])
		self.memory.free_if_temp(right_op[0])
		return (new_address, res_type)

	def check_call_validity(self, property, arguments):
		symbol = property[2]
		argument_types = list(map(lambda x: x[1], arguments))
		if not symbol.is_callable:
			raise Exception('Cannot call a non callable object')
		if not symbol.accepts_arguments(argument_types):
			raise Exception('Arguments do not match function parameters.')
		new_address = self.memory.get_address('temp', symbol.type)
		for param in arguments:
			self.quads.generate(OpIds.param, 0, 0, param[0])
		self.quads.generate(OpIds.call, symbol.address, 0, new_address)
		return (new_address, symbol.type)
 
	def call_stack(self, stack_symbol, call):
		if call[0] == 'push':
			return self.push_stack(stack_symbol, call[1])
		elif call == 'peek':
			return self.peek_stack(stack_symbol)
		elif call == 'size':
			return self.size_stack(stack_symbol)
		else:
			return self.pop_stack(stack_symbol)

	def push_stack(self, symbol, tuple_expr):
		if symbol.type != tuple_expr[1]:
			raise Exception('Cannot push element of type '+tuple_expr[1]+' into a stack of type '+symbol.type)
		self.quads.generate(OpIds.push, tuple_expr[0], 0, symbol.address)
		return tuple_expr

	def size_stack(self, symbol):
		new_address = self.memory.get_address('temp', 'int')
		self.quads.generate(OpIds.size, symbol.address, 0, new_address)
		return (new_address, 'int')

	def pop_stack(self, symbol):
		new_address = self.memory.get_address('temp', symbol.type)
		self.quads.generate(OpIds.pop, symbol.address, 0, new_address)
		return (new_address, symbol.type)


	def peek_stack(self, symbol):
		new_address = self.memory.get_address('temp', symbol.type)
		self.quads.generate(OpIds.peek, symbol.address, 0, new_address)
		return (new_address, symbol.type)

	def is_stack_type(self, variable):
		symbol = self.table.lookup(variable)
		if not isinstance(symbol, StackSymbol):
			raise Exception('Cannot perform stack methods on non-stack property '+variable+'.')
		return symbol

	def clear_instance_memory(self):
		self.memory.clear_instance_memory()

	def id_does_not_exist(self, identifier):
		id_exist = self.table.lookup(identifier)
		if id_exist:
			raise Exception('Identifier '+identifier + ' already exists')

	def fill_goto(self):
		self.quads.fill_jump()

	# TODO : move to quad_generator
	def create_quads_txt(self, filename):
		file = open(filename,"w+")
		for addr, value in self.memory.consts.ints.items():
			if addr > 0:
				file.write(str(addr)+','+str(value)+'\n')
		for addr, value in self.memory.consts.floats.items():
			if addr > 0:
				file.write(str(addr)+','+str(value)+'\n')
		for addr, value in self.memory.consts.bools.items():
			if addr > 0:
				file.write(str(addr)+','+str(value)+'\n')
		for addr, value in self.memory.consts.strs.items():
			if addr > 0:
				file.write(str(addr)+','+str(value)+'\n')
		file.write(str(OpIds.endconst)+'\n')
		for index, quad in self.quads.quads.items():
			file.write(str(quad)+'\n')
		file.close()



# 
# Var instantiation
# 
	def var_type_is_obj(self, type_name):
		return self.mem_type_from_var_type(type_name) == 'obj'

	def mem_type_from_var_type(self, type_name):
		return type_name if type_name in ['int', 'float', 'bool', 'str'] else 'obj'

	def new_var_of_type(self, type_name, scope, args = {}):
		is_stack = isinstance(type_name, tuple) and type_name[0] == 'stack'
		if is_stack:
			type_name = type_name[1]

		mem_type = self.mem_type_from_var_type(type_name)
		new_address = self.memory.get_address(scope, mem_type)
		self.quads.generate(OpIds.declare, 0, 0, new_address)

		if is_stack:
			return StackSymbol(new_address, type_name)

		new_attributes = {}
		if self.var_type_is_obj(type_name):
			new_attributes = self.get_attributes_for_class(type_name, scope, args)
		new_symbol = VariableSymbol(new_address, type_name, new_attributes)
		return new_symbol

	def get_attributes_for_class(self, type_name, scope, args = {}):
		class_scope = self.table.get_class_scope(type_name)
		attrs = {}
		for name,symbol in class_scope.symbols.items():
			if isinstance(symbol, VariableSymbol):
				new_symbol = args.get(name, None)
				if not new_symbol:
					symbol = self.new_var_of_type(symbol.type, scope)
			attrs[name] = new_symbol
		return attrs

	def replicate(self, var_tuple):
		return

	def declare(self, var_tuple):
		scope = 'local' if self.in_local_scope else 'global'
		var_name = var_tuple[0]
		self.table.local_neg_lookup(var_name)
		var_type = var_tuple[1]
		var = self.new_var_of_type(var_type, scope)
		self.table.store(var_name, var)
		return var.to_tuple()