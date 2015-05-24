from GUI import GUI
from Tools import *
from Biotope import Biotope
from Ecosystem_settings import DEFAULT_SETTINGS, ecosystem_settings
from Organism import Organism
from time import *

# from time import sleep  # To remove
# import Biotope
# import Organism

things_to_see = {
    "https://www.coursera.org/course/ml",
    ""
}


def make_mutability(mutability_settings, gene):    
    if 'new value' in mutability_settings:
        calculate_new_value = make_function(mutability_settings['new value'], number_of_arguments = 1)
    elif 'absolute variation' in mutability_settings:
        absolute_variation = make_function(mutability_settings['absolute variation'], number_of_arguments = 1)
        if 'percentage variation' in mutability_settings:
            percentage_variation = make_function(mutability_settings['percentage variation'], number_of_arguments = 1)
            calculate_new_value = lambda organism: organism[gene] * (1 + percentage_variation(organism)) + absolute_variation(organism)
        else:
            calculate_new_value = lambda organism: organism[gene] + absolute_variation(organism)
    elif 'percentage variation' in mutability_settings:
        percentage_variation = make_function(mutability_settings['percentage variation'], number_of_arguments = 1)
        calculate_new_value = lambda organism: organism[gene] * (1 + percentage_variation(organism))
    else:
        calculate_new_value = lambda organism: organism[gene] # (no mutation) 
    if 'mutation frequency' in mutability_settings:
        mutation_frequency = make_function(mutability_settings['mutation frequency'], number_of_arguments = 1)
    else:
        mutation_frequency = lambda organism: 1
    will_mutate = lambda organism: (random() < mutation_frequency(organism))
    if 'allowed interval' in mutability_settings:
        interval = mutability_settings['allowed interval']
        if  (interval[0] in {'- infinity', '-infinity'}) and (interval[1] in {'+ infinity', '+infinity', 'infinity'}): # this means no constraints
            new_value = calculate_new_value
        elif interval[0] in {'- infinity', '-infinity'}:
            upper_constraint_function = lambda value, default_value, constraint: value if value < constraint else default_value
            new_value = lambda organism: upper_constraint_function(calculate_new_value(organism), organism[gene], interval[1])
        elif interval[1] in {'+ infinity', '+infinity', 'infinity'}:
            lower_constraint_function = lambda value, default_value, constraint: value if value > constraint else default_value
            new_value = lambda organism: lower_constraint_function(calculate_new_value(organism), organism[gene], interval[0])
        else:
            lower_and_upper_constraint_function = lambda value, default_value, lower_constraint, upper_constraint: value if (value > lower_constraint) and (value <= upper_constraint) else default_value
            new_value = lambda organism: lower_and_upper_constraint_function(calculate_new_value(organism), organism[gene], *interval)         
    else:
        new_value = calculate_new_value
    return {'will mutate?': will_mutate, 'new value': new_value}
        
