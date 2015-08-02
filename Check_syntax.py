from SYNTAX import *




# Este archivo debe ser reformado. Ahora mismo no esta en uso



# *********************************************************************************
#                                   CHECK SYNTAX:
# *********************************************************************************


def check_settings_syntax(settings, syntax, all_gene_names, all_feature_names, error_messenger = default_error_messenger):

    if '$ ALLOWED COMMANDS' in syntax:
        allowed = syntax['$ ALLOWED COMMANDS']
    else:
        allowed = []
        
    if '$ MANDATORY COMMANDS' in syntax:
        mandatory = syntax['$ MANDATORY COMMANDS']
    else:
        mandatory = []
        
    if '$ NO-EFFECT COMMANDS' in syntax:
        no_effect = syntax['$ NO-EFFECT COMMANDS'] + No_effect_commands
    else:
        no_effect = No_effect_commands
        
    for item in mandatory:
        if not item in settings:
            error_messenger("Syntax error. Attribute missing:", item)
            return False

    for item in settings:
        if not (allowed == []) and \
            not (item in allowed) and \
            not (item in mandatory) and \
            not (item in no_effect):
            error_messenger('Syntax error. Unknown attribute', item)
            return False
        elif is_dict(syntax) and item in syntax:
            if syntax[item] == '<expression>' and not check_expression(settings[item], all_gene_names, all_feature_names, error_messenger):
                error_messenger('Error in expression', settings[item])
                return False
            elif syntax[item] == '<boolean expression>' and not (
                        check_expression(settings[item], all_gene_names, all_feature_names, error_messenger) and
                        check_type_of_expression('boolean', settings[item], all_gene_names, all_feature_names, error_messenger)
                    ):
                error_messenger('Error in boolean expression', settings[item])
                return False
            elif is_dict(syntax[item]) and not check_settings_syntax(settings[item], syntax[item], all_gene_names, all_feature_names):
                error_messenger('Syntax error in', settings)
                return False

    for syntax_item in syntax:
        if syntax_item[0] == "<" and syntax_item[-1] == ">":
            for settings_item in settings:
                if not settings_item in allowed + mandatory + no_effect and \
                    not check_settings_syntax(settings[settings_item], syntax[syntax_item], all_gene_names, all_feature_names):
                    return False
    
    return True

def check_type_of_expression(type_to_check, expression, all_gene_names, all_feature_names, error_messenger):
    if type_to_check == 'Any type':
        return True
    elif (
        (type_to_check == 'Number' and is_number(expression)) or
        (type_to_check == 'Boolean' and is_boolean(expression)) or
        (type_to_check == 'List' and is_tuple_or_list(expression)) or
        (type_to_check == 'Function' and is_function(expression)) or  # 'Function', but not 'String'
        (type_to_check == 'String' and is_string(expression)) or
        (is_string(expression) and expression in all_gene_names) or # A string could be the name of a gene of any type
        (is_string(expression) and expression in all_feature_names) # A string could be the name of a feature
        ): 
        return True
    elif is_string(expression) and not (
        expression in all_gene_names or
        expression in all_feature_names or
        expression in All_action_names or
        expression in All_allowed_commands
        ):
        error_messenger(expression, 'is not a fucking gene name')
        return False
    elif is_dict(expression):
        if not check_expression(expression, all_gene_names, all_feature_names, error_messenger):
            return False
        command = main_command(expression, error_messenger)
        if (
            (type_to_check == "Number" and command in Operators_with_numeric_output) or
            (type_to_check == "Boolean" and command in Operators_with_boolean_output) or
            (type_to_check == "List" and command in Operators_with_list_output) or
            (type_to_check == "String" and command in Operators_with_string_output)): # 'String', but not 'Function'
            return True
    error_messenger("Syntax error. ", command, "doesn't return a", type_to_check)
    return False

