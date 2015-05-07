import actions
import initial_settings
from GUI import GUI
# from time import sleep  # To remove
#import Biotope
#import Organism


class Ecosystem(object):

    def __init__(self, experiment):
        self.initialize_organisms(experiment['organisms'])
        self.initialize_biotope(experiment['biotope'])
        self.initialize_substances(experiment['substances'])

    def initialize_biotope(self, experiment_biotope_data):
        pass  # TODO

    def initialize_organisms(self, experiment_organisms_data):
        pass  # TODO

    def initialize_substances(self, experiment_substances_data):
        pass  # TODO

    def evolve(self):
        # Biotope actions
        actions.BiotopeActions.change_temperature(self)  # Temporal

        # Organisms actions
        i = 0
        while i < len(self.organisms):
            organism = self.organisms[i]
            # Actions
            organism.move(self)

            # Procreation and death of organism:
            organism.procreate(self)
            org_status = organism.age(self)
            if org_status == 'Dead':
                self.organisms.remove(organism)

            # Get i pointing to right organism:
            i = i + 1
        self.organisms += self.newborns
        self.newborns = []
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
