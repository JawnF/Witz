import ply.yacc as yacc
from lexicon import tokens
from manager import StatementManager
manager = StatementManager()

# Grammar for the general structure of the program
def p_program(p):
    '''program : classes functions statements
    '''
    manager.create_quads_txt()









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
    manager.end_class_scope()

def p_inheritance(p):
    '''inheritance : '<' ID check_class '>'
                   | empty
    '''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = None    

def p_params(p):
    '''params : '(' attrs ')'
    '''
    p[0] = p[2]

def p_attrs(p):
    '''attrs : attr attrs_alt
             | empty
    '''
    if len(p) > 2:
        p[0] = [p[1]] + p[2] 
    else:
        p[0] = []

def p_attrs_alt(p):
    '''attrs_alt : ',' attr attrs_alt
                 | empty
    '''
    if len(p) > 2:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

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
    manager.close_function_scope()

def p_return_type(p):
    '''return_type : VOID
                   | type
    '''
    p[0] = p[1]

def p_func_block(p):
    '''func_block : '{' statements return '}'
    '''
    
def p_return(p):
    '''return : RETURN exp ';'
              | empty
    '''
    if(len(p) > 3):
        # table.check_return(p[2][1])
        return_value = p[2]
        manager.return_value(return_value)
    else:
        manager.return_void()
        # table.check_return('void')









# 
# Rules for STATEMENTS
# 
def p_statements(p):
    '''statements : statement statements
                  | empty
    '''

def p_statement(p):
    '''statement : declaration
                 | print_stmt
                 | if_block
                 | while_block
                 | for_block
                 | expr
    '''

def p_declaration(p):
    '''declaration : '$' attr 
    '''
    p[0] = (manager.declare(p[2]), p[2][1])
    
def p_attr(p):
    '''attr : ID ':' type
            | ID ':' stack_type
    '''
    # table.neg_lookup(p[1])
    p[0] = (p[1], p[3])

def p_type(p):
    '''type : INT_TYPE
            | FLOAT_TYPE
            | STRING_TYPE
            | BOOLEAN_TYPE
            | ID check_class
    '''
    p[0] = p[1]

def p_stack_type(p):
    '''stack_type : STACK '(' type ')'
    '''
    p[0] = (p[1], p[3])

def p_print_stmt(p):
    '''print_stmt : PRINT '(' exp ')' ';'
    '''
    output = p[3]
    manager.print_output(output)










# 
# Rules for EXPRESSIONS
# 
def p_expr(p):
    '''expr : exp ';'
    '''
    temp_dir = p[1]
    manager.free_temp_memory(temp_dir)

def p_exp(p):
    '''exp : read 
           | math_or 
           | assign
           | string
           | new
           | stack_call
    '''
    p[0] = p[1]

def p_read(p):
    '''read : READ '(' ')'
    '''
    p[0] = manager.read()

def p_assign(p):
    '''assign : var '=' exp
    '''
    var = p[1]
    value = p[3]
    # table.check_variable_symbol(prop)
    # oracle.can_assign(p[1].var_type, p[3][1])
    # quads.generate(p[2], p[3], None, p[1])
    # p[0] = p[3]
    p[0] = manager.assign(value, var)
   
def p_string(p):
    '''string : STRING
    '''
    value = p[1]
    p[0] = manager.string_constant(value)
    # p[0] = (p[1], 'str')

def p_var(p):
    '''var : prop 
           | declaration
    '''
    p[0] = p[1]

def p_new(p):
    '''new : NEW constructor_call
    '''
    p[0] = p[2]

def p_constructor_call(p):
    '''constructor_call : ID '(' args ')'
    '''
    # constructor = p[1]
    # var_type = p[-3][1]
    # table.check_new(constructor, var_type)
    class_name = p[1]
    args = p[3]
    p[0] = (manager.instantiate(class_name), class_name, args)

def p_stack_call(p):
    '''stack_call : ID '.' stack_method
    '''
    # table.check_stack(p[1])
    manager.is_stack_type(p[1])

def p_stack_method(p):
    '''stack_method : POP '(' ')'
                    | PUSH '(' prop ')'
                    | PEEK '(' ')'
    '''









# 
# Rules for LOGIC expressions
# 
def p_math_or(p):
    '''math_or : math_and math_or_alt
    '''
    p[0] = p[2]
    if p[2] == None:
        p[0] = p[1]

def p_math_or_alt(p):
    '''math_or_alt : OR math_and new_quad math_or_alt
                   | empty
    '''
    if len(p) > 2:
        p[0] = p[3]

def p_math_and(p):
    '''math_and : math_comp math_and_alt
    '''
    p[0] = p[2]
    if p[2] == None:
        p[0] = p[1]

def p_math_and_alt(p):
    '''math_and_alt : AND math_comp new_quad math_and_alt
                    | empty
    '''
    if len(p) > 2:
        p[0] = p[3]

def p_math_comp(p):
    '''math_comp : math_exp math_comp_alt
    '''
    p[0] = p[2]
    if p[2] == None:
        p[0] = p[1]

