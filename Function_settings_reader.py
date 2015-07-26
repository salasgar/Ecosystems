from SYNTAX import *
from Basic_tools import *

class Function_maker:
    """ 
        This object reads function settings like:
    
                        {'initial value #x #y': {
                            'if': (
                                {'random true': 0.03},
                                {'uniform': [0, 10]},
                                {'*': (2.5, '#x', '#y')}
                            )}
                        }

        and returns an actual function.

        All methods of this class must be treated as private, but:

                read_function_settings(self, function_name_with_tags, function_settings)

                        and

                turn_settings_into_functions(self, settings, caller)
    """
    def __init__(self, parent_ecosystem, ecosystem_settings, error_messenger = default_error_messenger):
        self.parent_ecosystem = parent_ecosystem
        self.ecosystem_settings = ecosystem_settings
        self.error_messenger = error_messenger
        self.all_operators = deepcopy(All_operators)
        self.all_main_command_names = (
            self.all_operators 
            + Commands_that_comunicate_an_organism_with_its_environment 
            + ['literal']
        )
        self.operator_definitions = deepcopy(Operator_definitions)
        self.all_gene_names = extract_all_gene_names(ecosystem_settings)
        self.biotope_feature_names = extract_biotope_feature_names(ecosystem_settings)
        self.ecosystem_feature_names = extract_ecosystem_feature_names(ecosystem_settings)
        self.all_feature_names = self.biotope_feature_names + self.ecosystem_feature_names
        self.tags_list = []
        for feature_name in self.biotope_feature_names:
            if self.is_two_dimensional_feature(feature_name):
                self.add_feature_operators(feature_name)
        self.initialize_new_operators()

    def initialize_new_operators(self):
        if 'new operators' in self.ecosystem_settings:
            new_operators = [
                operator for operator in self.ecosystem_settings['new operators'].keys() 
                if not operator in No_effect_commands
                ]
            self.all_operators += new_operators  
            self.all_main_command_names += new_operators
            progressing = True
            while progressing:
                progressing = False
                for operator_name in self.ecosystem_settings['new operators']:
                    if not operator_name in self.operator_definitions:
                        operator_settings = self.ecosystem_settings['new operators'][operator_name]
                        if self.check_new_operators(operator_settings, new_operators):
                            self.add_new_operator(operator_name, operator_settings)
                            progressing = True

    def check_new_operators(self, operator_settings, new_operators):
        all_strings = extract_all_strings(operator_settings)
        for item in all_strings:
            if item in new_operators and not item in self.operator_definitions:
                return False
        return True

    def add_new_operator(self, operator_name, operator_settings):
        definition = deepcopy(operator_settings)
        for item in definition:
            if remove_tags(item) == 'output function':
                output_function_name = item
        definition['output function'] = self.read_function_settings(
            output_function_name, 
            definition[output_function_name]
            )
        self.operator_definitions[operator_name] = definition

    def add_feature_operators(self, feature_name):
        self.operator_definitions['#biotope ' + feature_name] = {
            'check number of inputs': lambda inputs: \
                is_tuple_or_list(inputs) and (len(inputs) == 2),
            'type of inputs': 'Number',
            'type of output': 'Number',
            'output function': lambda x, y: \
                self.parent_ecosystem.biotope.biotope_features[feature_name].get_value(x, y)
        }
        self.operator_definitions['extract #biotope ' + feature_name] = {
            'check number of inputs': lambda inputs: \
                is_tuple_or_list(inputs) and (len(inputs) == 3),
            'type of inputs': 'Number',
            'type of output': 'Number',
            'output function': lambda x, y, amount: \
                self.parent_ecosystem.biotope.biotope_features[feature_name].modify(x, y, -amount)
        }
        self.operator_definitions['extract #biotope ' + feature_name + ' (percentage)'] = {
            'check number of inputs': lambda inputs: \
                is_tuple_or_list(inputs) and (len(inputs) == 3),
            'type of inputs': 'Number',
            'type of output': 'Number',
            'output function': lambda x, y, amount: \
                self.parent_ecosystem.biotope.biotope_features[feature_name].modify_proportionally(x, y, -amount)
        }
        self.operator_definitions['secrete #biotope ' + feature_name] = {
            'check number of inputs': lambda inputs: \
                is_tuple_or_list(inputs) and (len(inputs) == 3),
            'type of inputs': 'Number',
            'type of output': 'Number',
            'output function': lambda x, y, amount: \
                self.parent_ecosystem.biotope.biotope_features[feature_name].modify(x, y, amount)
        }
        self.operator_definitions['secrete #biotope ' + feature_name + ' (percentage)'] = {
            'check number of inputs': lambda inputs: \
                is_tuple_or_list(inputs) and (len(inputs) == 3),
            'type of inputs': 'Number',
            'type of output': 'Number',
            'output function': lambda x, y, amount: \
                self.parent_ecosystem.biotope.biotope_features[feature_name].modify_proportionally(x, y, amount)
        }
        new_operators = [
            '#biotope ' + feature_name,
            'extract #biotope ' + feature_name,
            'extract #biotope ' + feature_name + ' (percentage)',
            'secrete #biotope ' + feature_name,
            'secrete #biotope ' + feature_name + ' (percentage)'
        ]
        self.all_operators += new_operators
        self.all_main_command_names += new_operators



    def is_two_dimensional_feature(self, feature_name):
        if (
            'biotope features' in self.ecosystem_settings['biotope'] and
            feature_name in self.ecosystem_settings['biotope']['biotope features'] and
            'matrix size' in self.ecosystem_settings['biotope']['biotope features'][feature_name]
            ):
            return True
        else:
            return False

    def make_function_from_string(self, function_settings):
        if function_settings in self.tags_list:
            """ EXAMPLE:
                'my_function #x #y': '#x'
            """
            tag_position = self.tags_list.index(function_settings)
            return lambda *arguments: arguments[tag_position]
        else:
            hash_position = function_settings.find('#')
            if hash_position == 0:
                """ EXAMPLE:
                    'my function #prey': '#prey defense capacity'
                """
                length = function_settings.find(' ')
                tag = function_settings[:length]
                attribute_name = function_settings[length+1:]
                if tag in self.tags_list:
                    tag_position = self.tags_list.index(tag)
                    return lambda *arguments: arguments[tag_position][attribute_name]
                elif tag in ['#ecosystem', '#biotope']:
                    """ EXAMPLE:
                        Inside 'constraints', 'cost' or 'genes':
                        '#ecosystem maximum population allowed'
                    """
                    if attribute_name in self.ecosystem_feature_names:
                        return lambda *arguments: arguments[0].parent_ecosystem.\
                            ecosystem_features[attribute_name].get_value()
                    elif attribute_name in self.biotope_feature_names:
                        return lambda *arguments: arguments[0].parent_ecosystem.biotope.\
                            biotope_features[attribute_name].get_value()
                    else:
                        self.error_messenger(
                            'Unknown feature', 
                            attribute_name, 
                            'in', 
                            function_settings
                        )
                        error_maker = 1/0
                else:
                    self.error_messenger(
                        'Syntax error in ', 
                        function_settings, 
                        tag, 
                        'not in tags list', 
                        self.tags_list
                    )
                    error_maker = 1/0
            elif hash_position == -1:
                if function_settings in self.all_gene_names:
                    """ EXAMPLE:
                        'attack capacity'
                    """
                    return lambda *arguments: arguments[0][function_settings]
                elif (
                    function_settings in self.ecosystem_feature_names and 
                    self.tags_list[0] == '#ecosystem'
                    ):
                    """ EXAMPLE:
                        Inside 'ecosystem features':
                        '#ecosystem maximum population allowed'
                    """
                    return lambda *arguments: arguments[0].ecosystem_features[function_settings].get_value()
                elif (
                    function_settings in self.biotope_feature_names and 
                    self.tags_list[0] == '#biotope'
                    ):
                    """ EXAMPLE:
                        Inside 'biotope features':
                        '#ecosystem maximum population allowed'
                    """
                    return lambda *arguments: arguments[0].biotope_features[function_settings].get_value()
                elif function_settings == 'normalized location x':
                    return lambda *arguments: (
                        float(arguments[0]['location'][0]) / 
                        arguments[0].parent_ecosystem.biotope.size_x()
                        ) 
                elif function_settings == 'normalized location y':
                    return lambda *arguments: (
                        float(arguments[0]['location'][1]) / 
                        arguments[0].parent_ecosystem.biotope.size_y()
                        )
                else:
                    """ EXAMPLE:
                        The value of a gene could be a string, like 'Plants':

                        {'if': (
                            {'!=': (
                                'category name',
                                'Plants'
                            )},
                            0,
                            1
                        )}

                        In this example, function_settings = 'Plants'
                    """
                    return lambda *arguments: function_settings
            else:
                self.error_messenger('Syntax error. ', function_settings)
                error_maker = 1/0

    def apply_associative_operator(self, main_operation, inputs):
        """ EXAMPLE:
            {'+': (1, 2, 3, 4, 5)}
            In this case we have to apply several times the operator '+'
        """
        return reduce(main_operation, inputs[1:], inputs[0])

    def main_command(self, expression, error_messenger):
        if is_dict(expression):
            for command in expression:
                if command in self.all_main_command_names: # not all commands can be the main command. For example 'allowed interval' of 'help' can't be main commands
                    return command
        self.error_messenger('Syntax error. Command not found in', expression)
        return None

    def make_function_from_dict(self, function_settings):
        command = self.main_command(function_settings, self.error_messenger)
        if command in function_settings:
            inputs = function_settings[command]
        else:
            self.error_messenger('Main command not found in', function_settings)
            print 'ALL MAIN COMMANDS:'
            for one_command in self.all_main_command_names:
                print one_command
            error_maker = 1/0

        if command == 'literal':
            return lambda *arguments: inputs # 'literal' operator returns its input without evaluate it
        
        elif command == 'cost':
            if is_string(inputs):
                substance_name = 'energy reserve'
                action_name = inputs
            elif is_tuple_or_list(inputs):
                substance_name = inputs[1]
                action_name = inputs[0]
            elif is_dict(inputs):
                substance_name = inputs['substance']
                action_name = inputs['action']
            #print "action_name", action_name, "substance_name", substance_name, "inputs", inputs
            return lambda *arguments: arguments[0].parent_ecosystem\
                .costs[action_name][substance_name](arguments[0])

        elif command == 'constraint':
            return lambda *arguments: arguments[0].parent_ecosystem\
                .constraints[inputs](arguments[0])

        elif command in self.all_operators:
            inputs_function = self.make_function(inputs)
            main_operation = self.operator_definitions[command]['output function']
            if command in Associative_operators:          
                return lambda *arguments: self.apply_associative_operator(
                    main_operation, 
                    inputs_function(*arguments)
                    )
            elif command in Unary_operators:
                return lambda *arguments: main_operation(inputs_function(*arguments))
            else:
                return lambda *arguments: main_operation(*(inputs_function(*arguments)))
        else:        
            self.error_messenger('Syntax error in', function_settings)
            self.error_messenger('Unknown command', command)
            error_maker = 1/0

    def constrain_function_to_allowed_interval(self, function_to_return, interval_functions):
        bounded_value = lambda value, a, b: a if value < a else b if value > b else value
        return lambda *arguments: bounded_value(
            function_to_return(*arguments), 
            *interval_functions(*arguments)
            )

    def make_function(self, function_settings):
        if print_methods_names:
            print 'make_function', self.tags_list
            print function_settings

        if is_number(function_settings) or is_function(function_settings):
            return lambda *arguments: function_settings

        elif is_string(function_settings):
            return self.make_function_from_string(function_settings)

        elif is_tuple_or_list(function_settings):
            terms = [self.make_function(item) for item in function_settings]
            return lambda *arguments: [item(*arguments) for item in terms] # This is necessary for 'shuffle' operator
        
        elif is_dict(function_settings):
            function_to_return = self.make_function_from_dict(function_settings)
            if 'allowed interval' in function_settings:
                allowed_interval = self.make_function(function_settings['allowed interval'])
                return self.constrain_function_to_allowed_interval(
                    function_to_return, 
                    allowed_interval)
            else:
                return function_to_return


    def read_function_settings(self, function_name_with_tags, function_settings):
        """ 
        In this EXAMPLE:
    
                        {'initial value #x #y': {
                            'if': (
                                {'random true': 0.03},
                                {'uniform': [0, 10]},
                                {'*': (2.5, '#x', '#y')}
                            )}
                        }

        function_name_with_tags = 'initial value #x #y'
        function_settings = {'initial value #x #y': {
                                'if': (
                                    {'random true': 0.03},
                                    {'uniform': [0, 10]},
                                    {'*': (2.5, '#x', '#y')}
                                )}
                            }

        and this method returns an actual function that takes two arguments x and y
        """
        self.tags_list = get_tags_list(function_name_with_tags)
        function_to_return = self.make_function(function_settings)
        self.tags_list = []
        return function_to_return

    def turn_settings_into_functions(self, settings, caller):
        if not is_dict(settings):
            return self.read_function_settings(caller, settings)
        result = {}
        for item in settings:
            #print 'turning', item, 'into function', settings[item]
            function_name = remove_tags(item)
            self.tags_list = [caller] + get_tags_list(item)
            #print 'tags_list', self.tags_list
            result[function_name] = self.make_function(settings[item])
            self.tags_list = []
        if 'allowed interval' in settings:
            for function_name in result:
                result[function_name] = self.constrain_function_to_allowed_interval(
                    result[function_name],
                    result['allowed interval']
                    )
        return result

















