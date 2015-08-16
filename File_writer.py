from Basic_tools import *
from SYNTAX import *
from copy import *
import yaml
import os

def get_skeleton_of_settings(settings, final_element):
    if is_dict(settings):
        result = {}
        for item in settings:
            if item in (
                All_operators +
                Auxiliar_directives +
                Directives_that_comunicate_an_organism_with_the_environment +
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
                ]
            ):
                return final_element
            elif item not in No_effect_directives:
                result[item] = get_skeleton_of_settings(
                    settings[item],
                    final_element)
        return result
    else:
        return final_element

"""
    When we change the settings of the ecosystem, we can
    execute this line to write the dictionary of
    elements_to_store:

    print_dictionary(get_skeleton_of_settings(
            my_example_of_ecosystem_settings,
            'Once'),
        'Elements_to_store')
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

    def store_data(self, history_path):

        # print "Storing data..."

        def check(*kew_words):
            # This checks if it's time to store the
            # element referenced with kew_words
            code = self.elements_to_store
            for kew_word in kew_words:
                if is_dict(code) and kew_word in code:
                    code = code[kew_word]
                else:
                    return False
            return (
                (
                    code == 'Once' and self.parent_ecosystem.time == 0
                ) or
                (
                    is_number(code) and
                    (self.parent_ecosystem.time % code == 0)
                )
            )
        data_is_empty = True
        current_data = {
            'biotope': {
                'biotope features': {}
            },
            'ecosystem features': {},
            'organisms list': [],
        }
        if check('biotope', 'size'):
            data_is_empty = False
            current_data['biotope']['size'] = deepcopy(
                self.parent_ecosystem.biotope['size'])
        if (
            'biotope' in self.elements_to_store and
            'biotope features' in self.elements_to_store['biotope']
        ):
            for feature in (
                self.elements_to_store['biotope']['biotope features']
            ):
                if check('biotope', 'biotope features', feature):
                    data_is_empty = False
                    current_data['biotope']['biotope features'][
                        feature] = deepcopy(
                            self.parent_ecosystem.biotope.biotope_features[
                                feature].current_value
                    )
        if 'ecosystem features' in self.elements_to_store:
            for feature in self.elements_to_store['ecosystem features']:
                if check('ecosystem features', feature):
                    data_is_empty = False
                    current_data['ecosystem features'][feature] = deepcopy(
                        self.parent_ecosystem.ecosystem_features[
                            feature].current_value
                    )
        for organism in self.parent_ecosystem.organisms_list:
            data = {}
            organisms_list_is_empty = True
            if 'genes' in self.elements_to_store:
                for gene in self.elements_to_store['genes']:
                    if check('genes', gene):
                        data_is_empty = False
                        organisms_list_is_empty = False
                        data[gene] = deepcopy(organism[gene])
            if not organisms_list_is_empty:
                current_data['organisms list'].append(data)

        if not data_is_empty:
            if not os.path.exists(history_path):
                os.mkdir(history_path)
            if not os.path.exists(os.path.join(history_path,
                                               self.parent_ecosystem.name)):
                os.mkdir(os.path.join(history_path,
                                      self.parent_ecosystem.name))
            data_file = os.path.join(
                history_path,
                self.parent_ecosystem.name,
                'cycle_' + str(self.parent_ecosystem.time) + '.yaml')
            with open(data_file, 'w') as f:
                f.write(yaml.dump(current_data))
