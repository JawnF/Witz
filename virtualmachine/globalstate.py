from VMState import VMState

class GlobalState(VMState):

	operations = {
		
	}

	def execute(self, cont, op, left, right, res):
		op = self.get_operation(op)
		return op(cont, left, right, res)
	
	
