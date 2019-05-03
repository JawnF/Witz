class AddressResolver:

    @staticmethod
    def get_scope_and_type_from_address(address):
        if address >= 1 and address <= 4000:
            return ('global', 'int')
        elif address >= 4001 and address <= 8000:
            return ('global', 'float')
        elif address >= 8001 and address <= 12000:
            return ('global', 'bool')
        elif address >= 12001 and address <= 16000:
            return ('global', 'str')
        elif address >= 16001 and address <= 20000:
            return ('global', 'obj')

        elif address >= 20001 and address <= 24000:
            return ('local', 'int')
        elif address >= 24001 and address <= 28000:
            return ('local', 'float')
        elif address >= 28001 and address <= 32000:
            return ('local', 'bool')
        elif address >= 32001 and address <= 36000:
            return ('local', 'str')
        elif address >= 36001 and address <= 40000:
            return ('local', 'obj')

        elif address >= 40001 and address <= 44000:
            return ('temp', 'int')
        elif address >= 44001 and address <= 48000:
            return ('temp', 'float')
        elif address >= 48001 and address <= 52000:
            return ('temp', 'bool')
        elif address >= 52001 and address <= 56000:
            return ('temp', 'str')
        elif address >= 56001 and address <= 60000:
            return ('temp', 'obj')

        elif address >= 60001 and address <= 64000:
            return ('const', 'int')
        elif address >= 64001 and address <= 68000:
            return ('const', 'float')
        elif address >= 68001 and address <= 72000:
            return ('const', 'bool')
        elif address >= 72001 and address <= 76000:
            return ('const', 'str')
        elif address >= 76001 and address <= 80000:
            return ('const', 'obj')

        elif address >= 80001 and address <= 84000:
            return ('instance', 'int')
        elif address >= 84001 and address <= 88000:
            return ('instance', 'float')
        elif address >= 88001 and address <= 92000:
            return ('instance', 'bool')
        elif address >= 92001 and address <= 96000:
            return ('instance', 'str')
        elif address >= 96001 and address <= 100000:
            return ('instance', 'obj')
        