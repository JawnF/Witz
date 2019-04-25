class AddressManager:

    dict_index = {
        'global_int': 0,
        'global_float': 0,
        'global_str': 0,
        'global_bool': 0,
        'global_obj': 0,

        'temp_int': 0,
        'temp_float': 0,
        'temp_str': 0,
        'temp_bool': 0,
        'temp_obj': 0,

        'local_int': 0,
        'local_float': 0,
        'local_str': 0,
        'local_bool': 0,
        'local_obj': 0,
        
        'const_int': 0,
        'const_float': 0,
        'const_str': 0,
        'const_bool': 0
    }
     
    offset = {
        'global_int': 1,
        'global_float': 4001,
        'global_bool': 8001,
        'global_str': 12001,
        'global_obj': 16001,

        'local_int': 20001,
        'local_float': 20101,
        'local_str': 20201,
        'local_bool': 20301,
        'local_obj': 20401,

        'temp_int': 40001,
        'temp_float': 44001,
        'temp_str': 48001,
        'temp_bool': 52001,
        'temp_obj': 56001,
        
        'const_int': 60001,
        'const_float': 64001,
        'const_str': 68001,
        'const_bool': 72001
    }

    limits = {
        'global_int': 4000,
        'global_float': 8000,
        'global_str': 12000,
        'global_bool': 16000,
        'global_obj': 20000,

        'local_int': 100,
        'local_float': 200,
        'local_str': 300,
        'local_bool': 400,
        'local_obj': 500,

        'temp_int': 44000,
        'temp_float': 48000,
        'temp_str': 52000,
        'temp_bool': 56000,
        'temp_obj': 60000,
        
        'const_int': 64000,
        'const_float': 68000,
        'const_str': 72000,
        'const_bool': 76000
    }

    def __init__(self):
        self.hola_mundo = 'hola mundo'
        
    def get_next(self, type):
        self.dict_index[type] += 1
        if self.dict_index[type] + self.offset[type] > self.limits[type]:
            raise Exception('Overflow error')
        return self.dict_index
    
    def reset_local(self):
        self.dict_index['local_int']: 0
        self.dict_index['local_float']: 0
        self.dict_index['local_str']: 0
        self.dict_index['local_bool']: 0
        self.dict_index['local_obj']: 0

    def free_temporals(self, address):
        if address < self.offset['temp_int'] or address > self.limits['temp_obj']:
            raise Exception ('Cannot free non-temporal memory')
        if self.is_temporal_object(address):
            print('hola mundo')
            #for add in self.