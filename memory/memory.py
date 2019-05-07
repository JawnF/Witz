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

    def get_value(self, address):
        (scope, v_type) = ranges.get_scope_and_type_from_address(address)
        return {
        	'global' : self.globals,
        	'local' : self.locals,
        	'temp' : self.temps,
        	'const' : self.consts,
            'instance' : self.instances
        }.get(scope).retrieve(v_type, address)
    
    def store(self, address, value):
        scope_type = ranges.get_scope_and_type_from_address(address)
        directory = {
        	'global' : self.globals,
        	'local' : self.locals,
        	'temp' : self.temps,
        	'const' : self.consts,
            'instance' : self.instances
        }.get(scope_type[0]).store(scope_type, address, value)
    
    def print_value(self, address):
        scope_type = ranges.get_scope_and_type_from_address(address)
        directory = {
        	'global' : self.globals,
        	'local' : self.locals,
        	'temp' : self.temps,
        	'const' : self.consts,
            'instance' : self.instances
        }.get(scope_type[0]).print_value(scope_type, address)
    
    def get_dict_with_address(self, address):
        scope_type = ranges.get_scope_and_type_from_address(address)
        directory = {
        	'global' : self.globals,
        	'local' : self.locals,
        	'temp' : self.temps,
        	'const' : self.consts,
            'instance' : self.instances
        }.get(scope_type[0]).print_value(scope_type)