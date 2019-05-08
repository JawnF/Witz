from VMState import VMState

class GlobalState(VMState):

	def execute(self, cont, op, left, right, res):
		# try:
			# print(self.vm.object)
		# except:
			# print(None)
		op = self.get_operation(op)
		return op(cont, left, right, res)
	