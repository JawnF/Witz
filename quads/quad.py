class Quad:
    def __init__(self, operation, opleft, opright, result, pending = False):
        self.operation = operation
        self.left = opleft
        self.right = opright
        self.result = result
        self.pending = pending
