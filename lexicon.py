import ply.lex as lex

# Estas son las palabras reservadas que generan tokens
reserved = {
	'int' 		: 'INT_TYPE',
	'float' 	: 'FLOAT_TYPE',
    'bool'      : 'BOOLEAN_TYPE',
    'str'       : 'STRING_TYPE',
    'read'   	: 'READ',
	'print' 	: 'PRINT',
	'if' 		: 'IF',
	'else' 		: 'ELSE',
    'while'     : 'WHILE',
    'or'        : 'OR',
    'and'       : 'AND',
    'this'      : 'THIS',
    'new'       : 'NEW',
    'pop'       : 'POP',
    'peek'      : 'PEEK',
    'size'      : 'SIZE',
    'push'      : 'PUSH',
    'stack'     : 'STACK',
    'this'      : 'THIS',
	'void'		: 'VOID'
	}

# Pasa's default tokens
tokens = [
    'ID',
	'INT',
	'FLOAT',
	'STRING',
	# operators
    'EQ', # equal
	'NE', # not equal
	'GE', # greater or equal
	'LE', # less or equal
    # Witz custom declaration
    'RETURN',
	] + list(reserved.values())

# Estos son los caracteres que el lexer individualmente como tokens
literals = r';,.:{}()=<>+-*/$@#~'

# Token Rules
def t_ID(t):
	r'[a-zA-Z_][a-zA-Z0-9_]*'
	if t.value == 'true':
		t.type = 'INT'
		t.value = 1
	elif t.value == 'false':
		t.type = 'INT'
		t.value = 0
	else:
		t.type = reserved.get(t.value, 'ID')
	return t

def t_FLOAT(t):
	r'[0-9]*\.[0-9]+'
	t.value = float(t.value)
	return t

def t_INT(t):
	r'[0-9]+'
	t.value = int(t.value)
	return t

def t_STRING(t):
	r'(".*?")|(\'.*?\')'
	t.value = t.value.strip("\"\'")
	return t

# Error handling rule
def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

t_NE = r'!='

t_EQ = r'=='

t_LE = r'<='

t_GE = r'>='

t_RETURN = r'<-'

t_ignore = ' \t\n'



lex.lex()