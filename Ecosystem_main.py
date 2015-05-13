from GUI import GUI
import Tools
# from time import sleep  # To remove
# import Biotope
# import Organism

def make_mutability(description, gene):
    if 'new value' in description:
        calculate_new_value = make_function(description['new value'])
    elif 'absolute variation' in description:
        absolute_variation = make_function(description['absolute variation'])
        if 'percentage variation' in description:
            percentage_variation = make_function(description['percentage variation'])
            calculate_new_value = lambda organism: organism[gene] * (1 + percentage_variation(organism)) + absolute_variation(organism)
        else:
            calculate_new_value = lambda organism: organism[gene] + absolute_variation(organism)
    elif 'percentage variation' in description:
        calculate_new_value = lambda organism: organism[gene] * (1 + percentage_variation(organism))
    else:
        calculate_new_value = lambda organism: organism[gene] # (no mutation) 
    if 'mutation frequency' in description:
        mutation_frequency = make_function(description['mutation frequency'])
    else:
        mutation_frequency = lambda organism: 1
    will_mutate = lambda organism: (random() < mutation_frequency(organism))
    if 'allowed interval' in description:
        new_value = lambda 
    else:
        new_value = calculate_new_value
    # TODO: 'allowed interval'
    return new_value
    
        
class Ecosystem(object):

    def __init__(self, experiment):
        self.experiment = experiment
        self.complete_with_default_values(self.experiment)
        self.initialize_biotope(self.experiment['biotope'])
        self.initialize_organisms(self.experiment['organisms'])

    def complete_with_default_values(self, experiment):
        if 'biotope' not in experiment.keys():
            experiment['biotope'] = {
                'size': (100, 200),
                'featuremaps': None}
        # TODO More things


    def initialize_biotope(self, biotope_data_definition):
        self.biotope = Biotope(biotope_data = biotope_data_definition, parent_ecosystem = self)

    def add_organism(organism):
        self.biotope.add_organism(organism)
        self.newborns.append(organism)  
        
    def delete_organism(organism):
        self.biotope.delete_organism(organism['location'])
        if organism in self.newborns:
            self.newborns.delete(organism) 
        if organism in self.organisms_list:
            self.organisms_list.delete(organism)            
        
    def initialize_organisms(self, experiment_organisms_data):
        self.newborns = []
        for organisms_category in experiment_organisms_data:
            for _ in range(experiment_organisms_data['number of organisms']):
                # Note: By the moment, location has random distribution
                organism = {'location': self.biotope.seek_free_location(), 'mutability': {}}
                genes_dict = organisms_category['genes']
                for gene in genes_dict.keys():
                    initial_value_generator = Tools.make_function(genes_dict[gene]['initial value'])
                    organism[gene] = initial_value_generator(organism)
                    if 'mutability' in genes_dict[gene]:
                        organism['mutability'][gene] = make_mutability(genes_dict[gene]['mutability'], gene)       
                status_dict = organisms_category['status']
                for status in status_dict:
                    initial_value_generator = Tools.make_function(status_dict[status]['initial value'])
                    organism[status] = initial_value_generator(organism)
                self.add_organism(organism)
        self.organisms_list = self.newborns
        self.newborns = []

    def evolve(self):
        # Biotope actions
        self.biotope.evolve()
        # Organisms actions
        # TODO: Adaptar a nuevos métodos
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
    experiment = None
    ecosystem = Ecosystem(experiment)
    # Add initial organisms to the ecosystem:

    gui = GUI(ecosystem)
    # Loop
    time = 0
    while (len(ecosystem.organisms) > 0) and (time < 300):
        # TODO: Define correct condition
        ecosystem.evolve()
        gui.handle_events()
        gui.draw_ecosystem()
        # sleep(0.1)  # To remove
        time += 1
        if time % 10 == 0:
            print ("time =", time, "Num of organisms =",
                   len(ecosystem.organisms))
    gui.delete()

if __name__ == '__main__':
    main()
