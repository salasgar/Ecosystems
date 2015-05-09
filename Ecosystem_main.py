from GUI import GUI
# from time import sleep  # To remove
#import Biotope
#import Organism

def complete_with_default_values(experiment):
    if !('biotope' in experiment.keys()):
        experiment['biotope']= {
            'size': (100, 200),
        	'featuremaps': None }
    # TO DO More things    

def generate_functions(dictionary):
    if 'type' in dictionary:
        if dictionary['type'] == 'random function':
            return Tools.random_function_maker(dictionary)
        elif dictionary['type'] == 'outlay function':
            return Tools.outlay_function_maker(dictionary)
        elif dictionary['type'] == 'interpreted function':
            return Tools.interpreted_function_maker(dictionary)
    else:
        for x in dictionary:
            if type(dictionary[x]) == dict:
                dictionary[x] = generate_functions(dictionary[x])
            else:
                if hasattr(dictionary[x], __iter__):
                    for i in dictionary[x]:
                        if type(dictionary[x][i]) == dict:
                            dictionary[x][i] = generate_functions(dictionary[x][i])   
    return dictionary

class Ecosystem(object):

    def __init__(self, experiment):
        complete_with_default_values(experiment)
        generate_functions(experiment)
        self.experiment = experiment
        self.initialize_biotope(self.experiment['biotope'])
        self.initialize_organisms(self.experiment['organisms'])
        # self.initialize_featuremaps(experiment['featuremaps'])  """ This is included in self.initialize_biotope

    def initialize_biotope(self, experiment_biotope_data):
        pass  # TODO

    def initialize_organisms(self, experiment_organisms_data):
        for set_of_organisms in experiment_organisms_data:
            for N in range(experiment_organisms_data['number of organisms']):
                organism = {'location': self.biotope.seek_free_location()}
                for gene in set_of_organisms['genes']:
                    organism[gene] = set_of_organisms['genes'][gene]['initial values']()
                for status in set_of_organisms['status']:
                    organism[status] = set_of_organisms['status'][status]['initial values']()
                self.add_organism(organism)
                

    def evolve(self):
        # Biotope actions
        self.biotope.evolve()
    
        # Organisms actions
        # TODO: Adaptar a nuevos métodos
    
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
    ecosystem.create_organisms(initial_settings.initial_organisms)

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
