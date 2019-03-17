class FunctionSymbol:
    symbol_type = 'function'
    is_callable = True
    def __init__(self, return_type, params):
        self.params = params
        self.param_type = list(map(lambda x: x[1], params))
        self.return_type = return_type
    