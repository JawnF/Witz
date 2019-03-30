from quad import Quad
from temp import Temp

class QuadGenerator:
    quads = {}
    current_index = 1
    jumps = []

    def generate(self, operator, left, right, result, pending = False):
        quad = Quad(operator, left, right, result, pending)
        if isinstance(left, Temp):
            left.free()
        if isinstance(right, Temp):
            right.free()
        self.quads[self.current_index] = quad
        self.current_index += 1
    
    def generate_persistent(self, operator, left, right, result, pending = False):
        quad = Quad(operator, left, right, result, pending)
        self.quads[self.current_index] = quad
        self.current_index += 1

    def store_jump(self, offset = 0):
        self.jumps.append(self.current_index + offset)
    
    def pop_jump(self):
        return self.jumps.pop()
    
    def fill_jump(self, index):
        temp_quad = self.quads[index]
        temp_quad.result = self.current_index
        self.quads[index] = temp_quad

    