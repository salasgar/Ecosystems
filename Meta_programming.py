from SYNTAX import *


No_effect_commands = ['help', 'comment', 'label']



Dictionary_of_operators_output_function_in_text = {

    # BINARY:
    'op': "lambda x, y: 'op(' + x + ', ' + y + ')'", #formal operator for debugging purpose
    'op_': "lambda x, y: '(' + x + ' op ' + y + ')'", #formal operator for debugging purpose
    '+': "lambda x, y: x + y",
    '-': "lambda x, y: x - y",
    '*': "lambda x, y: x * y",
    '/': "lambda x, y: x / y",
    '**': "lambda x, y: x ** y",
    '//': "lambda x, y: x // y",
    '%': "lambda x, y: x % y",
    'mod': "lambda x, y: x % y",
    '>': "lambda x, y: x > y",
    '<': "lambda x, y: x < y",
    '>=': "lambda x, y: x >= y",
    '<=': "lambda x, y: x <= y",
    '==': "lambda x, y: x == y",
    '!=': "lambda x, y: x != y",
    'in': "lambda x, y: x in y",
    'random integer': "randint",  # random integer between x and y
    'randint': "randint",  # random integer between x and y
    'gauss': "gauss", # random value, normal distribution with mean x and variance y
    'uniform': "uniform", # random value, uniform distribution in [x, y]
    
    # Logic operators:
    'and': "lambda x, y: x and y",
    'AND': "lambda x, y: x and y",
    '&': "lambda x, y: x and y",
    '&&': "lambda x, y: x and y",
    'or': "lambda x, y: x or y",
    'OR': "lambda x, y: x or y",
    '|': "lambda x, y: x or y",
    '||': "lambda x, y: x or y",
    'xor': "lambda x, y: (x and not y) or (y and not x)",
    'XOR': "lambda x, y: (x and not y) or (y and not x)",

    # UNARY:
    'abs': "abs",
    'minus': "lambda x: -x",
    'sqrt': "sqrt",
    'log': "log",
    'exp': "exp",
    'sigmoid': "sigmoid",
    'sin': "sin",
    'cos': "cos",
    'tan': "tan",
    'tg':  "tan",
    'round': "lambda x: round(x, 0)",
    'int': "lambda x: int(x)",
    'roundint': "lambda x: int(round(x, 0))",
    'random boolean': "random_boolean",
    'randbool': "random_boolean",
    'random true': "random_boolean",
    'chi-squared': "chi_squared", # random value, chi-squared distribution with given degree of freedom k
    'shuffle': "shuffle_function",
    'not': "lambda x: not x",
    'NOT': "lambda x: not x",

    # Literal operator returns its input without evaluate it:
    'literal': "lambda x: x"
    }




def check_number_of_inputs_in_text(operator):
    if operator in Operators_with_list_inputs:
        return 'lambda inputs: is_list(inputs)'
    elif operator in Unary_operators:
        return 'lambda inputs: not is_tuple_or_list(inputs)'
    elif operator in Associative_operators or operator == 'choice':
        return 'lambda inputs: is_tuple_or_list(inputs) and (len(inputs) > 1)'
    elif operator in Binary_operators:
        return 'lambda inputs: is_tuple_or_list(inputs) and (len(inputs) == 2)'
    else:
        return 'lambda inputs: True'

def type_of_inputs(operator):
    if operator in Operators_with_inputs_of_any_type:
        return 'Any type'
    elif operator in Operators_with_numeric_inputs:
        return 'Number'
    elif operator in Operators_with_boolean_inputs:
        return 'Boolean'
    elif operator in Operators_with_list_inputs:
        return 'List'
    else:
        print operator
        error_maker = 1/0

def type_of_output(operator):
    if operator in Operators_with_output_of_any_type:
        return 'Any type'
    elif operator in Operators_with_numeric_output:
        return 'Number'
    elif operator in Operators_with_boolean_output:
        return 'Boolean'
    elif operator in Operators_with_list_output:
        return 'List'
    else:
        error_maker = 1/0

def output_function_in_text(operator):
    return Dictionary_of_operators_output_function_in_text[operator]

def Make_operator_definition(operator):
    return """
    '{0}': {1}
        'check number of inputs': {2},
        'type of inputs': '{3}',
        'type of output': '{4}',
        'output function': {5}
    {6},""".format(
        operator, 
        '{',
        check_number_of_inputs_in_text(operator),
        type_of_inputs(operator),
        type_of_output(operator),
        output_function_in_text(operator),
        '}'
        )
print "\n"*200
for operator in All_operators:
    print Make_operator_definition(operator)

