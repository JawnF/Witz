import os, sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from globalstate import GlobalState
from memory.memory import Memory
from quads.opids import OpIds
# from .memory.memory import Memory
# from .quads.opids import OpIds
import sys

class WitzVirtualMachine:

	def __init__(self, quad_file):
		self.state = GlobalState(self)
		self.memory = Memory()
		self.jumps = []
		self.returns = []
		self.grabs = []
		self.context = None
		self.quads = self.store_constants(quad_file.read().splitlines())

	def run(self):
		cont = 1
		while cont <= len(self.quads):
			# print('running', cont)
			quad = self.quads[cont-1].split(',')
			tup = self.state.execute(cont, int(quad[0]), int(quad[1]), int(quad[2]), int(quad[3]))
			cont, self.state = tup

	def store_constants(self, quad_file):
		processed = 0
		for line in quad_file:
			processed += 1
			values = line.partition(',')
			if int(values[0]) == OpIds.endconst:
				break
			address = int(values[0])
			value = values[2]
			self.memory.consts.store(address, value)
		return quad_file[processed:]