from syntax import All_operator_names, no_effect_directives
from syntax import Associative_operators
from syntax import Unary_operators
from syntax import directives_that_comunicate_an_organism_with_its_environment
from syntax import Operators_definitions
from basic_tools import extract_all_gene_names
from basic_tools import is_string
from basic_tools import is_dict, is_iterable
from basic_tools import is_tuple_or_list
from basic_tools import extract_biotope_feature_names
from basic_tools import extract_ecosystem_feature_names
from basic_tools import remove_tags, get_tags_list
from basic_tools import extract_all_strings
from basic_tools import print_operators, bounded_value
from basic_tools import is_number, is_function
from basic_tools import print_methods_names
from copy import deepcopy
from basic_tools import default_error_messenger


def remove_no_effect_directives(function_settings):
    if is_dict(function_settings):
        for item in no_effect_directives:
            if item in function_settings:
                del function_settings[item]
        for item in function_settings:
            remove_no_effect_directives(function_settings[item])
    elif is_iterable(function_settings):
        for item in function_settings:
            remove_no_effect_directives(item)
    return function_settings


class FunctionMaker:

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

                read_function_settings(
                    self,
                    function_name_with_tags,
                    function_settings)

                        and

                turn_settings_into_functions(self, settings, caller)
    """

    def __init__(
        self,
        parent_ecosystem,
        ecosystem_settings,
        error_messenger=default_error_messenger
    ):
        self.parent_ecosystem = parent_ecosystem
        self.ecosystem_settings = ecosystem_settings
        self.error_messenger = error_messenger
        self.all_operator_names = deepcopy(All_operator_names)
        self.associative_operators = deepcopy(Associative_operators)
        self.unary_operators = deepcopy(Unary_operators)
        self.all_main_directive_names = (
            self.all_operator_names
            + directives_that_comunicate_an_organism_with_its_environment
            + ['literal']
        )
        self.operators_definitions = deepcopy(Operators_definitions)
        self.all_gene_names = extract_all_gene_names(ecosystem_settings)
        self.biotope_feature_names = extract_biotope_feature_names(
            ecosystem_settings)
        self.ecosystem_feature_names = extract_ecosystem_feature_names(
            ecosystem_settings)
        self.all_feature_names = self.biotope_feature_names + \
            self.ecosystem_feature_names
        self.tags_list = []
        self.caller = None
        for feature_name in self.biotope_feature_names:
            if self.is_two_dimensional_feature(feature_name):
                self.add_feature_operators(feature_name)
        self.initialize_new_operators()

    def initialize_new_operators(self):
        if 'new operators' in self.ecosystem_settings:
            new_operators_settings = self.ecosystem_settings['new operators']
            new_operator_names = [
                operator for operator in new_operators_settings.keys()
                if operator not in no_effect_directives
            ]
            self.all_operator_names += new_operator_names
            self.all_main_directive_names += new_operator_names
            # The following lines are designed to initialize new operators in
            # the right order
            # so that some of them can be call others and must be initialized
            # after these others:
            progressing = True
            while progressing:
                progressing = False
                for operator_name in self.ecosystem_settings['new operators']:
                    if operator_name not in self.operators_definitions:
                        operator_settings = self.ecosystem_settings[
                            'new operators'][operator_name]
                        if self.check_new_operators(
                            operator_settings,
                            new_operator_names
                        ):
                            self.add_new_operator(
                                operator_name, operator_settings)
                            progressing = True

    def check_new_operators(self, operator_settings, new_operator_names):
        """
            If in operator_settings is there a mention to an operator
            of new_operator_names that
            hasn't yet been initialized, operator_settings can't still
            be initialized until
            all operators that it refers to are initialized.
            This function says whether operator_settings can be already
            initialized  or not.
        """
        all_strings = extract_all_strings(operator_settings)
        for item in all_strings:
            if (
                item in new_operator_names and
                item not in self.operators_definitions
                    ):
                return False
        return True

    def add_new_operator(self, operator_name, operator_settings):
        definition = deepcopy(operator_settings)
        # Find output function name:
        for item in definition:
            if remove_tags(item) == 'output function':
                output_function_name = item
        # Turn function's definition into a function:
        definition['output function'] = self.read_function_settings(
            output_function_name,
            definition[output_function_name]
        )
        # Add operator definition to self.operators_definitions:
        self.operators_definitions[operator_name] = definition
        # Add operator name to self.unary_operators or
        # self.associative_operators lists if that's the case:
        if len(get_tags_list(output_function_name)) == 1:
            self.unary_operators.append(operator_name)
        elif len(get_tags_list(output_function_name)) == 2 \
            and not (
                'is associative' in operator_settings
                and not operator_settings['is associative']
        ):
            self.associative_operators.append(operator_name)

    def add_feature_operators(self, feature_name):
        self.operators_definitions['#biotope ' + feature_name] = {
            'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 2),
            'type of inputs': 'Number',
            'type of output': 'Number',
            'output function': lambda x, y:
            self.parent_ecosystem.biotope.biotope_features[
                feature_name].get_value(x, y)
        }
        self.operators_definitions['extract #biotope ' + feature_name] = {
            'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 3),
            'type of inputs': 'Number',
            'type of output': 'Number',
            'output function': lambda x, y, amount:
            -
                self.parent_ecosystem.biotope.biotope_features[
                    feature_name].modify(x, y, -amount)
        }
        operator_name = 'extract #biotope ' + feature_name + ' (proportion)'
        self.operators_definitions[operator_name] = {
            'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 3),
            'type of inputs': 'Number',
            'type of output': 'Number',
            'output function': lambda x, y, amount:
            - self.parent_ecosystem.biotope.biotope_features[
                feature_name].modify_proportionally(x, y, -amount)
        }
        self.operators_definitions['secrete #biotope ' + feature_name] = {
            'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 3),
            'type of inputs': 'Number',
            'type of output': 'Number',
            'output function': lambda x, y, amount:
            self.parent_ecosystem.biotope.biotope_features[
                feature_name].modify(x, y, amount)
        }
        operator_name = 'secrete #biotope ' + feature_name + ' (proportion)'
        self.operators_definitions[operator_name] = {
            'check number of inputs': lambda inputs:
            is_tuple_or_list(inputs) and (len(inputs) == 3),
            'type of inputs': 'Number',
            'type of output': 'Number',
            'output function': lambda x, y, amount:
            self.parent_ecosystem.biotope.biotope_features[
                feature_name].modify_proportionally(x, y, amount)
        }
        new_operator_names = [
            '#biotope ' + feature_name,
            'extract #biotope ' + feature_name,
            'extract #biotope ' + feature_name + ' (proportion)',
            'secrete #biotope ' + feature_name,
            'secrete #biotope ' + feature_name + ' (proportion)'
        ]
        self.all_operator_names += new_operator_names
        self.all_main_directive_names += new_operator_names

    def is_two_dimensional_feature(self, feature_name):
        if (
            'biotope features' in self.ecosystem_settings[
                'biotope'] and
            feature_name in self.ecosystem_settings[
                'biotope']['biotope features'] and
            'matrix size' in self.ecosystem_settings[
                'biotope']['biotope features'][feature_name]
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
                length = function_settings.find(' ')
                tag = function_settings[:length]
                attribute_name = function_settings[length + 1:]
                if tag in self.tags_list and tag not in [
                    '#ecosystem', '#biotope'
                        ]:
                    """ EXAMPLE:
                        'my function #prey': '#prey defense capacity'
                    """
                    tag_position = self.tags_list.index(tag)
                    return lambda *arguments: arguments[tag_position][
                        attribute_name]

                elif tag in ['#ecosystem', '#biotope']:
                    """
                        Inside 'constraints', 'cost' or 'genes',
                                    self.tags_list[0] = '#organism'.
                        Then, '#ecosystem' and '#biotope' may not be
                        in self.tags_list.
                        EXAMPLE:
                        '#ecosystem maximum population allowed'
                    """
                    if attribute_name in self.ecosystem_feature_names:
                        return lambda *arguments: arguments[0].\
                            parent_ecosystem.\
                            ecosystem_features[attribute_name].get_value()
                    elif attribute_name in self.biotope_feature_names:
                        return lambda *arguments: arguments[0].\
                            parent_ecosystem.biotope.\
                            biotope_features[attribute_name].get_value()
                    else:
                        self.error_messenger(
                            'Unknown feature',
                            attribute_name,
                            'in',
                            function_settings
                        )
                        exit()
                else:
                    self.error_messenger(
                        'syntax error in ',
                        function_settings,
                        tag,
                        'not in tags list',
                        self.tags_list
                    )
                    exit()
            elif hash_position == -1:
                """
                    In this case there isn't a tag inside function_settings
                """
                if function_settings in self.all_gene_names:
                    """ EXAMPLE:
                        'attack capacity'
                        In this case we asume that
                        self.tags_list[0] = '#organism'
                    """
                    return lambda *arguments: arguments[0][function_settings]
                    # return lambda *arguments: arguments[0][
                    #     function_settings]\
                    # if self.error_messenger(arguments) else 0
                elif (
                    function_settings in self.ecosystem_feature_names
                    # and self.tags_list[0] == '#ecosystem'
                ):
                    """ EXAMPLE:
                        'maximum population allowed'
                    """
                    if self.tags_list[0] == '#ecosystem':
                        return lambda *arguments: arguments[0]\
                            .ecosystem_features[function_settings].get_value()
                    elif self.tags_list[0] in ['#biotope', '#organism']:
                        return lambda *arguments: arguments[0].\
                            parent_ecosystem.ecosystem_features[
                                function_settings].get_value()
                elif (
                    function_settings in self.biotope_feature_names
                    # and self.tags_list[0] == '#biotope'
                        ):
                    """ EXAMPLE:
                        'seasons speed'
                    """
                    if self.tags_list[0] == '#ecosystem':
                        return lambda *arguments: arguments[0]\
                            .biotope.biotope_features[
                                function_settings].get_value()
                    elif self.tags_list[0] == '#biotope':
                        return lambda *arguments: arguments[0]\
                            .biotope_features[function_settings].get_value()
                    elif self.tags_list[0] == '#organism':
                        return lambda *arguments: arguments[0]\
                            .parent_ecosystem.biotope.biotope_features[
                                function_settings].get_value()

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
                elif function_settings == 'normalized abcissa unit':
                    if self.tags_list[0] == '#ecosystem':
                        return lambda *arguments: (
                            1.0 / arguments[0].biotope.size_x()
                        )
                    else:
                        return lambda *arguments: (
                            1.0 /
                            arguments[0].parent_ecosystem.biotope.size_x()
                        )
                elif function_settings == 'normalized ordinate unit':
                    if self.tags_list[0] == '#ecosystem':
                        return lambda *arguments: (
                            1.0 / arguments[0].biotope.size_y()
                        )
                    else:
                        return lambda *arguments: (
                            1.0 /
                            arguments[0].parent_ecosystem.biotope.size_y()
                        )
                elif function_settings == 'time':
                    if self.tags_list[0] in ['#organism', '#biotope']:
                        return lambda *arguments: arguments[0].\
                            parent_ecosystem.time
                    elif self.tags_list[0] == '#ecosystem':
                        return lambda *arguments: arguments[0].time
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
                self.error_messenger('syntax error. ', function_settings)
                exit()

    def apply_associative_operator(self, main_operation, inputs):
        """ EXAMPLE:
            {'+': (1, 2, 3, 4, 5)}
            In this case we have to apply several times the operator '+'
        """
        # print "associative", inputs # ***
        return reduce(main_operation, inputs[1:], inputs[0])

    def main_directive(self, expression, error_messenger):
        if is_dict(expression):
            for directive in expression:
                # not all directives can be the main directive. For example
                # 'allowed interval' of 'help' can't be main directives
                if directive in self.all_main_directive_names:
                    return directive
        self.error_messenger('syntax error. Directive not found in',
                             expression)
        return None

    def make_function_from_dict(self, function_settings):
        directive = self.main_directive(function_settings,
                                        self.error_messenger)
        if directive in function_settings:
            inputs = function_settings[directive]
        else:
            self.error_messenger(
                'Main directive not found in', function_settings)
            print 'ALL MAIN DIRECTIVES:'  # ***
            for one_directive in self.all_main_directive_names:
                print one_directive
            exit()

        if directive == 'literal':
            # 'literal' operator returns its input without evaluate it
            return lambda *arguments: inputs

        elif directive == 'cost':
            if is_string(inputs):
                substance_name = 'energy reserve'
                action_name = inputs
            elif is_tuple_or_list(inputs):
                substance_name = inputs[1]
                action_name = inputs[0]
            elif is_dict(inputs):
                substance_name = inputs['substance']
                action_name = inputs['action']
            # print "action_name", action_name, "substance_name",
            # substance_name, "inputs", inputs # ***
            if len(function_settings) == 1:
                return lambda *arguments: arguments[0].parent_ecosystem\
                    .costs[action_name][substance_name](
                        {'#organism': arguments[0]}
                        )
            else:
                tags_dictionary_functions = {}
                for item in function_settings:
                    if item != 'cost':
                        tags_dictionary_functions[item] =\
                            self.make_function(function_settings[item])

                def function_to_return(*arguments):
                    organism = arguments[0]
                    cost = organism.parent_ecosystem.costs[action_name][
                        substance_name]
                    tags_dictionary = {
                        '#organism': organism
                    }
                    for item in tags_dictionary_functions:
                        tags_dictionary[item] = tags_dictionary_functions[
                            item](*arguments)
                    return cost(tags_dictionary)

                return function_to_return

        elif directive == 'constraint':
            return lambda *arguments: arguments[0].parent_ecosystem\
                .constraints[inputs](arguments[0])

        elif directive in self.all_operator_names:
            if directive == 'function':
                if is_tuple_or_list(inputs):
                    inputs_function = self.make_function(inputs[1:])
                    main_operation = self.make_function(inputs[0])
                else:
                    def void_tuple_function(*arguments):
                        return ()
                    inputs_function = void_tuple_function
                    main_operation = self.make_function(inputs)
            else:
                inputs_function = self.make_function(inputs)
                main_operation = self.operators_definitions[
                    directive]['output function']
            if directive in self.associative_operators:
                return lambda *arguments: self.apply_associative_operator(
                    main_operation,
                    inputs_function(*arguments)
                )
            elif directive in self.unary_operators:
                if print_operators:  # ***
                    return lambda *arguments: main_operation(
                        inputs_function(*arguments)) \
                        if self.error_messenger(directive, '') \
                        else main_operation(inputs_function(*arguments))
                else:
                    return lambda *arguments: \
                        main_operation(inputs_function(*arguments))
            else:
                if print_operators:  # ***
                    return lambda *arguments: \
                        main_operation(*(inputs_function(*arguments))) \
                        if self.error_messenger(directive, '') \
                        else main_operation(*(inputs_function(*arguments)))
                else:
                    return lambda *arguments: \
                        main_operation(*(inputs_function(*arguments)))
        else:
            self.error_messenger('syntax error in', function_settings)
            self.error_messenger('Unknown directive', directive)
            exit()

    def constrain_function_to_allowed_interval(
        self,
        function_to_return,
        interval_functions
            ):
        return lambda *arguments: bounded_value(
            function_to_return(*arguments),
            *interval_functions(*arguments)
        )  # if self.error_messenger(interval_functions(*arguments)) else 0

    def set_tags_list(self, tags_list):
        self.tags_list = tags_list

    def make_function(self, function_settings, tags_list=None):
        remove_no_effect_directives(function_settings)
        if tags_list is not None:
            self.tags_list = tags_list
        if print_methods_names:  # ***
            print 'make_function', self.tags_list
            print function_settings

        if is_number(function_settings):
            return lambda *arguments: function_settings

        elif is_function(function_settings):
            return function_settings

        elif is_string(function_settings):
            return self.make_function_from_string(function_settings)

        elif is_tuple_or_list(function_settings):
            terms = [self.make_function(item) for item in function_settings]
            return lambda *arguments: [item(*arguments) for item in terms]

        elif is_dict(function_settings):
            function_to_return = self.make_function_from_dict(
                function_settings)
            if 'allowed interval' in function_settings:
                allowed_interval = self.make_function(
                    function_settings['allowed interval'])
                return self.constrain_function_to_allowed_interval(
                    function_to_return,
                    allowed_interval)
            else:
                return function_to_return

        else:
            self.error_messenger(
                'Warning. Unevaluated function settings:',
                str(function_settings),
                'y tal',
                type(function_settings),
                'y eso'
                )
            return lambda *arguments: function_settings

    def read_function_settings(
        self,
        function_name_with_tags,
        function_settings,
        caller=None
            ):
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

        and this method returns an actual function that takes
        two arguments x and y
        """
        self.tags_list = get_tags_list(function_name_with_tags)
        if caller is not None and caller not in self.tags_list:
            self.tags_list = [caller, ] + self.tags_list
        function_to_return = self.make_function(function_settings)
        self.tags_list = []
        return function_to_return

    def turn_settings_into_functions(self, settings, caller):
        if not is_dict(settings):
            return self.read_function_settings(caller, settings)
        result = {}
        for item in settings:
            # print 'turning', item, 'into function', settings[item] # ***
            if item == 'offer to sell':
                offer_to_sell = {}
                self.tags_list = [caller, ]
                offer_to_sell['amount'] = self.make_function(
                    settings['offer to sell']['amount']
                )
                price = {}
                for substance in settings['offer to sell']['prices']:
                    price[substance] = self.make_function(
                        settings['offer to sell']['prices'][substance]
                    )
                offer_to_sell['prices'] = price
                result['offer to sell'] = offer_to_sell
            elif item not in no_effect_directives:
                function_name = remove_tags(item)
                self.tags_list = [caller, ] + get_tags_list(item)
                # print 'tags_list', self.tags_list # ***
                result[function_name] = self.make_function(settings[item])
        if 'allowed interval' in settings:
            for function_name in result:
                if function_name not in ['allowed interval', 'offer to sell']:
                    result[function_name] = \
                        self.constrain_function_to_allowed_interval(
                            result[function_name],
                            result['allowed interval']
                    )
        self.tags_list = []
        return result

    def make_function_with_tags_dictionary(
        self,
        function_name_with_tags,
        function_settings,
        caller
            ):
        self.caller = caller
        self.tags_list = get_tags_list(function_name_with_tags)
        if caller is not None and caller not in self.tags_list:
            self.tags_list = [caller, ] + self.tags_list
        function_to_evaluate = self.make_function(function_settings)
        tags_list = deepcopy(self.tags_list)
        self.tags_list = []
        self.caller = None

        def function_to_return(tags_dictionary):
            inputs = [tags_dictionary[tag] for tag in tags_list]
            return function_to_evaluate(*inputs)

        return function_to_return
