from GUI import GUI
from Tools import *
from Biotope import Biotope


# from time import sleep  # To remove
# import Biotope
# import Organism

things_to_see = {
    "https://www.coursera.org/course/ml",
    ""
}


def make_mutability(mutability_definition, gene):    
    if 'new value' in mutability_definition:
        calculate_new_value = make_function(mutability_definition['new value'])
    elif 'absolute variation' in mutability_definition:
        absolute_variation = make_function(mutability_definition['absolute variation'])
        if 'percentage variation' in mutability_definition:
            percentage_variation = make_function(mutability_definition['percentage variation'])
            calculate_new_value = lambda organism: organism[gene] * (1 + percentage_variation(organism)) + absolute_variation(organism)
        else:
            calculate_new_value = lambda organism: organism[gene] + absolute_variation(organism)
    elif 'percentage variation' in mutability_definition:
        calculate_new_value = lambda organism: organism[gene] * (1 + percentage_variation(organism))
    else:
        calculate_new_value = lambda organism: organism[gene] # (no mutation) 
    if 'mutation frequency' in mutability_definition:
        mutation_frequency = make_function(mutability_definition['mutation frequency'])
    else:
        mutation_frequency = lambda organism: 1
    will_mutate = lambda organism: (random() < mutation_frequency(organism))
    if 'allowed interval' in mutability_definition:
        interval = mutability_definition['allowed interval']
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
        
class Ecosystem(object):

    def __init__(self, ecosystem_definition):
        self.ecosystem_definition = ecosystem_definition
        self.complete_with_default_values(self.ecosystem_definition)
        self.initialize_biotope(self.ecosystem_definition['biotope'])
        self.initialize_organisms(self.ecosystem_definition['organisms'])

    def complete_with_default_values(self, ecosystem_definition):
        if 'biotope' not in ecosystem_definition.keys():
            ecosystem_definition['biotope'] = {
                'size': (100, 200),
                'featuremaps': None}
        # TODO More things
                

    def initialize_biotope(self, biotope_definition):
        self.biotope = Biotope(biotope_definition = biotope_definition, parent_ecosystem = self)

    def add_organism(self, organism):
        self.biotope.add_organism(organism)
        self.newborns.append(organism)  
        
    def delete_organism(organism):
        self.biotope.delete_organism(organism['location'])
        if organism in self.newborns:
            self.newborns.delete(organism) 
        if organism in self.organisms_list:
            self.organisms_list.delete(organism)            
        
    def initialize_organisms(self, organisms_definition):
        self.newborns = []
        if isinstance(organisms_definition, dict):
            organisms_definition = [organisms_definition]
        for organisms_category in organisms_definition:
            for _ in range(organisms_category['number of organisms']):
                # Note: By the moment, location has random distribution
                organism = {'location': self.biotope.seek_free_location(), 'mutating genes': {}}
                genes_definition = organisms_category['genes']
                for gene in genes_definition.keys():
                    if isinstance(genes_definition[gene], dict) and ('initial value' in genes_definition[gene]):
                        initial_value_generator = make_function(genes_definition[gene]['initial value'])
                    else:
                        initial_value_generator = make_function(genes_definition[gene])
                    organism[gene] = initial_value_generator(organism)
                    if isinstance(genes_definition[gene], dict) and ('mutability' in genes_definition[gene]):
                        organism['mutating genes'][gene] = make_mutability(genes_definition[gene]['mutability'], gene)       
                status_definition = organisms_category['status']
                for status in status_definition:
                    if isinstance(status_definition[status], dict) and ('initial value' in status_definition[status]):
                        initial_value_generator = make_function(status_definition[status]['initial value'])
                    else:
                        initial_value_generator = make_function(status_definition[status])
                    organism[status] = initial_value_generator(organism)
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
    ecosystem_definition = None
    ecosystem = Ecosystem(ecosystem_definition)
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
