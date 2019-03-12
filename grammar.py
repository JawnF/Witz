import ply.yacc as yacc
from lexicon import tokens
# Grammar for the general structure of the program
def p_program(p):
    '''program : classes functions vars statements
    '''

def p_vars(p):
    '''vars : var vars
            | empty
    '''

def p_var(p):
    '''var : '$' attr init ';'
    '''

def p_attr(p):
    '''attr : ID ':' type
    '''
    
def p_init(p):
    '''init : '=' EXPR
            | empty
    '''

def p_type(p):
    '''type : INT_TYPE
            | FLOAT_TYPE
            | STRING_TYPE
            | BOOLEAN_TYPE
    '''

def p_return_type(p):
    '''return_type : VOID
                   | type
    '''

def p_classes(p):
    '''classes : class classes
               | empty
    '''

def p_class(p):
    '''class : '@' ID inheritance class_block
    '''

def p_inheritance(p):
    '''inheritance : '<' ID '>'
                   | empty
    '''
    
def p_class_block(p):
    '''class_block : '{' vars constructor functions '}'
    '''    

def p_constructor(p):
    '''constructor : '~' ID params func_block
                   | empty
    '''

def p_functions(p):
    '''functions : function functions
                 | empty
    '''

def p_function(p):
    '''function : '#' ID ':' return_type params func_block
    '''

def p_params(p):
    '''params : '(' attrs ')'
    '''

def p_attrs(p):
    '''attrs : attr attrs_alt
             | empty
    '''

def p_attrs_alt(p):
    '''attrs_alt : ',' attr attrs_alt
                 | empty
    '''

def p_func_block(p):
    '''func_block : '{' vars statements '}'
    '''

def p_statements(p):
    '''statements : statement
                  | empty
    '''

def p_statement(p):
    '''statement : assignment
                 | if_block
                 | while_block
                 | for_block
                 | print_stmt
                 | EXPR
                 | return
    '''

def p_assignment(p):
    '''assignment : prop '=' EXPR ';'
    '''

def p_prop(p):
    '''prop : THIS '.' ID
            | ID
    '''

def p_if_block(p):
    '''if_block : IF '(' EXPR ')' block
    '''

def p_while_block(p):
    '''while_block : WHILE '(' EXPR ')' block
    '''
    
def p_for_block(p):
    '''for_block : FOR number FOR_TO number SKIP number block
    '''
    
def p_print_stmt(p):
    '''print_stmt : PRINT '(' EXPR ')' ';'
    '''
    
def p_return(p):
    '''return : RETURN EXPR ';'
              | RETURN ';'
    '''

def p_block(p):
    '''block : '{' statements '}'
    '''
   
def p_number(p):
    '''number : FLOAT
              | INT
    '''

    
    
# -------------------------------------------------------


# def p_declarations(p):
# 	'''declarations : names ':' type ';' xdeclarations'''

# def p_xdeclarations(p):
# 	'''xdeclarations : names ':' type ';' xdeclarations 
# 					 | empty '''

# def p_names(p):
# 	'names : ID name'

# def p_name(p):
# 	'''name : ',' ID name
# 			| empty'''



# # Regla <ASIGNACION>
# def p_assignment(p):
# 	'''assignment : ID '=' expression ';' '''

# # Regla <ESCRITURA>
# def p_writing(p):
# 	'''writing : PRINT '(' params ')' ';' '''

# def p_params(p):
# 	'params : param xparam'

# def p_param(p):
# 	'''param : expression
# 			 | STRING '''

# def p_xparam(p):
# 	'''xparam : ',' param xparam
# 			  | empty '''

# # Regla <CONDICION>
# def p_condition(p):
# 	'''condition : IF '(' expression ')' block ';'
# 				 | IF '(' expression ')' block ELSE block ';' '''

# # Regla <EXPRESION>
# def p_expression(p):
# 	'''expression : exp comparison
# 				  | exp '''

# def p_comparison(p):
# 	'''comparison : '>' exp 
# 				  | '<' exp 
# 				  | NE exp '''

# # Regla <EXP>
# def p_exp(p):
# 	'''exp : term 
# 		   | term addsub'''

# def p_addsub(p):
# 	'''addsub : '+' term addsub
# 			  | '-' term addsub 
# 			  | empty'''

# # Regla <TERMINO>
# def p_term(p):
# 	'''term : factor
# 			| factor multdiv'''

# def p_multdiv(p):
# 	'''multdiv : '*' factor multdiv
# 			   | '/' factor multdiv 
# 			   | empty '''

# # Regla <FACTOR>
# def p_factor(p):
# 	'''factor : '(' expression ')'
# 			  | '+' const  
# 			  | '-' const
# 			  | const '''

# # Regla <VAR CTE>
# def p_const(p):
# 	'''const : ID
# 			 | INT
# 			 | FLOAT '''

def p_empty(p):
	'empty :'
	pass

def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()

# # Se puede pasar el nombre de archivo como argumento
# if (len(sys.argv) > 1):
# 	filename = sys.argv[1]

# # O se puede ingresar al correr el programa
# else:
# 	filename = raw_input('Nombre de archivo > ')

# # Leer contenido del archivo
# with open(filename,"r") as file:
# 	inp = file.read()

# # Parsear y confirmar
# result = parser.parse(inp)
# if result:
# 	print(result)