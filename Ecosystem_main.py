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
    #print 'make_mutability'
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
    #print 'make_modifying_status'
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
        print 'load_settings'
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
        print 'initialize_biotope'
        self.biotope = Biotope(settings = self.settings['biotope'], parent_ecosystem = self)
                
    def initialize_outlays(self):
        print 'initialize_outlays'
        self.outlays = {}
        for action in self.settings['outlays']:
            self.outlays[action] = {}
            for reserve_substance in self.settings['outlays'][action]:
                self.outlays[action][reserve_substance] = make_function(self.settings['outlays'][action][reserve_substance], number_of_arguments = 1)
    
    def initialize_constraints(self):
        print 'initialize_constraints'
        self.constraints = {}
        for action in self.settings['constraints']:
            if action == 'kill?':
                self.constraints[action] = make_function(self.settings['constraints'][action], number_of_arguments = 2)        
            else:
                self.constraints[action] = make_function(self.settings['constraints'][action], number_of_arguments = 1)        
    
    def initialize_statistics(self):
        print 'initialize_statistics'
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
            for _ in range(organisms_category['number of organisms']):
                # Note: By the moment, location has random distribution
                new_organism = Organism(self, {'mutating genes': {}, 'modifying status': {}, 'list of reserve substances': []})
                genes_settings = organisms_category['genes']
                for gene in genes_settings.keys():
                    if isinstance(genes_settings[gene], dict):
                        if 'initial value' in genes_settings[gene]:
                            initial_value_generator = make_function(genes_settings[gene]['initial value'], number_of_arguments = 1)
                            new_organism[gene] = initial_value_generator(new_organism)
                        else: # the gene is a function:
                            new_organism[gene] = make_function(genes_settings[gene], number_of_arguments = 1)         
                        if 'mutability' in genes_settings[gene]:
                            new_organism['mutating genes'][gene] = make_mutability(genes_settings[gene]['mutability'], gene)       
                    else:
                        if isinstance(genes_settings[gene], str) and genes_settings[gene] in genes_settings:
                            new_organism[gene] = make_function(genes_settings[gene], number_of_arguments = 1)
                        else:
                            new_organism[gene] = genes_settings[gene]
                status_settings = organisms_category['status']
                for status in status_settings:
                    if isinstance(status_settings[status], dict):
                        if 'initial value' in status_settings[status]:
                            initial_value_generator = make_function(status_settings[status]['initial value'], number_of_arguments = 1)
                            new_organism[status] = initial_value_generator(new_organism)
                        else:
                            new_organism[status] = make_function(status_settings[status], number_of_arguments = 1)
                        if 'modifying' in status_settings[status]:
                            new_organism['modifying status'][status] = make_modifying_status(status_settings[status]['modifying'], status)       
                    else:
                        new_organism[status] = status_settings[status]                
                if 'energy reserve' in new_organism and not 'energy reserve' in new_organism['list of reserve substances']:
                    new_organism['list of reserve substances'].append('energy reserve')
                if 'color' in new_organism:
                    red = make_function(new_organism['color'][0], number_of_arguments = 1)
                    green = make_function(new_organism['color'][1], number_of_arguments = 1)
                    blue = make_function(new_organism['color'][2], number_of_arguments = 1)
                    
                                        
                                        
                    
                    
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
    print " *"*50, "\nWe start NOW!"
    # create Ecosystem
    ecosystem = Ecosystem(ecosystem_settings)
    
    enable_graphics = True
    time_lapse = 4
    make_pauses = False
    make_sleeps = False
    Total_time = 1000
    
    print_outlays = False
    print_deths = False
    print_births = False
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
            print ecosystem.count('category', 'plant'), 'plants and', ecosystem.count('category', 'animal'), 'animals'
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
        
    a = range(20)
    
    for i in a:
        print i, a
        if i < 10:
            del a[a.index(i)]   
        
            
if __name__ == '__main__':
    main()
