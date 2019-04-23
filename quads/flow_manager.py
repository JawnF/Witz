from quad_generator import QuadGenerator
from quads.temp import Temp

class FlowManager:

    def __init__(self, generator):
        self.quads = generator

    def exp_evaluation(self):
        temp = Temp.last()
        self.quads.store_jump()
        self.generate_gotof(temp)

    # -------- IF block flow
    
    def if_after_block(self):
        fill = self.quads.pop_jump()
        self.quads.fill_jump(fill)
    
    # -------- IF ELSE block flow

    def if_else_after_if_block(self):
        fill = self.quads.pop_jump()
        self.quads.store_jump()
        self.generate_goto()
        self.quads.fill_jump(fill)
    
    # -------- WHILE block flow

    def while_leave_breadcrumb(self):
        self.quads.store_jump()
        
    def while_after_block(self):
        fill = self.quads.pop_jump()
        start = self.quads.pop_jump()
        self.generate_goto(start)
        self.quads.fill_jump(fill)
    
    # -------- FOR block flow

    def for_store_first_argument(self, value):
        pass

    # -------- Other

    def generate_goto(self, target = None):
        self.quads.generate('GOTO', None, None, target, target == None)
    
    def generate_gotof(self, temp, target = None):
        self.quads.generate('GOTOF', temp, None, target, target == None)
