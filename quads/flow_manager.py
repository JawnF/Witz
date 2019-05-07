from quads.opids import OpIds

class FlowManager:

    def __init__(self, generator):
        self.quads = generator

    def exp_evaluation(self, variable_data):
        self.generate_gotof(variable_data[0])
        self.quads.store_jump()

    # -------- IF block flow
    
    def if_after_block(self):
        self.quads.fill_jump()
    
    # -------- IF ELSE block flow

    def if_else_after_if_block(self):
        self.quads.fill_jump()
        self.generate_goto()
        self.quads.store_jump()
    
    # -------- WHILE block flow

    def while_leave_breadcrumb(self):
        self.quads.store_jump()
        
    def while_after_block(self):
        start = self.quads.pop_jump()
        self.generate_goto(start)
        self.quads.fill_jump()
    
    # -------- FOR block flow

    def for_store_first_argument(self, value):
        pass

    # -------- Other

    def generate_goto(self, target = None):
        self.quads.generate(OpIds.goto, 0, 0, target, target == None)
    
    def generate_gotof(self, temp, target = None):
        self.quads.generate(OpIds.gotof, temp, 0, target, target == None)
