class SemanticCube:
    # Available types:
    # int, float, str, stack
    # 
    # Available operations:
    # +, -, *, /, >, <, and, or, ==, !=, >=, <=
    oracle = {
        '+' : {
            'int' : {
                'int' : 'int',
                'float' : 'float',
                'str' : 'str',
                'stack' : False
            },
            'float': {
                'int': 'float',
                'float': 'float',
                'str': 'str',
                'stack': False
            },
            'str' : {
                'int' : 'str',
                'float' : 'str',
                'str' : 'str',
                'stack' : False
            },
            'stack' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            }
        },
        
        '-' : {
            'int' : {
                'int' : 'int',
                'float' : 'float',
                'str' : False,
                'stack' : False
            },
            'float': {
                'int': 'float',
                'float': 'float',
                'str': False,
                'stack': False
            },
            'str' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            },
            'stack' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            }
        },

        '*' : {
            'int' : {
                'int' : 'int',
                'float' : 'float',
                'str' : False,
                'stack' : False
            },
            'float': {
                'int': 'float',
                'float': 'float',
                'str': False,
                'stack': False
            },
            'str' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            },
            'stack' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            }
        },

        '/' : {
            'int' : {
                'int' : 'int',
                'float' : 'float',
                'str' : False,
                'stack' : False
            },
            'float': {
                'int': 'float',
                'float': 'float',
                'str': False,
                'stack': False
            },
            'str' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            },
            'stack' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            }
        },
        
        '>' : {
            'int' : {
                'int' : 'int',
                'float' : 'int',
                'str' : False,
                'stack' : False
            },
            'float': {
                'int': 'int',
                'float': 'int',
                'str': False,
                'stack': False
            },
            'str' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            },
            'stack' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            }
        },

        '>=' : {
            'int' : {
                'int' : 'int',
                'float' : 'int',
                'str' : False,
                'stack' : False
            },
            'float': {
                'int': 'int',
                'float': 'int',
                'str': False,
                'stack': False
            },
            'str' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            },
            'stack' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            }
        },

        '<' : {
            'int' : {
                'int' : 'int',
                'float' : 'int',
                'str' : False,
                'stack' : False
            },
            'float': {
                'int': 'int',
                'float': 'int',
                'str': False,
                'stack': False
            },
            'str' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            },
            'stack' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            }
        },

        '<=' : {
            'int' : {
                'int' : 'int',
                'float' : 'int',
                'str' : False,
                'stack' : False
            },
            'float': {
                'int': 'int',
                'float': 'int',
                'str': False,
                'stack': False
            },
            'str' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            },
            'stack' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            }
        },
        
        '==' : {
            'int' : {
                'int' : 'int',
                'float' : 'int',
                'str' : False,
                'stack' : False
            },
            'float': {
                'int': 'int',
                'float': 'int',
                'str': False,
                'stack': False
            },
            'str' : {
                'int' : False,
                'float' : False,
                'str' : 'int',
                'stack' : False
            },
            'stack' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            }
        },

        '!=' : {
            'int' : {
                'int' : 'int',
                'float' : 'int',
                'str' : False,
                'stack' : False
            },
            'float': {
                'int': 'int',
                'float': 'int',
                'str': False,
                'stack': False
            },
            'str' : {
                'int' : False,
                'float' : False,
                'str' : 'int',
                'stack' : False
            },
            'stack' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            }
        },

        'and' : {
            'int' : {
                'int' : 'int',
                'float' : False,
                'str' : False,
                'stack' : False
            },
            'float': {
                'int': False,
                'float': False,
                'str': False,
                'stack': False
            },
            'str' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            },
            'stack' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            }
        },

        'or' : {
            'int' : {
                'int' : 'int',
                'float' : False,
                'str' : False,
                'stack' : False
            },
            'float': {
                'int': False,
                'float': False,
                'str': False,
                'stack': False
            },
            'str' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            },
            'stack' : {
                'int' : False,
                'float' : False,
                'str' : False,
                'stack' : False
            }
        },

        '=' : {
            'int' : {
                'int' : 'int',
                'float' : 'float',
                'str' : 'str',
                'stack' : False
            },
            'float': {
                'int': 'int',
                'float': 'float',
                'str': 'str',
                'stack': False
            },
            'str' : {
                'int': 'int',
                'float': 'float',
                'str': 'str',
                'stack' : False
            },
            'stack' : {
                'int': 'int',
                'float': 'float',
                'str': 'str',
                'stack' : False
            }
        }
    }

    # TODO : agregar bools a cubo

    types = ['stack', 'int', 'float', 'str']

    def is_valid(self, op, left, right):
        if not left in self.types or not right in self.types:
            raise Exception('Cannot perform operation '+op+' on class instances.') 
        result_type = self.oracle[op][left][right]
        if result_type:
            return result_type
        raise Exception('Cannot use operand '+op+' between types '+left+' and '+right)

    def can_assign(self, type1, type2):
        if type1 != type2:
            raise Exception('Assignment must be of the same object type')
