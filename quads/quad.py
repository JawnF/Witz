class Quad:
    def __init__(self, operation, opleft, opright, target, pending = False):
        self.operation = operation
        self.left = opleft
        self.right = opright
        self.target = target
        self.pending = pending
    
    def __str__(self):
        representation = '(' + self.operation + ',' + self.left + ',' + self.right + ',' + self.target + ')'
        return representation