class Symbol:
    def __init__(self, is_callable):
        self.is_callable = is_callable
    
    def set_iscallable(self, is_callable):
        self.is_callable = is_callable
    
    def get_iscallable(self, is_callable):
        return(self.is_callable)

    