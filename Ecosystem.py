from GUI import GUI
from Basic_tools import *
from Biotope import Biotope
from Settings import *
from Organism import *
from time import *
from SYNTAX import *
from Function_settings_reader import *
from copy import deep_copy
import logging


DEFAULT_SETTINGS = {}

logger = logging.getLogger('ecosystems')

class Ecosystem(object):

    def __init__(self, ecosystem_settings):
        self.function_maker = Function_maker(ecosystem_settings)
        self.load_settings(ecosystem_settings)
        self.time = 0
        self.initialize_biotope()
        self.initialize_ecosystem_features()
        self.initialize_costs()
        self.initialize_constraints()
        self.newborns = []
        self.new_deads = []
        self.initialize_organisms()
        self.storage_capacities_dictionary = {
            'energy reserve': 'energy storage capacity',
            'water reserve': 'water storage capacity'
            # to do: add more thigs
            }
        self.initialize_statistics()
        
    def load_settings(self, ecosystem_settings):
        self.settings = ecosystem_settings  
        #print_dictionary(self.settings)   
        self.all_gene_names = extract_all_gene_names(self.settings)
        self.all_feature_names = extract_all_feature_names(self.settings)    
        if not check_settings_syntax(ecosystem_settings, ecosystem_settings_syntax, self.all_gene_names, self.all_feature_names):
            error_maker = 1/0  

    def initialize_biotope(self):
        print 'initialize_biotope'
        self.biotope = Biotope(settings = self.settings['biotope'],
                               parent_ecosystem = self)
                
    def add_feature(self, feature_name, feature_settings):
        self.ecosystem_features[feature_name] = Feature(feature_settings, self)

    def initialize_ecosystem_features(self):
        if 'ecosystem features' in self.settings:
            for feature in self.settings['ecosystem features']:
                self.add_feature(feature, self.settings['biotope features'][feature])

    def initialize_costs(self):
        print 'initialize_costs'
        self.costs = {}
        if 'costs' in self.settings:
            for action_name in self.settings['costs']:
                self.costs[action_name] = {}
                for reserve_substance in self.settings['costs'][action_name]:
                    self.costs[action_name][reserve_substance] = \
                        self.function_maker.read_function_settings(
                            action_name
                            self.settings['costs'][action_name][reserve_substance]
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
            self.statistics['number of ' + category + ' killed by a predator'] = 0
            if 'list of reserve substances' in category_settings['genes']:
                for reserve_substance in category_settings['genes']['list of reserve substances']:
                    self.statistics['total amount of ' + reserve_substance] = 0
                    self.statistics['average amount of ' + reserve_substance] = 0
                    self.statistics['total amount of ' + reserve_substance + ' in ' + category] = 0
                    self.statistics['average amount of ' + reserve_substance + ' in ' + category] = 0             
        for gene in self.all_gene_names:
            self.statistics['average ' + gene] = 0
        print "statistics finished"
        
    def add_organism(self, organism):
        #print 'add organism'
        self.biotope.add_organism(organism)
        self.newborns.append(organism)  
        
    def delete_organism(self, organism):
        #print 'delete organism'
        self.biotope.delete_organism(organism['location'])
        if organism in self.newborns:
            del self.newborns[self.newborns.index(organism)]
        if organism in self.organisms_list:
            del self.organisms_list[self.organisms_list.index(organism)]
            # warning: list.index() can be very slow. We should use a double chain list            
        
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
        for category_name in self.settings['organisms']:  # in Ecosystem.load_settings we make sure that self.settings['organisms'] is a list of (one or more) categories
            category_settings = self.settings['organisms'][category_name]
            number_of_organisms = category_settings['initial number of organisms']
            genes_settings = category_settings['genes']
            for _ in range(number_of_organisms):                
                new_organism = Organism(
                    self, {
                        'value after mutation': {}, 
                        'value in next cycle': {}, 
                        'list of reserve substances': []
                    })
                # Load genes:
                for gene_name in genes_settings:
                    new_organism.add_gene(gene_name, genes_settings[gene_name])
                # Load decisions:
                if 'decisions' in category_settings:
                    for decision in category_settings['decisions']:
                        new_organism.add_decision(decision, category_settings['decisions'][decision])
                self.add_organism(new_organism) # This adds new_organism to self.newborns and to self.biotope in a random location
        self.organisms_list = self.newborns
        self.newborns = []

    def evolve(self):
        #print 'evolve'
        # Biotope actions:
        self.biotope.evolve()
        # Organisms actions:
        i = 0        
        while i < len(self.organisms_list):
            self.organisms_list[i].act()
            i += 1
            for dead_organism in self.new_deads:
                # the organism may be in self.organisms_list or in self.newborns:
                if dead_organism in self.organisms_list and self.organisms_list.index(dead_organism) < i:
                    i -= 1
                self.delete_organism(dead_organism) # this erases the organism from the biotope too
                #print "number of organisms", len(self.organisms_list)
            self.new_deads = []
        self.organisms_list += self.newborns
        self.newborns = []
        for feature in self.ecosystem_features:
            feature.update()        
        self.time += 1
        
        # print 'Num of organisms + newborns: %d' % len(self.organisms)

    def count(self, gene, value): # Counts how many organisms have that gene with that value
        N = 0
        for organism in self.organisms_list:
            if gene in organism and organism[gene] == value:
                N += 1
        return N

    def count(self, gene, value1, value2): # Counts how many organisms have that gene with that value
        N = 0
        for organism in self.organisms_list:
            if gene in organism and value1 <= organism[gene] and organism[gene] <= value:
                N += 1
        return N

    def get_random_organisms(self, number_of_random_organisms):
        return sample(self.organisms_list, number_of_random_organisms)






