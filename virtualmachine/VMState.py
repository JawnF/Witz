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
			OpIds.size : self.size,
			OpIds.relate : self.relate,
			OpIds.context : self.context
		}.get(op_id, self.null)

	def scope(self):
		return 'global'

	def null(self, cont, left, right, res):
		return (cont+1, self)

	def get_value_from_memory(self, address):
		if address == 0:
			return 0
		scope,v_type = ranges.get_scope_and_type_from_address(address)
		if scope == 'instance':
			obj_addr = self.vm.object
			obj_dict = self.vm.memory.get_value(obj_addr) 
			address = obj_dict[address]
		return self.vm.memory.get_value(address)

	def store_to_memory(self, address, value):
		scope,v_type = ranges.get_scope_and_type_from_address(address)
		if scope == 'instance':
			obj_addr = self.vm.object
			obj_dict = self.vm.memory.get_value(obj_addr) 
			address = obj_dict[address]
		self.vm.memory.store(address, value)

	def add(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.store_to_memory(res, lo+ro)
		return (cont+1, self)

	def sub(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.store_to_memory(res, lo-ro)
		return (cont+1, self)

	def mult(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.store_to_memory(res, lo*ro)
		return (cont+1, self)

	def div(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.store_to_memory(res, lo/ro)
		return (cont+1, self)

	def gt(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.store_to_memory(res, lo>ro)
		return (cont+1, self)

	def lt(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.store_to_memory(res, lo<ro)
		return (cont+1, self)

	def ge(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.store_to_memory(res, lo>=ro)
		return (cont+1, self)

	def le(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.store_to_memory(res, lo<=ro)
		return (cont+1, self)

	def eq(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.store_to_memory(res, lo==ro)
		return (cont+1, self)

	def ne(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.store_to_memory(res, lo!=ro)
		return (cont+1, self)

	def logic_and(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.store_to_memory(res, lo and ro)
		return (cont+1, self)

	def logic_or(self, cont, left, right, res):
		lo = self.get_value_from_memory(left)
		ro = self.get_value_from_memory(right)
		self.store_to_memory(res, lo or ro)
		return (cont+1, self)

	def assign(self, cont, left, right, res):
		val = self.get_value_from_memory(left)
		scope,v_type = ranges.get_scope_and_type_from_address(res)
		if v_type == 'obj':
			
			# obj_addr = res # direccion obj del objeto target
			# dic = self.vm.memory.get_dict_with_address(obj_addr) 
			# for inst_addr,target_real_addr in dic[obj_addr].items():
			# 	origin_real_address = val[inst_addr]
			# 	dic[obj_addr][inst_addr] = target_real_address
			# self.store_to_memory(real_addr, value)
			t = 1
		else:
			cast = {
				'int' : int,
				'float' : float,
				'bool' : bool,
				'str' : str,
				'obj' : lambda x: x
			}.get(v_type, str)
			self.store_to_memory(res, cast(val))
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
		self.store_to_memory(res, val)
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
		self.store_to_memory(res, val)
		return (cont+1, self)

	def size(self, cont, left, right, res):
		mem = self.vm.memory.get_dict_with_address(left)
		current_value = mem[left]
		if not isinstance(current_value, list):
			raise Exception('Can\'t get size of non-stack.')
		val = len(mem[left])
		self.store_to_memory(res, val)
		return (cont+1, self)

	def peek(self, cont, left, right, res):
		mem = self.vm.memory.get_dict_with_address(left)
		if len(mem[left]) == 0:
			raise Exception('Can\'t peek value from empty stack.')
		else:
			val = mem[left][-1]
		self.store_to_memory(res, val)
		return (cont+1, self)

	def declare(self, cont, left, right, res):
		scope,v_type = ranges.get_scope_and_type_from_address(res)
		if v_type == 'obj':
			self.vm.memory.temps.objs[res] = {}
			self.vm.object = res
		self.store_to_memory(res, 0)
		return (cont+1, self)

	def inherit(self, cont, left, right, res):
		return (cont+1, self)

	def attr(self, cont, left, right, res):
		value = self.vm.grabs.pop()
		addr = res
		obj_addr = self.vm.object
		dic = self.vm.memory.get_dict_with_address(obj_addr)
		if not isinstance(dic[obj_addr], dict):
			dic[obj_addr] = {}
		real_addr = dic[obj_addr][res]
		self.store_to_memory(real_addr, value)
		return (cont+1, self)

	def endattr(self, cont, left, right, res):
		continue_at = self.vm.jumps.pop()
		self.vm.object = None
		return (continue_at, self)

	def instance(self, cont, left, right, res):
		self.vm.object = res
		self.vm.jumps.append(cont+1)
		return (left, self)

	def relate(self, cont, left, right, res):
		obj_addr = self.vm.object
		dic = self.vm.memory.get_dict_with_address(obj_addr)
		if not isinstance(dic[obj_addr], dict):
			dic[obj_addr] = {}
		real_addr = left
		dic[obj_addr][res] = real_addr
		return (cont+1, self)

	def endconst(self, cont, left, right, res):
		return (cont+1, self)

		self.store_to_memory(res, lo-ro)

	def call(self, cont, left, right, res):
		quad = left
		self.vm.memory.locals.expand()
		self.vm.returns.append(res)
		self.vm.jumps.append(cont+1)
		return (quad, self)

	def param(self, cont, left, right, res):
		value = self.get_value_from_memory(res)
		self.vm.grabs.append(value)
		return (cont+1, self)

	def func_return(self, cont, left, right, res):
		continue_at = self.vm.jumps.pop()
		if res != 0:
			store_return_to = self.vm.returns.pop()
			return_value = self.get_value_from_memory(res)
			self.store_to_memory(store_return_to, return_value)
		try:
			self.vm.object = None
		except:
			pass
		self.vm.memory.locals.end_function()
		return (continue_at, self)

	def grab(self, cont, left, right, res):
		value = self.vm.grabs.pop()
		addr = res
		self.store_to_memory(addr, value)
		return (cont+1, self)

	def context(self, cont, left, right, res):
		self.vm.object = res
		return (cont+1, self)