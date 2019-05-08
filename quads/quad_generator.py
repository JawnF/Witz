from .quad import Quad

class QuadGenerator:
    quads = {}
    current_index = 1
    jumps = []

    def generate(self, operator, left, right, target_address, pending = False):
        quad = Quad(operator, left, right, target_address, pending)
        self.quads[self.current_index] = quad
        self.current_index += 1

    def store_jump(self, offset = 0):
        self.jumps.append(self.current_index + offset)
    
    def pop_jump(self):
        return self.jumps.pop()
    
    def fill_jump(self, offset = 0):
        index = self.pop_jump()
        temp_quad = self.quads[index]
        temp_quad.target = self.current_index + offset
        self.quads[index] = temp_quad
    