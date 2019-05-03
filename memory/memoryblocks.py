from addressresolver import AddressResolver as resolver

class GlobalMemory:
	start = -1
	end   = -2

	ints 	= {start: 1, 		end: 4000}
	floats 	= {start: 4001,	    end: 8000}
	bools 	= {start: 8001,		end: 12000}
	strs 	= {start: 12001,	end: 16000}
	objs 	= {start: 16001, 	end: 20000}

	def __init__(self):
		pass

	def get_next(self, v_temp):
		mem = {
			'int' : self.ints,
			'float' : self.floats,
			'bool' : self.bools,
			'str' : self.strs,
			'obj' : self.objs,
		}.get(v_temp, self.objs)
		index = self.last_index(mem) + 1
		address = index
		if address > mem[self.end]:
			raise Exception('Memory error: Global memory full')
		mem[address] = 0
		return address

	def last_index(self, mem):
		keys = mem.keys()
		index = max(keys)
		if index < 0:
			return -1 + mem[self.start]
		return index


class TemporalMemory:
	
	start = -1
	end   = -2
	next_addr = -3

	ints 	= {start: 40001, 		end: 44000,		next_addr: 40001}
	floats 	= {start: 44001,		end: 48000,		next_addr: 44001}
	bools 	= {start: 48001,		end: 52000,		next_addr: 48001}
	strs 	= {start: 52001,		end: 56000,		next_addr: 52001}
	objs 	= {start: 56001, 		end: 60000,		next_addr: 56001}

	def __init__(self):
		pass

	def get_next(self, v_type):
		mem = {
			'int' : self.ints,
			'float' : self.floats,
			'bool' : self.bools,
			'str' : self.strs,
			'obj' : self.objs,
		}.get(v_type, self.objs)
		address = self.last_index(mem)
		if address > mem[self.end]:
			raise Exception('Memory error: Temporal memory full')
		mem[address] = 0
		return address

	def last_index(self, mem):
		keys = mem.keys()
		while (mem[self.next_addr] in keys):
			mem[self.next_addr] += 1
		return mem[self.next_addr]
	
	def free(self, addr):
		(scope, v_type) = resolver.get_scope_and_type_from_address(addr)
		if scope == 'temp':
			mem = {
				'int' : self.ints,
				'float' : self.floats,
				'bool' : self.bools,
				'str' : self.strs,
				'obj' : self.objs,
			}.get(v_type, self.objs)
			mem.pop(addr)
			if mem[self.next_addr] > addr:
				mem[self.next_addr] = addr
            
class LocalMemory:

	start = -1
	end   = -2

	ints 	= {start: 20001, 		end: 24000}
	floats 	= {start: 24001 ,		end: 28000}
	bools 	= {start: 28001,		end: 32000}
	strs 	= {start: 32001,		end: 36000}
	objs 	= {start: 36001, 		end: 40000}

	top = -1
	last = -2
	current = top
	stack = []

	def __init__(self):
		pass

	def expand(self):
		self.stack.append({
			'int' : dict(LocalMemory.ints),
			'float' : dict(LocalMemory.floats),
			'bool' : dict(LocalMemory.bools),
			'str' : dict(LocalMemory.strs),
			'obj' : dict(LocalMemory.objs),
		})
		self.current = self.top

	def end_function(self):
		self.stack.pop()

	def get_next(self, v_temp):
		mem = {
			'int' : self.ints,
			'float' : self.floats,
			'bool' : self.bools,
			'str' : self.strs,
			'obj' : self.objs,
		}.get(v_temp, self.objs)
		index = self.last_index(mem) + 1
		address = index
		if address > mem[self.end]:
			raise Exception('Memory error: Local memory full')
		mem[address] = 0
		return address

	def last_index(self, mem):
		keys = mem.keys()
		index = max(keys)
		if index < 0:
			return -1 + mem[self.start]
		return index

class ConstantMemory:
	start = -1
	end   = -2
	
	ints 	= {start: 60001, 		end: 64000}
	floats 	= {start: 64001,	    end: 68000}
	bools 	= {start: 68001,		end: 72000}
	strs 	= {start: 72001,	    end: 76000}
	objs 	= {start: 76001, 	    end: 80000}

	def __init__(self):
		pass

	def get_next(self, v_temp):
		mem = {
			'int' : self.ints,
			'float' : self.floats,
			'bool' : self.bools,
			'str' : self.strs,
			'obj' : self.objs,
		}.get(v_temp, self.objs)
		index = self.last_index(mem) + 1
		address = index
		if address > mem[self.end]:
			raise Exception('Memory error: Constant memory full')
		mem[address] = 0
		return address

	def last_index(self, mem):
		keys = mem.keys()
		index = max(keys)
		if index < 0:
			return -1 + mem[self.start]
		return index

	def get_constant_address(self, v_type, value):
		mem = {
			'int' : self.ints,
			'float' : self.floats,
			'bool' : self.bools,
			'str' : self.strs,
			'obj' : self.objs,
		}.get(v_type, self.objs)
		for key,val in mem.items():
			if val == value and key > 0:
				return key
		new_addr = self.get_next(v_type)
		mem[new_addr] = value
		return new_addr


class InstanceMemory:
	start = -1
	end   = -2

	ints 	= {start: 80001, 		end: 84000}
	floats 	= {start: 84001,	    end: 88000}
	bools 	= {start: 88001,		end: 92000}
	strs 	= {start: 92001,	    end: 96000}
	objs 	= {start: 96001, 	    end: 100000}

	def __init__(self):
		pass

	def get_next(self, v_temp):
		mem = {
			'int' : self.ints,
			'float' : self.floats,
			'bool' : self.bools,
			'str' : self.strs,
			'obj' : self.objs,
		}.get(v_temp, self.objs)
		index = self.last_index(mem) + 1
		address = index
		if address > mem[self.end]:
			raise Exception('Memory error: Instance memory full')
		mem[address] = 0
		return address

	def last_index(self, mem):
		keys = mem.keys()
		index = max(keys)
		if index < 0:
			return -1 + mem[self.start]
		return index
