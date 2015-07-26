from Basic_tools import *
from Settings import *
from SYNTAX import *
from copy import *

Elements_to_store = {

    """
        In this dictionary we indicate what and how often to store:

            'Once'  means that this data is stored only once at the begining of the file
            200     means that this data is stored once every 200 cycles
            None    means that this data is never stored

    """

    'genes': {
        'nutrient B reserve at birth': None,
        'photosynthesis capacity growth': None,
        'nutrient B storage capacity': None,
        'generation': 200,
        'energy reserve': 100,
        'nutrient A reserve': None,
        'temperature adaptation level': 40,
        'aggressiveness': 20,
        'indicator gene B': 1000,
        'indicator gene A': 1000,
        'moving frequency': None,
        'photosynthesis capacity': None,
        'defense capacity': None,
        'minimum energy reserve for procreating': None,
        'speed': None,
        'minimum nutrient B reserve for procreating': None,
        'species': None,
        'actions sequence': None,
        'nutrient B reserve': None,
        'energy reserve at birth': None,
        'hunt radius': None,
        'optimal temperature': None,
        'nutrient A reserve at birth': None,
        'energy storage capacity': None,
        'attack capacity': None,
        'mean aggressiveness': None,
        'procreation frequency': None,
        'species identity mutation frequency': None,
        'basal defense capacity': None,
        'age': 20,
        'minimum nutrient A reserve for procreating': None,
        'nutrient A storage capacity': None,
        'radius of procreation': None,
        'mutation frequency': None
        }
    },
    'biotope': {
        'biotope features': {
            'nutrient B': 'Once',
            'nutrient A': 'Once',
            'sunlight': 'Once',
            'temperature': 'Once',
            'seasons speed': 'Once'
            },
        'size': 'Once'
        },
    'ecosystem features': {
        'maximum population allowed': 100,
        'time': 20,
        'autotrophs productivity': 'Once',
        'population': 20
        }
    }

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
            current_data['biotope']['size'] = deep_copy(self.parent_ecosystem.biotope.size)
        for feature in self.elements_to_store['biotope']['biotope features']:
            if check('biotope', 'biotope features', feature):
                current_data['biotope']['biotope features'][feature] = deep_copy(self.parent_ecosystem.biotope.biotope_features[feature].current_value)
        for feature in self.elements_to_store['ecosystem features']:
            if check('ecosystem features', feature):
                current_data['ecosystem features'][feature] = deep_copy(self.parent_ecosystem.ecosystem_features[feature].current_value)
        for organism in self.parent_ecosystem.organisms_list:
            data = {}
            for gene in self.elements_to_store['genes']:
                if check('genes', gene):
                    data[gene] = deep_copy(organism[gene])
            current_data['organisms list'].append(data)

        self.data.append(current_data)

        return current_data




















