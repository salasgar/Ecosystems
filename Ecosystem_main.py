from GUI import GUI
from Tools import *
from Biotope import Biotope
from Ecosystem_settings import ecosystem_settings
from Organism import *
from time import *

# from time import sleep  # To remove
# import Biotope
# import Organism

things_to_see = {
    "https://www.coursera.org/course/ml",
    ""
}

DEFAULT_SETTINGS = {}

def extract_genes_and_status_names(category_settings):
    def extract(settings):
        result_list = []
        for item in settings:
            if isinstance(item, str):
                result_list.append(item)
            elif hasattr(item, '__iter__'):
                for sub_item in item:
                    if isinstance(sub_item, str):
                        result_list.append(sub_item)
        return result_list        
    final_list = []
    for x in ('genes', 'status', 'mutabilities', 'initial values'):
        if x in category_settings:
            final_list += extract(category_settings[x])
    return final_list
                    
                    
            
    return result_list
    
class Ecosystem(object):
    """ Attributes:
    self.biotope
    self.organisms_list
    self.newborns    
    self.outlays
    self.constraints
    """

    def __init__(self, ecosystem_settings, default_settings = DEFAULT_SETTINGS):
        self.load_settings(ecosystem_settings, default_settings)
        self.initialize_biotope()
        self.initialize_outlays()
        self.initialize_constraints()
        self.initialize_organisms()
        self.storage_capacities_dictionary = {
            'energy reserve': 'energy storage capacity',
            'water reserve': 'water storage capacity'
            # to do: add more thigs
            }
        self.new_deads = []
        self.initialize_statistics()
        
    def load_settings(self, ecosystem_settings, default_settings):
        print 'load_settings'
        if 'ecosystem' in default_settings:            
            merge_dictionaries(
                dictionary_to_be_completed = ecosystem_settings,
                dictionary_to_complete_with = default_settings['ecosystem'])
        if isinstance(ecosystem_settings['organisms'], dict):
            ecosystem_settings['organisms'] = [ecosystem_settings['organisms']]
        for category in ecosystem_settings['organisms']:
            if not 'genes' in category:
                category['genes'] = {}
            if not 'status' in category:
                category['status'] = {}
            if ('seeking prey' in default_settings) and (('attack capacity' in category) or ('strength' in category)):
                merge_dictionaries(
                    dictionary_to_be_completed = category,
                    dictionary_to_complete_with = default_settings['seeking prey'])
            if not 'list of reserve substances' in category['genes']:
                if 'energy reserve' in category['status']:
                    category['genes']['list of reserve substances'] = ['energy reserve']
            if not 'actions list' in category['genes']:
                category['genes']['actions list'] = []
                actions_list = category['genes']['actions list']
                organisms_attributes_list = category['genes'].keys() + category['status'].keys()
                if 'photosynthesis capacity' in organisms_attributes_list:
                    actions_list.append('do photosynthesis')
                if 'speed' in organisms_attributes_list:
                    actions_list.append('move')                 
                if ('attack capacity' in organisms_attributes_list) or ('hunt radius' in organisms_attributes_list):
                    actions_list.append('hunt')                   
                if 'list of reserve substances' in organisms_attributes_list:
                    actions_list.append('interchange substances with the biotope')
                    actions_list.append('interchange substances with other organisms')                    
                if 'sex' in organisms_attributes_list:
                    actions_list.append('fertilize other organisms')                 
                if 1 + 1 == 2:
                    actions_list.append('procreate')
                    actions_list.append('stay alive')   
                if 'age' in organisms_attributes_list:
                    actions_list.append('age')
                category['genes']['actions list'] = actions_list
            if 'hunt' in category['genes']['actions list'] and not 'hunt radius' in (category['genes'].keys() + category['status'].keys()):
                category['genes']['hunt radius'] = 1.5
        self.settings = ecosystem_settings  
        #print_dictionary( self.settings     )         
        
    def initialize_biotope(self):
        print 'initialize_biotope'
        self.biotope = Biotope(settings = self.settings['biotope'], parent_ecosystem = self)
                
    def initialize_outlays(self):
        print 'initialize_outlays'
        self.outlays = {}
        for action in self.settings['outlays']:
            self.outlays[action] = {}
            for reserve_substance in self.settings['outlays'][action]:
                self.outlays[action][reserve_substance] = make_function(self.settings['outlays'][action][reserve_substance], number_of_organisms = 1)
    
    def initialize_constraints(self):
        print 'initialize_constraints'
        self.constraints = {}
        for action in self.settings['constraints']:
            if action == 'kill?':
                self.constraints[action] = make_function(self.settings['constraints'][action], number_of_organisms = 2)        
            else:
                self.constraints[action] = make_function(self.settings['constraints'][action], number_of_organisms = 1)        
    
    def initialize_statistics(self):
        print 'initialize_statistics'
        self.statistics = {
            'number of natural deths': 0,
            'number of killed by a predator': 0,
            'number of births': 0}
        for category in self.settings['organisms']:
            if 'category' in category:
                self.statistics['number of births of ' + category['category']] = 0
                self.statistics['number of natural deths of ' + category['category']] = 0
                self.statistics['number of ' + category['category'] + ' killed by a predator'] = 0
            if 'list of reserve substances' in category['genes']:
                for reserve_substance in category['genes']['list of reserve substances']:
                    self.statistics['total amount of ' + reserve_substance] = 0
                    self.statistics['average amount of ' + reserve_substance] = 0
                    self.statistics['total amount of ' + reserve_substance + ' in ' + category['category']] = 0
                    self.statistics['average amount of ' + reserve_substance + ' in ' + category['category']] = 0             
            for gene_or_status in (category['genes'].keys() + category['status'].keys()):
                self.statistics['average ' + gene_or_status] = 0
                
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
        self.newborns = []
        organisms_settings = self.settings['organisms']
        for organisms_category in organisms_settings:
            all_genes_and_status = extract_genes_and_status_names(organisms_category)               
            genes_settings = organisms_category['genes'] if 'genes' in organisms_category else {}
            status_settings = organisms_category['status'] if 'status' in organisms_category else {}
            for _ in range(organisms_category['number of organisms']):
                # Note: By the moment, location has random distribution
                new_organism = Organism(self, {'mutating genes': {}, 'modifying status': {}, 'list of reserve substances': []})
                
                # READING GENES:
                for genes_list in genes_settings:
                    current_genes_settings = genes_settings[genes_list]
                    if not hasattr(genes_list, '__iter__'):
                        genes_list = [genes_list]
                    for gene in genes_list:
                        new_organism.add_gene(gene, current_genes_settings, all_genes_and_status)
                                       
                # READING STATUS:
                for status_list in status_settings:
                    current_status_settings = status_settings[status_list]
                    if not hasattr(status_list, '__iter__'):
                        status_list = [status_list]
                    for status in status_list:
                        new_organism.add_status(status, current_status_settings, all_status_and_status)
                
                # READING MUTABILITIES:
                mutabilities_settings = organisms_category['mutabilities'] if 'mutabilities' in organisms_category else {}
                for genes_list in mutabilities_settings:
                    mutability = mutabilities_settings[genes_list]
                    if not hasattr(genes_list, '__iter__'):
                        genes_list = [genes_list]
                    for gene in genes_list:
                        new_organism['mutating genes'][gene] = make_mutability(gene, mutability)
                
                # READING MODIFYING STATUS:
                modifying_status_settings = organisms_category['modifying'] if 'modifying' in organisms_category else {}
                for status_list in modifying_status_settings:
                    modifying = modifying_status_settings[status_list]
                    if not hasattr(status_list, '__iter__'):
                        status_list = [status_list]
                    for status in status_list:
                        new_organism['modifying status'][status] = make_modifying_status(status, modifying)
                
                # READING INITIAL VALUES:
                initial_values_settings = organisms_category['initial values'] if 'initial values' in organisms_category else []
                for attributes_list in initial_values_settings:
                    settings = initial_values_settings[attributes_list]
                    if not hasattr(attributes_list, '__iter__'):
                        attributes_list = [attributes_list]
                    initial_value_generator = make_function(settings, number_of_organisms = 1)
                    for attribute in attributes_list:
                        new_organism[attribute] = initial_value_generator(new_organism)
                                
                # CONFIGURING new_organism:                
                if 'energy reserve' in new_organism and not 'energy reserve' in new_organism['list of reserve substances']:
                    new_organism['list of reserve substances'].append('energy reserve')
                if 'color' in new_organism:
                    if hasattr(new_organism['color'], '__getitem__'):
                        red = make_function(new_organism['color'][0], number_of_organisms = 1)
                        green = make_function(new_organism['color'][1], number_of_organisms = 1)
                        blue = make_function(new_organism['color'][2], number_of_organisms = 1)
                        new_organism['color'] = lambda organism: (int(red(organism)), int(green(organism)), int(blue(organism)))
                self.add_organism(new_organism)
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
        
        # print 'Num of organisms + newborns: %d' % len(self.organisms)

    def count(self, item, value):
        N = 0
        for organism in self.organisms_list:
            if item in organism and organism[item] == value:
                N += 1
        return N

