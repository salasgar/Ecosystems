import actions
import experiment_settings
from GUI import GUI
from time import sleep  # To remove


class Ecosystem(object):

    def __init__(self, individuals, biotope):
        self.individuals = individuals
        self.biotope = biotope

    def evolve(self):
        # Biotope actions
        actions.Biotope.change_temperature(self)

        # Individuals actions
        for individual in self.individuals[:]:
            actions.Individual.move(individual, self)
            actions.Individual.eat(individual, self)
            if individual['genes']['do_photosynthesis']:
                actions.Individual.do_photosynthesis(individual, self)
            actions.Individual.check_if_die_and_delete(individual, self)


def main():
    # create Ecosystem
    ecosystem = Ecosystem(experiment_settings.individuals,
                          experiment_settings.biotope)
    gui = GUI()

    # Loop
    while len(ecosystem.individuals) > 0:  # TODO: Define correct condition
        ecosystem.evolve()
        gui.handle_events(ecosystem)
        gui.draw_ecosystem(ecosystem)
        sleep(0.1)

    gui.delete()


if __name__ == '__main__':
    main()
