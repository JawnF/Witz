import ply.yacc as yacc
from lexicon import tokens

# Grammar for the general structure of the program
def p_program(p):
    '''program : classes functions statements
    '''









# 
#       Rules for CLASSES
# 
def p_classes(p):
    '''classes : class classes
               | empty
    '''

def p_class(p):
    '''class : '@' ID inheritance params scope_class store_attributes class_block
    '''

def p_inheritance(p):
    '''inheritance : '<' ID check_class '>'
                   | empty
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

def p_class_block(p):
    '''class_block : '{' functions '}'
    '''









# 
#       Rules for FUNCTIONS
# 
def p_functions(p):
    '''functions : function functions
                 | empty
    '''

def p_function(p):
    '''function : '#' ID neg_lookup ':' return_type params scope_function func_block
    '''

def p_return_type(p):
    '''return_type : VOID
                   | type
    '''

def p_func_block(p):
    '''func_block : '{' statements return '}'
    '''
    
def p_return(p):
    '''return : RETURN exp ';'
              | empty
    '''









# 
# Rules for STATEMENTS
# 
def p_statements(p):
    '''statements : statement statements
                  | empty
    '''

def p_statement(p):
    '''statement : declaration ';'
                 | print_stmt
                 | if_block
                 | while_block
                 | for_block
                 | expr
    '''

def p_declaration(p):
    '''declaration : '$' attr 
    '''
    
def p_attr(p):
    '''attr : ID ':' type
            | ID ':' stack_type
    '''

def p_type(p):
    '''type : INT_TYPE
            | FLOAT_TYPE
            | STRING_TYPE
            | BOOLEAN_TYPE
            | ID check_class
    '''

def p_stack_type(p):
    '''stack_type : STACK '(' type ')'
    '''

def p_print_stmt(p):
    '''print_stmt : PRINT '(' exp ')' ';'
    '''










# 
# Rules for EXPRESSIONS
# 
def p_expr(p):
    '''expr : exp ';'
    '''

def p_exp(p):
    '''exp : read 
           | math_or 
           | assign
           | string
           | new
           | stack_call
    '''

def p_read(p):
    '''read : READ '(' ')'
    '''

def p_assign(p):
    '''assign : var '=' exp
    '''
   
def p_string(p):
    '''string : STRING
    '''

def p_var(p):
    '''var : prop 
           | declaration
    '''

def p_new(p):
    '''new : NEW constructor_call
    '''

def p_constructor_call(p):
    '''constructor_call : ID '(' args ')'
    '''

def p_stack_call(p):
    '''stack_call : ID '.' stack_method
    '''

def p_stack_method(p):
    '''stack_method : POP '(' ')'
                    | PUSH '(' exp ')'
                    | PEEK '(' ')'
    '''
#    ---------------------------------------------- Vamos aqui... hacia arriba









# 
# Rules for LOGIC expressions
# 
def p_math_or(p):
    '''math_or : math_and math_or_alt
    '''

def p_math_or_alt(p):
    '''math_or_alt : OR math_and new_quad math_or_alt
                   | empty
    '''

def p_math_and(p):
    '''math_and : math_comp math_and_alt
    '''

def p_math_and_alt(p):
    '''math_and_alt : AND math_comp new_quad math_and_alt
                    | empty
    '''

def p_math_comp(p):
    '''math_comp : math_exp math_comp_alt
    '''

def p_math_comp_alt(p):
    '''math_comp_alt : comparison_op math_exp new_quad
                     | empty
    '''

def p_comparison_op(p):
    '''comparison_op : '<'
                     | '>'
                     | EQ
                     | NE
                     | LE
                     | GE
    '''









# 
# Rules for MATH expressions
#
def p_math_exp(p):
    '''math_exp : term math_exp_alt
    '''

def p_math_exp_alt(p):
    '''math_exp_alt : '+' term new_quad math_exp_alt
                    | '-' term new_quad math_exp_alt 
                    | empty 
    '''

def p_term(p):
    '''term : factor term_alt
    '''
    
def p_term_alt(p):
    '''term_alt : '*' factor new_quad term_alt 
                | '/' factor new_quad term_alt
                | empty
    '''

def p_factor(p):
    '''factor : prop
              | number
              | call 
              | '(' math_or ')'
    '''

def p_prop(p):
    '''prop : THIS '.' ID
            | ID '.' ID
            | ID
    '''
   
def p_number(p):
    '''number : FLOAT empty
              | INT
    '''








# 
# Rules for FUNCTION CALLS
# 
def p_call(p):
    '''call : prop '(' args ')'
    '''

def p_args(p):
    '''args : exp args_aux
            | empty
    '''

def p_args_aux(p):
    '''args_aux : ',' exp args_aux
                | empty
    '''









# 
# Rules for FLOW CONTROL
# 
def p_if_block(p):
    '''if_block : IF '(' exp exp_evaluation  ')' block 
                | IF '(' exp exp_evaluation ')' block after_if_block ELSE block
    '''

def p_while_block(p):
    '''while_block : WHILE '(' leave_breadcrumb exp exp_evaluation ')' block
    '''

def p_for_block(p):
    '''for_block : FOR number FOR_TO number SKIP number block
    '''

def p_block(p):
    '''block : '{' statements '}'
    '''









# 
# OTHER Rules
# 
def p_empty(p):
	'empty :'
	pass

def p_error(p):
    print("Syntax error in input!")














# Semantic actions 
        
def p_new_quad(p):
    '''new_quad : empty
    '''

# Rule in charge of creating and opening a new class scope
def p_scope_class(p):
    '''scope_class : empty
    '''

# Rule in charge of creating a new function scope
def p_scope_function(p):
    '''scope_function : empty
    '''

def p_check_class(p):
    '''check_class : empty
    '''

def p_neg_lookup(p):
    '''neg_lookup : empty
    '''

# Rule in charge of storing the attributes of the class
def p_store_attributes(p):
    '''store_attributes : empty
    '''


# Flow controls

def p_exp_evaluation(p):
    '''exp_evaluation : empty
    '''

def p_after_if_block(p):
    '''after_if_block : empty
    '''

def p_leave_breadcrumb(p):
    '''leave_breadcrumb : empty
    '''

parser = yacc.yacc()