def main():
    print " *"*30, "\nWe start NOW!"
    # create Ecosystem
    ecosystem = Ecosystem(ecosystem_settings)
    
    """ test:
    i = 0
    while ecosystem.organisms_list[i]['weapon'] != 'stone':
        i += 1
    predator = ecosystem.organisms_list[i]

    while ecosystem.organisms_list[i]['weapon'] != 'scissors':
        i += 1
    prey = ecosystem.organisms_list[i]

    print ecosystem.constraints['kill?'](predator, prey)
    
    organism = ecosystem.organisms_list[0]
    for i in range(100):
        print ecosystem.constraints['die?'](organism),
    return 0
    """
    
    return 0
    enable_graphics = False
    time_lapse = 4
    make_pauses = False #not enable_graphics
    make_sleeps = False
    Total_time = 200
    
    print_ages = False
    print_organisms = False
    
    if enable_graphics:
        gui = GUI(ecosystem)
    # Loop
    time = 0
    user_input = 'N'
    while (len(ecosystem.organisms_list) > 0) and (time < Total_time) and (user_input != 'Y') and (user_input != 'y'):
        if time % time_lapse == 0:
            print ("time =", time, "Num of organisms =",
                   len(ecosystem.organisms_list))
            if print_ages:
                print [organism['age'] for organism in ecosystem.organisms_list]
            if print_organisms:
                for organism in ecosystem.organisms_list:  
                    print organism['category'], round(organism['energy reserve'], 2), organism['color'](organism)
                    #print organism.__str__(list_of_attributes = ('category', 'energy reserve', 'color'))
                    #if organism['age'] > 100:
                    #    print ecosystem.constraints['die?'](organism)
            #print ecosystem.count('category', 'plant'), 'plants and', ecosystem.count('category', 'animal'), 'animals'
            if make_pauses:
                user_input = raw_input('exit? [Y/N]: ')                    
        # TODO: Define correct condition
        if (user_input != 'y') and (user_input != 'Y'):
            ecosystem.evolve()
        if enable_graphics:
            gui.handle_events()
            gui.draw_ecosystem()
        if make_sleeps:
            sleep(1.0)  # To remove
        time += 1
    if enable_graphics:
        gui.delete()
                    
if __name__ == '__main__':
    main()
