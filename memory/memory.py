from .memoryblocks import GlobalMemory
from .memoryblocks import TemporalMemory
from .memoryblocks import LocalMemory
from .memoryblocks import ConstantMemory
from .memoryblocks import InstanceMemory
from addressresolver import AddressResolver as ranges

class Memory:
    
    def __init__(self):
        self.globals = GlobalMemory()
        self.locals = LocalMemory()
        self.temps = TemporalMemory()
        self.consts = ConstantMemory()
        self.instances = InstanceMemory()

    def get_address(self, scope, v_type):
        directory = {
        	'global' : self.globals,
        	'local' : self.locals,
        	'temp' : self.temps,
        	'const' : self.consts,
            'instance' : self.instances
        }.get(scope)
        return directory.get_next(v_type)
    
    def free_if_temp(self, address):
        self.temps.free(address)

    def get_constant_address(self, v_type, value):
        return self.consts.get_constant_address(v_type, value)

    def clear_instance_memory(self):
        self.instances = InstanceMemory()