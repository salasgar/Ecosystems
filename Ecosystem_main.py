from GUI import GUI
from Tools import *
from Biotope import Biotope
from Ecosystem_settings import DEFAULT_SETTINGS, ecosystem_settings
from Organism import Organism


# from time import sleep  # To remove
# import Biotope
# import Organism

things_to_see = {
    "https://www.coursera.org/course/ml",
    ""
}


def make_mutability(mutability_settings, gene):    
    if 'new value' in mutability_settings:
        calculate_new_value = make_function(mutability_settings['new value'])
    elif 'absolute variation' in mutability_settings:
        absolute_variation = make_function(mutability_settings['absolute variation'])
        if 'percentage variation' in mutability_settings:
            percentage_variation = make_function(mutability_settings['percentage variation'])
            calculate_new_value = lambda organism: organism[gene] * (1 + percentage_variation(organism)) + absolute_variation(organism)
        else:
            calculate_new_value = lambda organism: organism[gene] + absolute_variation(organism)
    elif 'percentage variation' in mutability_settings:
        percentage_variation = make_function(mutability_settings['percentage variation'])
        calculate_new_value = lambda organism: organism[gene] * (1 + percentage_variation(organism))
    else:
        calculate_new_value = lambda organism: organism[gene] # (no mutation) 
    if 'mutation frequency' in mutability_settings:
        mutation_frequency = make_function(mutability_settings['mutation frequency'])
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
        calculate_new_value = make_function(modifying_settings['new value'])
    elif 'absolute variation' in modifying_settings:
        absolute_variation = make_function(modifying_settings['absolute variation'])
        if 'percentage variation' in modifying_settings:
            percentage_variation = make_function(modifying_settings['percentage variation'])
            calculate_new_value = lambda organism: organism[status] * (1 + percentage_variation(organism)) + absolute_variation(organism)
        else:
            calculate_new_value = lambda organism: organism[status] + absolute_variation(organism)
    elif 'percentage variation' in modifying_settings:
        percentage_variation = make_function(modifying_settings['percentage variation'])
        calculate_new_value = lambda organism: organism[status] * (1 + percentage_variation(organism))
    else:
        calculate_new_value = lambda organism: organism[status] # (no change) 
    if 'changing frequency' in modifying_settings:
        changing_frequency = make_function(modifying_settings['changing frequency'])
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
        self.settings = ecosystem_settings                
        
    def initialize_biotope(self):
        self.biotope = Biotope(settings = self.settings['biotope'], parent_ecosystem = self)
                
    def initialize_outlays(self):
        self.outlays = {}
        for action in self.settings['outlays']:
            self.outlays[action] = make_function(self.settings['outlays'][action])
    
    def initialize_constraints(self):
        self.constraints = {}
        for action in self.settings['constraints']:
            self.constraints[action] = make_function(self.settings['constraints'][action])        

    def add_organism(self, organism):
        self.biotope.add_organism(organism)
        self.newborns.append(organism)  
        
    def delete_organism(organism):
        self.biotope.delete_organism(organism['location'])
        if organism in self.newborns:
            self.newborns.delete(organism) 
        if organism in self.organisms_list:
            self.organisms_list.delete(organism)            
        
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
                            initial_value_generator = make_function(genes_settings[gene]['initial value'])
                            organism[gene] = initial_value_generator(organism)
                        else: # the gene is a function:
                            organism[gene] = make_function(genes_settings[gene])         
                        if 'mutability' in genes_settings[gene]:
                            organism['mutating genes'][gene] = make_mutability(genes_settings[gene]['mutability'], gene)       
                    else:
                        organism[gene] = genes_settings[gene]
                status_settings = organisms_category['status']
                for status in status_settings:
                    if isinstance(status_settings[status], dict):
                        if 'initial value' in status_settings[status]:
                            initial_value_generator = make_function(status_settings[status]['initial value'])
                            organism[status] = initial_value_generator(organism)
                        else:
                            organism[status] = make_function(status_settings[status])
                        if 'modifying' in status_settings[status]:
                            organism['modifying status'][status] = make_modifying_status(status_settings[status]['modifying'], status)       
                    else:
                        organism[status] = status_settings[status]                
                if 'energy reserve' in organism:
                    organism['list of reserve substances'].append('energy reserve')
                self.add_organism(organism)
        self.organisms_list = self.newborns
        self.newborns = []

    def evolve(self):
        # Biotope actions
        self.biotope.evolve()
        # Organisms actions
        # TODO: Adaptar a nuevos metodos
        """
        for organism in self.organisms:
            # Actions
            organism.move(self)

            # Procreation and death of organism:
            organism.procreate(self)
            org_status = organism.age(self)
            if org_status == 'Dead':
                self.organisms.remove(organism)

        self.organisms += self.newborns
        self.newborns = []
        """
        # print 'Num of organisms + newborns: %d' % len(self.organisms)


def main():
    # create Ecosystem
    ecosystem = Ecosystem(ecosystem_settings)
    # Add initial organisms to the ecosystem:

    enable_graphics = False
    if enable_graphics:
        gui = GUI(ecosystem)
    # Loop
    time = 0
    while (len(ecosystem.organisms) > 0) and (time < 300):
        # TODO: Define correct condition
        ecosystem.evolve()
        if enable_graphics:
            gui.handle_events()
            gui.draw_ecosystem()
        # sleep(0.1)  # To remove
        time += 1
        if time % 10 == 0:
            print ("time =", time, "Num of organisms =",
                   len(ecosystem.organisms))
    if enable_graphics:
        gui.delete()

if __name__ == '__main__':
    main()