def check_operator_input_types(operator, expression, all_gene_names, all_feature_names, error_messenger):
    inputs = expression[operator]
    if 'check inputs' in Operator_definition[operator]:
        if not Operator_definition[operator]['check inputs'](inputs):
            error_messenger("Syntax error in operator", operator, "Inputs:", inputs)
            return False
        else:
            return True
    elif 'type of inputs' in Operator_definition[operator]:        
        input_type = Operator_definition[operator]['type of inputs']
    else:
        error_messenger("Error in operator definition:", operator, Operator_definition[operator])
        error_maker = 1/0
    if operator == 'in':
        return (
            is_tuple_or_list(inputs) and 
            (len(inputs) == 2) and 
            check_type_of_expression('List', inputs[1], all_gene_names, all_feature_names, error_messenger))
    elif input_type == 'Any type':
        return True
    elif is_tuple_or_list(inputs):
        for item in inputs:
            if not check_type_of_expression(input_type, item, all_gene_names, all_feature_names, error_messenger):
                error_messenger('Type error in', expression)
                error_messenger(input_type, 'expected')
                return False
    else:   
        if not check_type_of_expression(input_type, inputs, all_gene_names, all_feature_names, error_messenger):
            error_messenger('Type error in', expression)
            error_messenger(input_type, 'expected')
            return False
    return True


def check_operator_expression(operator, expression, all_gene_names, all_feature_names, error_messenger):
    inputs = expression[operator]
    if 'check inputs' in Operator_definition[operator]:
        if not Operator_definition[operator]['check inputs'](inputs):
            error_messenger("Syntax error in operator", operator, "Inputs:", inputs)
            return False
    if 'check number of inputs' in Operator_definition[operator]:
        if not Operator_definition[operator]['check number of inputs'](inputs):
            error_messenger("Syntax error in operator", operator, "Incorrect number of inputs in:", inputs)
            return False
    if not check_operator_input_types(operator, expression, all_gene_names, all_feature_names, error_messenger):
        error_messenger("Syntax error in operator", operator, "Incorrect type of inputs in:", inputs)
        return False
    if 'allowed interval' in expression:
        interval = expression['allowed interval']
        if not (
            is_tuple_or_list(interval) and 
            (len(interval) == 2) and
            check_type_of_expression('Number', interval[0], all_gene_names, all_feature_names, error_messenger) and
            check_type_of_expression('Number', interval[1], all_gene_names, all_feature_names, error_messenger)):
            error_messenger('Error in interval', interval, 'defined in', expression)
            return False
    if operator == 'choice':
        if not ( # Conditions that "inputs" has to match:
            is_tuple_or_list(inputs) and 
            len(inputs) >= 3 and 
            check_expression(inputs, all_gene_names, all_feature_names, error_messenger)
        ):
            error_messenger('Syntax error in', expression)
            return False
        input_type = get_type_of_expression(inputs[0], error_messenger)
        for item in inputs[1:]:
            if not ( # Conditions that "item" has to match:
                is_tuple_or_list(item) and 
                len(item) == 2 and
                check_type_of_expression(input_type, item, all_gene_names, all_feature_names, error_messenger)
            ):
                error_messenger('Syntax error in', item)
                error_messenger('Syntax error in', expression)
                return False
    for instruction in expression:
        if not instruction in [operator, 'allowed interval'] + No_effect_commands:
            error_messenger('Syntax error. Unexpected command', instruction, 'in', expression)
            return False
    return True

def check_commands_in_expression(expression, error_messenger):
    count = count_elements(
        expression, 
        No_effect_commands, 
        Auxiliar_commands, 
        All_allowed_commands_in_expression)
    
    (n_No_effect_commands, n_Auxiliar_commands, n_All_allowed_commands, n_Unknown_commands) = count

    if n_Unknown_commands > 0:
        error_messenger('Syntax error. Unexpected command in', expression)
        return False
    elif n_All_allowed_commands - n_Auxiliar_commands - n_No_effect_commands != 1:
        error_messenger('Error in number of commands in', expression)
        return False
    elif n_Auxiliar_commands > 1:
        error_messenger('Error in number of commands in', expression)
        return False
    else:
        return True

def get_type_of_expression(expression, error_messenger):
    if not check_expression(expression, error_messenger):
        return 'Error in expression'
    elif is_number(expression):
        return 'Number'
    elif is_boolean(expression):
        return 'Boolean'
    elif is_tuple_or_list(expression):
        return 'List'
    elif is_string(expression):
        return 'Any type' # It could be the name of a gene of any type
    elif is_function(expression):
        return 'Function'
    elif is_dict(expression):
        command = main_command(expression)
        if command in Commands_with_numeric_output:
            return 'Number'
        elif command in Commands_with_boolean_output:
            return 'Boolean'
        elif command in Commands_with_list_output:
            return 'List'
        else:
            return 'Any type'

