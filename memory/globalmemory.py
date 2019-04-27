class GlobalMemory:

	start = -1
	end   = -2

	ints 	= {start: 1, 		end: 4000}
	floats 	= {start: 4001 ,	end: 8000}
	bools 	= {start: 8001,		end: 12000}
	strs 	= {start: 12001,	end: 16000}
	objs 	= {start: 16001, 	end: 20000}

	def __init__(self):
		pass

	def get_next(self, type):
		mem = {
			'int' : self.ints,
			'float' : self.floats,
			'bool' : self.bools,
			'str' : self.strs,
			'obj' : self.objs,
		}.get(type, self.objs)
		index = self.last_index(mem) + 1
		address = index + mem[self.start]
		if address > mem[self.end]:
			raise Exception('Memory error: memory full')
		mem[index] = 0
		return address

	def last_index(self, mem):
		keys = mem.keys()
		if len(keys) == 2:
			index = 0
		index = max(keys)
		return index