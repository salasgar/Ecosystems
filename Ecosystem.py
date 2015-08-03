from Basic_tools import *
from Biotope import *
from Settings import *
from Organism import *
from time import *
from SYNTAX import *
from Function_settings_reader import *
from File_writer import *
from copy import *
import logging


DEFAULT_SETTINGS = {}

logger = logging.getLogger('ecosystems')


class Ecosystem(object):

    def __init__(self, ecosystem_settings):
        self.settings = ecosystem_settings
        self.all_gene_names = extract_all_gene_names(self.settings)
        self.function_maker = Function_maker(self, ecosystem_settings)
        self.organisms_list = []
        self.newborns = []
        self.new_deads = []
        self.time = 0
        self.initialize_biotope()
        self.initialize_ecosystem_features()
        self.initialize_costs()
        self.initialize_constraints()
        self.initialize_organisms()
        self.storage_capacities_dictionary = {
            'energy reserve': 'energy storage capacity',
            'water reserve': 'water storage capacity'
            # to do: add more thigs
        }
        self.initialize_statistics()
        self.data_storer = Data_storer(self, Elements_to_store)
        self.number_of_new_deths = 0
        self.number_of_new_births = 0

    def __getitem__(self, code):
        if code == 'biotope':
            return self.biotope
        elif code == 'ecosystem features':
            return self.ecosystem_features
        elif code == 'organisms' or code == 'organisms list':
            return self.organisms_list
        elif code == 'constraints':
            return self.constraints
        elif code == 'costs':
            return self.costs
        elif code == 'time':
            return self.time
        else:
            print 'Unknown element of ecosystem'
            halt()

    def initialize_biotope(self):
        print 'initialize_biotope'
        self.biotope = Biotope(settings=self.settings['biotope'],
                               parent_ecosystem=self)

    def add_feature(self, feature_name, feature_settings):
        self.ecosystem_features[feature_name] = Feature(
            feature_name,
            feature_settings,
            parent_ecosystem=self)

    def initialize_ecosystem_features(self):
        self.ecosystem_features = {}
        if 'ecosystem features' in self.settings:
            for feature in self.settings['ecosystem features']:
                self.add_feature(
                    feature,
                    self.settings['ecosystem features'][feature])

    def initialize_costs(self):
        print 'initialize_costs'
        self.costs = {}
        if 'costs' in self.settings:
            for action_name_with_tags in self.settings['costs']:
                tags_list = get_tags_list(action_name_with_tags)
                action_name = remove_tags(action_name_with_tags)
                self.costs[action_name] = {'tags list': tags_list}
                cost_settings = self.settings['costs'][action_name_with_tags]
                for reserve_substance in cost_settings:
                    self.costs[action_name][reserve_substance] = \
                        self.function_maker.make_function_with_tags_dictionary(
                            action_name_with_tags,
                            cost_settings[reserve_substance],
                            caller='#organism'
                        )

    def initialize_constraints(self):
        print 'initialize_constraints'
        self.constraints = {}
        if 'constraints' in self.settings:
            for constraint_name in self.settings['constraints']:
                self.constraints[constraint_name] = \
                    self.function_maker.read_function_settings(
                        constraint_name,
                        self.settings['constraints'][constraint_name]
                )

    def initialize_statistics(self):
        print 'initialize_statistics'
        self.statistics = {
            'number of natural deths': 0,
            'number of killed by a predator': 0,
            'number of births': 0}
        for category in self.settings['organisms']:
            category_settings = self.settings['organisms'][category]
            self.statistics['number of births of ' + category] = 0
            self.statistics['number of natural deths of ' + category] = 0
            self.statistics[
                'number of ' + category + ' killed by a predator'
            ] = 0
            if 'list of reserve substances' in category_settings['genes']:
                for reserve_substance in category_settings['genes'][
                    'list of reserve substances'
                ]:
                    self.statistics[
                        'total amount of ' + reserve_substance
                    ] = 0
                    self.statistics[
                        'average amount of ' + reserve_substance
                    ] = 0
                    self.statistics[
                        'total amount of ' + reserve_substance
                        + ' in ' + category
                    ] = 0
                    self.statistics[
                        'average amount of ' + reserve_substance
                        + ' in ' + category
                    ] = 0
        for gene in self.all_gene_names:
            self.statistics['average ' + gene] = 0
        for action in self.costs:
            self.statistics['average cost ' + action] = {'total': 0}
            for substance in self.costs[action]:
                self.statistics['average cost ' + action][substance] = 0
        # print "statistics finished" # ***

    def add_organism(self, organism):
        # print 'add organism' # ***
        self.biotope.add_organism(organism)
        self.newborns.append(organism)

    def delete_organism(self, organism):
        # print 'delete organism' # ***
        self.biotope.delete_organism(organism['location'])
        if organism in self.newborns:
            del self.newborns[self.newborns.index(organism)]
        if organism in self.organisms_list:
            del self.organisms_list[self.organisms_list.index(organism)]

    def size_x(self):
        return self.biotope['size'][0]

    def size_y(self):
        return self.biotope['size'][1]

    def initialize_organisms(self):
        print 'initialize_organisms'
        """
        PRE-CONDITIONS:
            This initialization must be called AFTER self.initialize_biotope,
            because we use here Biotope.seek_free_location
        """
        for category_name in self.settings['organisms']:
            category_settings = self.settings['organisms'][category_name]
            number_of_organisms = category_settings[
                'initial number of organisms']
            for _ in range(number_of_organisms):
                new_organism = Organism(parent_ecosystem=self)
                new_organism.configure_with_category_settings(
                    category_settings)
                # This adds new_organism to self.newborns and to self.biotope
                # in a random location:
                self.add_organism(new_organism)
        self.organisms_list += self.newborns
        self.newborns = []

    def create_new_organisms(self, number_of_organisms):
        # Chose the number of new organisms of each category proportionally
        # to the initial number of organisms of each category:
        total = 0
        for category_name in self.settings['organisms']:
            total += self.settings['organisms'][category_name][
                'initial number of organisms']
        for category_name in self.settings['organisms']:
            n = (
                self.settings['organisms'][category_name][
                    'initial number of organisms']
                * number_of_organisms
            ) / total
            for _ in range(n):
                new_organism = Organism(parent_ecosystem=self)
                new_organism.configure_with_category_settings(
                    self.settings['organisms'][category_name]
                )
                # This adds new_organism to self.newborns and to self.biotope
                # in a random location:
                self.add_organism(new_organism)
        self.organisms_list += self.newborns
        self.newborns = []

    def evolve(self):
        # Biotope actions:
        self.biotope.evolve()
        # Ecosystem actions:
        for feature in self.ecosystem_features:
            self.ecosystem_features[feature].update()
        # Organisms actions:
        i = 0
        self.number_of_new_deths = 0
        while i < len(self.organisms_list):
            self.organisms_list[i].evolve()
            i += 1
            for dead_organism in self.new_deads:
                # the organism may be in self.organisms_list or
                # in self.newborns:
                if (
                    dead_organism in self.organisms_list and
                    self.organisms_list.index(dead_organism) < i
                ):
                    i -= 1
                # this erases the organism from the biotope too:
                self.delete_organism(dead_organism)
                # print "number of organisms", len(self.organisms_list) # ***
            self.number_of_new_deths += len(self.new_deads)
            self.new_deads = []
        self.organisms_list += self.newborns
        self.number_of_new_births = len(self.newborns)
        self.newborns = []
        self.time += 1

        # print 'Num of organisms + newborns: %d' % len(self.organisms) # ***

    def count(self, gene, value):
        # Counts how many organisms have that gene with that value
        N = 0
        for organism in self.organisms_list:
            if gene in organism and organism[gene] == value:
                N += 1
        return N

    def count_between(self, gene, value1, value2):
        # Counts how many organisms have that gene with that value
        N = 0
        for organism in self.organisms_list:
            if (
                gene in organism and
                value1 <= organism[gene] and
                organism[gene] <= value2
            ):
                N += 1
        return N

    def population(self):
        return len(self.organisms_list) + len(self.newborns)

    def get_random_organisms(self, number_of_random_organisms):
        return sample(self.organisms_list, number_of_random_organisms)
