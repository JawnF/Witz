from .globalmemory import GlobalMemory
from .localmemory import LocalMemory
from .temporalmemory import TemporalMemory
from .constmemory import ConstMemory

class Memory:
    
    def __init__(self):
        self.globals = GlobalMemory()
        self.locals = LocalMemory()
        self.temps = TemporalMemory()
        self.consts = ConstMemory()

    def get_address(self, scope, type):
        directory = {
        	'global' : self.globals,
        	'local' : self.locals,
        	'temp' : self.temps,
        	'const' : self.consts,
            'instance' : self.intances
        }.get(scope)
        return directory.get_next(type)


