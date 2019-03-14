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

# ----------------------- Aqui vamos en la definicion de puntos de tabla de simbolos
def p_var(p):
    '''var : '$' attr init ';'
    '''

def p_attr(p):
    '''attr : ID ':' type
    '''
    
def p_init(p):
    '''init : '=' exp
            | empty
    '''

def p_type(p):
    '''type : INT_TYPE
            | FLOAT_TYPE
            | STRING_TYPE
            | BOOLEAN_TYPE
            | STACK
    '''

def p_return_type(p):
    '''return_type : VOID
                   | type
    '''

def p_classes(p):
    '''classes : class classes
               | empty
    '''
    print(p[0])

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
    '''statement : if_block
                 | while_block
                 | for_block
                 | print_stmt
                 | expr
                 | return
    '''

def p_assign(p):
    '''assign : prop '=' expr
              | prop '=' NEW ID
    '''

def p_prop(p):
    '''prop : THIS '.' ID
            | ID '.' ID
            | ID
    '''

def p_if_block(p):
    '''if_block : IF '(' exp ')' block
                | IF '(' exp ')' block ELSE block
    '''

def p_while_block(p):
    '''while_block : WHILE '(' exp ')' block
    '''
    
def p_for_block(p):
    '''for_block : FOR number FOR_TO number SKIP number block
    '''
    
def p_print_stmt(p):
    '''print_stmt : PRINT '(' exp ')' ';'
    '''
    
def p_return(p):
    '''return : RETURN exp ';'
              | RETURN ';'
    '''

def p_block(p):
    '''block : '{' statements '}'
    '''
   
def p_number(p):
    '''number : FLOAT
              | INT
    '''

def p_expr(p):
    '''expr : exp ';'
    '''

def p_exp(p):
    '''exp : read
           | math_exp
           | logic_exp
           | assign
    '''

def p_read(p):
    '''read : READ '(' string ')'
    '''

def p_string(p):
    '''string : ID
              | STRING
    '''

def p_math_exp(p):
    '''math_exp : term math_exp_alt
    '''

def p_math_exp_alt(p):
    '''math_exp_alt : '+' term math_exp_alt
                    | '-' term math_exp_alt 
                    | empty 
    '''

def p_term(p):
    '''term : factor term_alt
    '''

def p_term_alt(p):
    '''term_alt : '*' factor term_alt 
                | '/' factor term_alt
                | empty
    '''

def p_factor(p):
    '''factor : ID
              | number
              | call
              | '(' math_exp ')' 
    '''

def p_logic_exp(p):
    '''logic_exp : log_a logic_exp_alt
    '''

def p_logic_exp_alt(p):
    '''logic_exp_alt : OR log_a logic_exp_alt
                     | empty
    '''

def p_log_a(p):
    '''log_a : log_b log_a_alt
    '''

def p_log_a_alt(p):
    '''log_a_alt : AND log_b log_a_alt
                 | empty
    '''

def p_log_b(p):
    '''log_b : '(' logic_exp ')' 
             | bool
             | comparison
             | math_exp
    '''

def p_bool(p):
    '''bool : TRUE
            | FALSE
    '''

def p_comparison(p):
    '''comparison : math_exp comparison_op math_exp
    '''

def p_comparison_op(p):
    '''comparison_op : '<'
                     | '>'
                     | EQ
                     | NE
    '''

def p_call(p):
    '''call : prop '(' args ')'
            | stack_call '(' args ')'
    '''

def p_args(p):
    '''args : exp args_aux
            | empty
    '''

def p_args_aux(p):
    '''args_aux : ',' exp args_aux
                | empty
    '''

def p_stack_call(p):
    '''stack_call : prop stack_method
    '''

def p_stack_method(p):
    '''stack_method : POP
                    | PUSH
                    | PEEK
    '''


def p_empty(p):
	'empty :'
	pass

def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()