def check_function_expression(command, expression, all_gene_names, all_feature_names, error_messenger):
    inputs = expression[command]
    if not check_expression(inputs, all_gene_names, all_feature_names, error_messenger):
        error_messenger('Syntax error in', expression)
        return False

    elif command == 'if':
        if (is_tuple_or_list(inputs) 
            and len(inputs) == 3
            and check_type_of_expression('Boolean', inputs[0], error_messenger)
            and check_expression(inputs[1], all_gene_names, all_feature_names, error_messenger)
            and check_expression(inputs[2], all_gene_names, all_feature_names, error_messenger)):
            return True
        else:
            error_messenger('Syntax error in', expression)
            return False

    elif command in ['cost', 'constraint']:
        if not check_type_of_expression('String', inputs, all_gene_names, all_feature_names, error_messenger):
            error_messenger('Action name expected in', inputs)
            error_messenger('Syntax error in', expression)
            return False
        if 'substance' in expression and not check_type_of_expression('String', expression['substance'], all_gene_names, all_feature_names, error_messenger):
            error_messenger('Substance name expected in', expression['substance'])
            error_messenger('Syntax error in', expression)
            return False

    elif command == 'function':
        if is_function(inputs):
                    return True
        elif (check_expression(inputs, all_gene_names, all_feature_names, error_messenger) and 
            is_tuple_or_list(inputs) and
            (len(inputs) > 0) and 
            is_function(inputs[0])):
                return True
        else:
            error_messenger('Syntax error. Function expected in', expression)
            return False

    elif command == 'discrete distribution':
        if not (
            is_tuple_or_list(inputs) and 
            check_expression(inputs, all_gene_names, all_feature_names, error_messenger)
        ):
            error_messenger('Syntax error in', expression)
            return False
        for pair in inputs:
            if not (
                is_dict(pair)
                and 'value' in pair
                and check_expression(pair['value'], all_gene_names, all_feature_names, error_messenger)
                and 'probability' in pair
                and check_type_of_expression('Number', pair['probability'], all_gene_names, all_feature_names, error_messenger)
            ):
                error_messenger('Syntax error in', expression)
                return False
        return True

    else:
        error_messenger('Syntax error. Unknown command', command, 'in', expression)

def check_names(expression, all_gene_names, all_feature_names, error_messenger):
    if is_string(expression):
        if len(expression) > 0 and expression[0] == '#': # Example: '#predator attack capacity'
            return True
        name = remove_tags(expression)
        if (
            name in all_gene_names or 
            name in all_feature_names or
            name in All_action_names or
            name in All_allowed_commands
            ):
            return True
        else:
            error_messenger(expression, 'is not a gene name nor a shit', name)
            return False
    elif is_dict(expression):
        for item in expression:
            if (
                not item in No_effect_commands
                and not check_names(expression[item], all_gene_names, all_feature_names, error_messenger)
                ):
                return False
        return True
    if is_iterable(expression): # Do not use "elif" here in steed of "if" !!!
        for item in expression:
            if not check_names(item, all_gene_names, all_feature_names, error_messenger):
                return False
        return True
    else:
        return True


def check_expression(expression, all_gene_names, all_feature_names, error_messenger = default_error_messenger):
    if not check_names(expression, all_gene_names, all_feature_names, error_messenger):
        return False
    elif is_number(expression) or is_boolean(expression):
        return True
    elif is_string(expression):
        if not expression in all_gene_names and expression != 'infinity':
            error_messenger('Warning. Not a gene name:', expression) # It could be a string value or a misspelled gene name
        return True
    elif is_tuple_or_list(expression):
        for item in expression:
            if not check_expression(item, all_gene_names, all_feature_names, error_messenger):
                error_messenger('Syntax error in', expression)
                return False
        return True
    elif is_dict(expression):
        if not check_commands_in_expression(expression, error_messenger):
            return False
        command = main_command(expression, error_messenger)
        if command in All_operator_names:
            return check_operator_expression(command, expression, all_gene_names, all_feature_names, error_messenger)
        else:
            return check_function_expression(command, expression, all_gene_names, all_feature_names, error_messenger)
    else:
        error_messenger('Syntax error in', expression)
        return False



