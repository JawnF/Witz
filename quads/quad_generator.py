from .quad import Quad
from .temp import Temp
from memory.addressmanager import AddressManager

class QuadGenerator:
    quads = {}
    current_index = 1
    jumps = []
    operators = ['+','=','-','*','/', 'GOTO', 'GOTOF', 'GOTOV',
                 'PRINT', 'READ', 'OR', 'AND', 'CONST', 'ATTR',
                 'RETURN', 'VAR', 'ENDCLASS', 'INHERIT', 'ENDATTR',
                 'INSTANCE', 'ASSIGN', 'FUNC']

    def generate(self, operator, left, right, target_address, pending = False):
        operator_type = self.operator_to_number(operator)
        quad = Quad(operator_type, left, right, target_address, pending)
        self.quads[self.current_index] = quad
        self.current_index += 1

    def store_jump(self, offset = 0):
        self.jumps.append(self.current_index + offset)
    
    def pop_jump(self):
        return self.jumps.pop()
    
    def fill_jump(self, index):
        temp_quad = self.quads[index]
        temp_quad.target = self.current_index
        self.quads[index] = temp_quad

    def operator_to_number(self, operator):
        return self.operators.index(operator)
    