# Esta clase se usa en compilacion para 

class LocalMemory:

	start = -1
	end   = -2

	ints 	= {start: 1, 		end: 100}
	floats 	= {start: 101 ,		end: 200}
	bools 	= {start: 201,		end: 300}
	strs 	= {start: 301,		end: 400}
	objs 	= {start: 401, 		end: 500}

	stack = []

	def __init__(self):
		pass

	def create_function():
		

	def get_next(self, type):
		mem = {
			'int' : self.ints,
			'float' : self.floats,
			'bool' : self.bools,
			'str' : self.strs,
			'obj' : self.objs,
		}.get(type)
		index = self.last_index(mem) + 1
		address = index + mem[self.start]
		if address > mem[self.end]:
			raise Exception('Memory error: memory full')
		mem[index] = 0
		return address