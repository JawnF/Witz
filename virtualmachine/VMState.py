import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from quads.opids import OpIds
from memory.addressresolver import AddressResolver as ranges
from semantic.cube import SemanticCube
oracle = SemanticCube()

class VMState:

	def __init__(self, vm):
		self.vm = vm

	def get_operation(self, op_id):
		op_id = int(op_id)
		return {
			OpIds.add : self.add,
			OpIds.sub : self.sub,
			OpIds.mult : self.mult,
			OpIds.div : self.div,
			OpIds.gt : self.gt,
			OpIds.lt : self.lt,
			OpIds.ge : self.ge,
			OpIds.le : self.le,
			OpIds.eq : self.eq,
			OpIds.ne : self.ne,
			OpIds.logic_and : self.logic_and,
			OpIds.logic_or : self.logic_or,
			OpIds.assign : self.assign,
			OpIds.goto : self.goto,
			OpIds.gotof : self.gotof,
			OpIds.gotov : self.gotov,
			OpIds.io_read : self.io_read,
			OpIds.io_print : self.io_print,
			OpIds.push : self.push,
			OpIds.pop : self.pop,
			OpIds.peek : self.peek,
			OpIds.declare : self.declare,
			OpIds.func_return : self.func_return,
			OpIds.inherit : self.inherit,
			OpIds.attr : self.attr,
			OpIds.grab : self.grab,
			OpIds.endattr : self.endattr,
			OpIds.instance : self.instance,
			OpIds.endconst : self.endconst,
			OpIds.call : self.call,
			OpIds.param : self.param,
			OpIds.size : self.size
		}.get(op_id, self.null)

	def scope(self):
		return 'global'

	def null(self, cont, left, right, res):
		return (cont+1, self)

	def get_value_from_memory(self, address):
		return self.vm.memory.get_value(address)

	def add(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.vm.memory.store(res, lo+ro)
		return (cont+1, self)

	def sub(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.vm.memory.store(res, lo-ro)
		return (cont+1, self)

	def mult(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.vm.memory.store(res, lo*ro)
		return (cont+1, self)

	def div(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.vm.memory.store(res, lo/ro)
		return (cont+1, self)

	def gt(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.vm.memory.store(res, lo>ro)
		return (cont+1, self)

	def lt(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.vm.memory.store(res, lo<ro)
		return (cont+1, self)

	def ge(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.vm.memory.store(res, lo>=ro)
		return (cont+1, self)

	def le(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.vm.memory.store(res, lo<=ro)
		return (cont+1, self)

	def eq(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.vm.memory.store(res, lo==ro)
		return (cont+1, self)

	def ne(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.vm.memory.store(res, lo!=ro)
		return (cont+1, self)

	def logic_and(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.vm.memory.store(res, lo and ro)
		return (cont+1, self)

	def logic_or(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.vm.memory.store(res, lo or ro)
		return (cont+1, self)

	def assign(self, cont, left, right, res):
		val = self.get_value_from_memory(left)
		scope,v_type = ranges.get_scope_and_type_from_address(res)
		cast = {
			'int' : int,
			'float' : float,
			'bool' : bool,
			'str' : str
		}.get(v_type, str)
		self.vm.memory.store(res, cast(val))
		return (cont+1, self)

	def goto(self, cont, left, right, res):
		return (res, self)

	def gotof(self, cont, left, right, res):
		cond = self.get_value_from_memory(left)
		if cond:
			return (cont+1, self)
		else:
			return (res, self)

	def gotov(self, cont, left, right, res):
		cond = self.get_value_from_memory(left)
		if not cond:
			return (cont+1, self)
		else:
			return (res, self)

	def io_read(self, cont, left, right, res):
		val = raw_input()
		self.vm.memory.store(res, val)
		return (cont+1, self)

	def io_print(self, cont, left, right, res):
		val = self.get_value_from_memory(res)
		print(val)
		return (cont+1, self)

	def push(self, cont, left, right, res):
		val = self.get_value_from_memory(left)
		mem = self.vm.memory.get_dict_with_address(res)
		current_value = mem[res]
		if not isinstance(current_value, list):
			mem[res] = []
		mem[res].append(val)
		return (cont+1, self)

	def pop(self, cont, left, right, res):
		mem = self.vm.memory.get_dict_with_address(left)
		if len(mem[left]) == 0:
			raise Exception('Can\'t pop value from empty stack.')
		else:
			val = mem[left].pop()
		self.vm.memory.store(res, val)
		return (cont+1, self)

	def size(self, cont, left, right, res):
		mem = self.vm.memory.get_dict_with_address(left)
		current_value = mem[left]
		if not isinstance(current_value, list):
			raise Exception('Can\'t get size of non-stack.')
		val = len(mem[left])
		self.vm.memory.store(res, val)
		return (cont+1, self)

	def peek(self, cont, left, right, res):
		mem = self.vm.memory.get_dict_with_address(left)
		if len(mem[left]) == 0:
			raise Exception('Can\'t peek value from empty stack.')
		else:
			val = mem[left][-1]
		self.vm.memory.store(res, val)
		return (cont+1, self)

	def declare(self, cont, left, right, res):
		self.vm.memory.store(res, 0)
		return (cont+1, self)

	def inherit(self, cont, left, right, res):
		return (cont+1, self)

	def attr(self, cont, left, right, res):
		return (cont+1, self)

	def endattr(self, cont, left, right, res):
		return (cont+1, self)

	def instance(self, cont, left, right, res):
		return (cont+1, self)




	def endconst(self, cont, left, right, res):
		return (cont+1, self)

		self.vm.memory.store(res, lo-ro)



	def call(self, cont, left, right, res):
		quad = left
		self.vm.memory.locals.expand()
		self.vm.grabs.reverse()
		self.vm.returns.append(res)
		self.vm.jumps.append(cont+1)
		return (quad, self)

	def param(self, cont, left, right, res):
		value = self.get_value_from_memory(res)
		# print('passing', value)
		self.vm.grabs.append(value)
		return (cont+1, self)

	def func_return(self, cont, left, right, res):
		continue_at = self.vm.jumps.pop()
		store_return_to = self.vm.returns.pop()
		return_value = self.get_value_from_memory(res)
		# print('returning', return_value)
		self.vm.memory.locals.end_function()
		self.vm.memory.store(store_return_to, return_value)
		# print('returning',self.get_value_from_memory(store_return_to))
		return (continue_at, self)

	def grab(self, cont, left, right, res):
		value = self.vm.grabs.pop()
		addr = res
		self.vm.memory.store(addr, value)
		# print('grabbing',res, self.get_value_from_memory(addr))
		return (cont+1, self)