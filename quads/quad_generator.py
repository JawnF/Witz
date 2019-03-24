from quad import Quad
from temp import Temp

class QuadGenerator:
    quads = {}
    current_index = 1

    def generate(self, operator, left, right, result, pending = False):
        quad = Quad(operator, left, right, result, pending)
        if isinstance(left, Temp):
            left.free()
        if isinstance(right, Temp):
            right.free()
        self.quads[self.current_index] = quad
        self.current_index += 1
