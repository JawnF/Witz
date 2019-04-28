from .globalmemory import GlobalMemory
from .localmemory import LocalMemory
from .temporalmemory import TemporalMemory
from .constmemory import ConstMemory
from addressresolver import AddressResolver as ranges


class Memory:
    
    def __init__(self):
        self.globals = GlobalMemory()
        self.locals = LocalMemory()
        self.temps = TemporalMemory()
        self.consts = ConstMemory()
        # TODO : hacer clase de instancememory y descomentar linea 38

    def get_address(self, scope, type):
        directory = {
        	'global' : self.globals,
        	'local' : self.locals,
        	'temp' : self.temps,
        	'const' : self.consts,
            'instance' : self.intances
        }.get(scope)
        return directory.get_next(type)
    
    def free_if_temp(self, address):
        if ranges.get_scope_and_type_from_address(address)[0] == 'temp':
            self.free(address)

    def free(self, address):
        pass

    def get_constant_address(self, value):
        pass

    def clear_instance_memory(self):
        # self.instances = InstanceMemory()
        pass