def make_modifying_status(modifying_settings, status):    
    if 'new value' in modifying_settings:
        calculate_new_value = make_function(modifying_settings['new value'], number_of_arguments = 1)
    elif 'absolute variation' in modifying_settings:
        absolute_variation = make_function(modifying_settings['absolute variation'], number_of_arguments = 1)
        if 'percentage variation' in modifying_settings:
            percentage_variation = make_function(modifying_settings['percentage variation'], number_of_arguments = 1)
            calculate_new_value = lambda organism: organism[status] * (1 + percentage_variation(organism)) + absolute_variation(organism)
        else:
            calculate_new_value = lambda organism: organism[status] + absolute_variation(organism)
    elif 'percentage variation' in modifying_settings:
        percentage_variation = make_function(modifying_settings['percentage variation'], number_of_arguments = 1)
        calculate_new_value = lambda organism: organism[status] * (1 + percentage_variation(organism))
    else:
        calculate_new_value = lambda organism: organism[status] # (no change) 
    if 'changing frequency' in modifying_settings:
        changing_frequency = make_function(modifying_settings['changing frequency'], number_of_arguments = 1)
    else:
        changing_frequency = lambda organism: 1
    will_change = lambda organism: (random() < changing_frequency(organism))
    if 'allowed interval' in modifying_settings:
        interval = modifying_settings['allowed interval']
        if  (interval[0] in {'- infinity', '-infinity'}) and (interval[1] in {'+ infinity', '+infinity', 'infinity'}): # this means no constraints
            new_value = calculate_new_value
        elif interval[0] in {'- infinity', '-infinity'}:
            upper_constraint_function = lambda value, default_value, constraint: value if value < constraint else default_value
            new_value = lambda organism: upper_constraint_function(calculate_new_value(organism), organism[status], interval[1])
        elif interval[1] in {'+ infinity', '+infinity', 'infinity'}:
            lower_constraint_function = lambda value, default_value, constraint: value if value > constraint else default_value
            new_value = lambda organism: lower_constraint_function(calculate_new_value(organism), organism[status], interval[0])
        else:
            lower_and_upper_constraint_function = lambda value, default_value, lower_constraint, upper_constraint: value if (value > lower_constraint) and (value <= upper_constraint) else default_value
            new_value = lambda organism: lower_and_upper_constraint_function(calculate_new_value(organism), organism[status], *interval)         
    else:
        new_value = calculate_new_value
    return {'will change?': will_change, 'new value': new_value}
        
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
        merge_dictionaries(
            dictionary_to_be_completed = ecosystem_settings,
            dictionary_to_complete_with = default_settings['ecosystem'])
        if isinstance(ecosystem_settings['organisms'], dict):
            ecosystem_settings['organisms'] = [ecosystem_settings['organisms']]
        for category in ecosystem_settings['organisms']:
            if ('attack capacity' in category) or ('strength' in category):
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
                if 'attack capacity' in organisms_attributes_list:
                    actions_list.append('hunt')                   
                if 'list of reserve substances' in organisms_attributes_list:
                    actions_list.append('interchange substances with the biotope')
                    actions_list.append('interchange substances with other organisms')                    
                if 'sex' in organisms_attributes_list:
                    actions_list.append('fertilize other organisms')                 
                if 1 + 1 == 2:
                    actions_list.append('procreate if possible')
                    actions_list.append('stay alive')   
                if 'age' in organisms_attributes_list:
                    actions_list.append('age')  
        self.settings = ecosystem_settings  
        #print_dictionary( self.settings     )         
        
    def initialize_biotope(self):
        self.biotope = Biotope(settings = self.settings['biotope'], parent_ecosystem = self)
                
    def initialize_outlays(self):
        self.outlays = {}
        for action in self.settings['outlays']:
            self.outlays[action] = {}
            for reserve_substance in self.settings['outlays'][action]:
                self.outlays[action][reserve_substance] = make_function(self.settings['outlays'][action][reserve_substance], number_of_arguments = 1)
    
    def initialize_constraints(self):
        self.constraints = {}
        for action in self.settings['constraints']:
            if action == 'hunting':
                self.constraints[action] = make_function(self.settings['constraints'][action], number_of_arguments = 2)        
            else:
                self.constraints[action] = make_function(self.settings['constraints'][action], number_of_arguments = 1)        
    
    def initialize_statistics(self):
        self.statistics = {
            'number of natural deths': 0,
            'number of killed by a predator': 0,
            'number of births': 0}
        for category in self.settings['organisms']:
            self.statistics['number of births of ' + category['category']] = 0
            self.statistics['number of natural deths of ' + category['category']] = 0
            self.statistics['number of ' + category['category'] + ' killed by a predator'] = 0
            for reserve_substance in category['genes']['list of reserve substances']:
                self.statistics['total amount of ' + reserve_substance] = 0
                self.statistics['average amount of ' + reserve_substance] = 0
                self.statistics['total amount of ' + reserve_substance + ' in ' + category['category']] = 0
                self.statistics['average amount of ' + reserve_substance + ' in ' + category['category']] = 0             

    def add_organism(self, organism):
        self.biotope.add_organism(organism)
        self.newborns.append(organism)  
        
    def delete_organism(self, organism):
        self.biotope.delete_organism(organism['location'])
        if organism in self.newborns:
            self.newborns.delete(organism) 
        if organism in self.organisms_list:
            del self.organisms_list[self.organisms_list.index(organism)]
            # warning: list.index() can be very slow. We should use a double chain list            
        
    def size_x(self):
        return self.biotope['size'][0]

    def size_y(self):
        return self.biotope['size'][1]

    
    def initialize_organisms(self):
        """ 
        PRE-CONDITIONS:
            This initialization must be called AFTER self.initialize_biotope, 
            because we use here Biotope.seek_free_location
        """
        self.newborns = []
        organisms_settings = self.settings['organisms']
        for organisms_category in organisms_settings:
            for _ in range(organisms_category['number of organisms']):
                # Note: By the moment, location has random distribution
                organism = Organism(self, {'mutating genes': {}, 'modifying status': {}, 'list of reserve substances': []})
                genes_settings = organisms_category['genes']
                for gene in genes_settings.keys():
                    if isinstance(genes_settings[gene], dict):
                        if 'initial value' in genes_settings[gene]:
                            initial_value_generator = make_function(genes_settings[gene]['initial value'], number_of_arguments = 1)
                            organism[gene] = initial_value_generator(organism)
                        else: # the gene is a function:
                            organism[gene] = make_function(genes_settings[gene], number_of_arguments = 1)         
                        if 'mutability' in genes_settings[gene]:
                            organism['mutating genes'][gene] = make_mutability(genes_settings[gene]['mutability'], gene)       
                    else:
                        if isinstance(genes_settings[gene], str) and genes_settings[gene] in genes_settings:
                            organism[gene] = make_function(genes_settings[gene], number_of_arguments = 1)
                        else:
                            organism[gene] = genes_settings[gene]
                status_settings = organisms_category['status']
                for status in status_settings:
                    if isinstance(status_settings[status], dict):
                        if 'initial value' in status_settings[status]:
                            initial_value_generator = make_function(status_settings[status]['initial value'], number_of_arguments = 1)
                            organism[status] = initial_value_generator(organism)
                        else:
                            organism[status] = make_function(status_settings[status], number_of_arguments = 1)
                        if 'modifying' in status_settings[status]:
                            organism['modifying status'][status] = make_modifying_status(status_settings[status]['modifying'], status)       
                    else:
                        organism[status] = status_settings[status]                
                if 'energy reserve' in organism and not 'energy reserve' in organism['list of reserve substances']:
                    organism['list of reserve substances'].append('energy reserve')
                self.add_organism(organism)
        self.organisms_list = self.newborns
        self.newborns = []

    def evolve(self):
        # Biotope actions:
        self.biotope.evolve()
        # Organisms actions:
        i = 0        
        while i < len(self.organisms_list):
            self.organisms_list[i].act()
            i += 1
            for dead_organism in self.new_deads:
                if self.organisms_list.index(dead_organism) < i:
                    #print 'dying', dead_organism.__str__(list_of_attributes = ('category', 'energy reserve'))
                    i -= 1
                self.delete_organism(dead_organism) # this erases the organism from the biotope too
                print "number of organisms", len(self.organisms_list)
            self.new_deads = []
        self.organisms_list += self.newborns
        self.newborns = []
        
        # print 'Num of organisms + newborns: %d' % len(self.organisms)


