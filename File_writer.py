from Basic_tools import *
from Settings import *
from SYNTAX import *
from copy import *


def get_skeleton_of_settings(settings, final_element):
    if is_dict(settings):
        result = {}
        for item in settings:
            if item in (
                All_operators +
                Auxiliar_commands +
                Commands_that_comunicate_an_organism_with_the_environment +
                [
                    'literal', 
                    'infinity',
                    'initial value', 
                    'initial value #x #y',
                    'value after updating',
                    'value after updating #x #y',
                    'update once every',
                    'value in next cycle',
                    'value after mutation',
                    'allowed interval',
                    'type of inputs',
                    'type of outputs',
                    'output function',
                    'check number of inputs',
                    'check inputs',
                    'matrix size'
                ]):
                return final_element
            elif not item in No_effect_commands:
                result[item] = get_skeleton_of_settings(settings[item], final_element)
        return result
    else:
        return final_element

"""
    When we change the settings of the ecosystem, we can execute this line to write the dictionary of
    elements_to_store:

    print_dictionary(get_skeleton_of_settings(my_example_of_ecosystem_settings, 'Once'), 'Elements_to_store')

"""

def store(element, file):
    """
        This method stores the element in the file
    """
    pass

class Data_storer:
    def __init__(self, parent_ecosystem, elements_to_store):
        self.parent_ecosystem = parent_ecosystem
        self.elements_to_store = elements_to_store
        self.data = []

    def store_data(self):
        def check(*kew_words):
            code = self.elements_to_store
            for kew_word in kew_words:
                code = code[kew_word]
            return (
                (code == 'Once' and self.parent_ecosystem.time == 0) or
                (is_number(code) and round(self.parent_ecosystem.time / code) == self.parent_ecosystem.time / code)
                )
        current_data = {
            'biotope': {
                'biotope features': {}
            },
            'ecosystem features': {},
            'organisms list': [],
        }
        if check('biotope', 'size'):
            current_data['biotope']['size'] = deepcopy(self.parent_ecosystem.biotope.size)
        for feature in self.elements_to_store['biotope']['biotope features']:
            if check('biotope', 'biotope features', feature):
                current_data['biotope']['biotope features'][feature] = deepcopy(self.parent_ecosystem.biotope.biotope_features[feature].current_value)
        for feature in self.elements_to_store['ecosystem features']:
            if check('ecosystem features', feature):
                current_data['ecosystem features'][feature] = deepcopy(self.parent_ecosystem.ecosystem_features[feature].current_value)
        for organism in self.parent_ecosystem.organisms_list:
            data = {}
            for gene in self.elements_to_store['genes']:
                if check('genes', gene):
                    data[gene] = deepcopy(organism[gene])
            current_data['organisms list'].append(data)

        self.data.append(current_data)

        return current_data




