def p_math_comp_alt(p):
    '''math_comp_alt : comparison_op math_exp new_quad
                     | empty
    '''
    if len(p) > 2:
        p[0] = p[3]

def p_comparison_op(p):
    '''comparison_op : '<'
                     | '>'
                     | EQ
                     | NE
                     | LE
                     | GE
    '''
    p[0] = p[1]









# 
# Rules for MATH expressions
#
def p_math_exp(p):
    '''math_exp : term math_exp_alt
    '''
    p[0] = p[2]
    if p[2] == None:
        p[0] = p[1]

def p_math_exp_alt(p):
    '''math_exp_alt : '+' term new_quad math_exp_alt
                    | '-' term new_quad math_exp_alt 
                    | empty 
    '''
    if len(p) > 2:
        p[0] = p[3]

def p_term(p):
    '''term : factor term_alt
    '''
    p[0] = p[2]
    if p[2] == None:
        p[0] = p[1]
    
def p_term_alt(p):
    '''term_alt : '*' factor new_quad term_alt 
                | '/' factor new_quad term_alt
                | empty
    '''
    if len(p) > 2:
        p[0] = p[3]

#    ---------------------------------------------- Vamos aqui... hacia arriba
def p_factor(p):
    '''factor : prop
              | number
              | call 
              | '(' math_or ')'
    '''
    item = p[1]
    if p[1] == '(':
        item = p[2]
    p[0] = item

def p_prop(p):
    '''prop : THIS '.' ID
            | ID '.' ID
            | ID
    '''
    if p[1] == 'this':
        # First rule
        prop_id = p[3]
        p[0] = manager.this_property(prop_id)
    elif len(p) == 4:
        # Second rule
        var_id = p[1]
        prop_id = p[3]
        p[0] = manager.var_property(var_id, prop_id)
    else:
        # Third rule
        prop_id = p[1]
        p[0] = manager.id_property(prop_id)
   
def p_number(p):
    '''number : FLOAT empty
              | INT
    '''
    value = p[1]
    if len(p) > 2:
        # FLOAT
        p[0] = manager.float_constant(value)
    else:
        # INT
        p[0] = manager.int_constant(value)
    # p[0] = (p[1], type(p[1]).__name__)









# 
# Rules for FUNCTION CALLS
# 
def p_call(p):
    '''call : prop '(' args ')'
    '''
    # table.check_params(p[1], p[3])
    manager.check_call_validity(p[1][0], p[3])

def p_args(p):
    '''args : exp args_aux
            | empty
    '''
    if len(p) > 2:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_args_aux(p):
    '''args_aux : ',' exp args_aux
                | empty
    '''
    if len(p) > 2:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []









# 
# Rules for FLOW CONTROL
# 
def p_if_block(p):
    '''if_block : IF '(' exp exp_evaluation  ')' block 
                | IF '(' exp exp_evaluation ')' block after_if_block ELSE block
    '''
    manager.flow.if_after_block()

def p_while_block(p):
    '''while_block : WHILE '(' leave_breadcrumb exp exp_evaluation ')' block
    '''
    manager.flow.while_after_block()

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
    op = p[-2]
    left = p[-3]
    right = p[-1]
    p[0] = manager.operate(op, left, right)
    # oracle.is_valid(op, left[1], right[1])
    # temp = Temp(res_type)
    # quads.generate(op, left[0], right[0], temp)
    # p[0] = (temp, res_type)

# Rule in charge of creating and opening a new class scope
def p_scope_class(p):
    '''scope_class : empty
    '''
    class_name = p[-3]
    parent_class = p[-2]
    # table.store(class_name, ClassSymbol(parent_class), 'class')
    manager.start_class_scope(class_name, parent_class)

# Rule in charge of creating a new function scope
def p_scope_function(p):
    '''scope_function : empty
    '''
    function_name = p[-5]
    return_type = p[-2]
    params = p[-1]
    # table.store(function_name, FunctionSymbol(return_type, params),'function')
    manager.start_function_scope(function_name, return_type, params)

def p_check_class(p):
    '''check_class : empty
    '''
    # table.check_class(p[-1])
    manager.check_class_exists(p[-1])

def p_neg_lookup(p):
    '''neg_lookup : empty
    '''
    # table.local_neg_lookup(p[-1])
    manager.id_does_not_exist(p[-1])

# Rule in charge of storing the attributes of the class
def p_store_attributes(p):
    '''store_attributes : empty
    '''
    manager.store_class_attributes(p[-2])


# Flow controls

def p_exp_evaluation(p):
    '''exp_evaluation : empty
    '''
    manager.flow.exp_evaluation()

def p_after_if_block(p):
    '''after_if_block : empty
    '''
    # flow.if_else_after_if_block() 
    manager.flow.if_else_after_if_block()

def p_leave_breadcrumb(p):
    '''leave_breadcrumb : empty
    '''
    manager.flow.while_leave_breadcrumb()

parser = yacc.yacc()