def main():
    print " *"*50, "\nWe start NOW!"
    # create Ecosystem
    ecosystem = Ecosystem(ecosystem_settings)
    # Add initial organisms to the ecosystem:

    enable_graphics = False
    time_lapse = 1
    Total_time = 200
    
    if enable_graphics:
        gui = GUI(ecosystem)
    # Loop
    time = 0
    while (len(ecosystem.organisms_list) > 0) and (time < Total_time):
        if time % time_lapse == 0:
            print ("time =", time, "Num of organisms =",
                   len(ecosystem.organisms_list))
            print [organism['age'] for organism in ecosystem.organisms_list]
            for organism in ecosystem.organisms_list:            
                print organism.__str__(list_of_attributes = ('age', 'category', 'energy reserve'))
                #if organism['age'] > 100:
                #    print ecosystem.constraints['dying'](organism)
                    
        # TODO: Define correct condition
        ecosystem.evolve()
        if enable_graphics:
            gui.handle_events()
            gui.draw_ecosystem()
        #sleep(0.5)  # To remove
        time += 1
    if enable_graphics:
        gui.delete()
        
    a = range(20)
    
    for i in a:
        print i, a
        if i < 10:
            del a[a.index(i)]
    
    print ecosystem.constraints['dying']({'energy reserve': 11, 'age': 100, 'longevity': 30})
    print ecosystem.constraints['dying']({'energy reserve': 10, 'age': 100, 'longevity': 30})
    print ecosystem.constraints['dying']({'energy reserve': 9, 'age': 100, 'longevity': 30})
    print ecosystem.constraints['dying']({'energy reserve': 11, 'age': 1, 'longevity': 30})
    print ecosystem.constraints['dying']({'energy reserve': 10, 'age': 1, 'longevity': 30})
    print ecosystem.constraints['dying']({'energy reserve': 9, 'age': 1, 'longevity': 30})
    print ecosystem.constraints['dying']({'energy reserve': 110, 'age': 30, 'longevity': 30})
    print ecosystem.constraints['dying']({'energy reserve': 100, 'age': 30, 'longevity': 30})
    print ecosystem.constraints['dying']({'energy reserve': 190, 'age': 30, 'longevity': 30})
            
if __name__ == '__main__':
    main()
