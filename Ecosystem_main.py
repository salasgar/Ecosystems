from GUI import GUI
import Tools
# from time import sleep  # To remove
# import Biotope
# import Organism


class Ecosystem(object):

    def __init__(self, experiment):
        self.experiment = experiment
        self.complete_with_default_values(self.experiment)
        self.replace_definitions_by_functions(self.experiment)
        self.initialize_biotope(self.experiment['biotope'])
        self.initialize_organisms(self.experiment['organisms'])

    def complete_with_default_values(self, experiment):
        if 'biotope' not in experiment.keys():
            experiment['biotope'] = {
                'size': (100, 200),
                'featuremaps': None}
        # TODO More things

    def replace_definitions_by_functions(self, experiment):
        """
            Recursively replace definitions of functions by actual functions.
        """
        if 'type' in experiment.keys():
            if experiment['type'] == 'random function':
                return Tools.random_function_maker(experiment)
            elif experiment['type'] == 'outlay function':
                return Tools.outlay_function_maker(experiment)
            elif experiment['type'] == 'constraint function':
                return Tools.constraint_function_maker(experiment)
            elif experiment['type'] == 'interpreted function':
                return Tools.interpreted_function_maker(experiment)
        else:
            # Get in a deeper level
            for key in experiment.keys():
                if isinstance(experiment[key], dict):
                    self.replace_definitions_by_functions(experiment[key])
                elif hasattr(experiment[key], '__iter__'):  # If it's iterable
                    for item in experiment[key]:
                        if isinstance(item, dict):
                            self.replace_definitions_by_functions(item)
                elif (isinstance(experiment[key], int) or
                      isinstance(experiment[key], float)):
                    def get_x(x): return x
                    experiment[key] = get_x
        return experiment

    def initialize_biotope(self, experiment_biotope_data):
        pass  # TODO

    def initialize_organisms(self, experiment_organisms_data):
        for organisms_category in experiment_organisms_data:
            for _ in range(experiment_organisms_data['number of organisms']):
                # Note: By the moment, location has random distribution
                organism = {'location': self.biotope.seek_free_location()}
                for gene in organisms_category['genes']:
                    organism[gene] = organisms_category[
                        'genes'][gene]['initial values']()
                for status in organisms_category['status']:
                    organism[status] = organisms_category[
                        'status'][status]['initial values']()
                self.add_organism(organism)

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
