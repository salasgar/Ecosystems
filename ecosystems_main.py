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
        i = 0
        while i < len(ecosystem.individuals):
            individual = self.individuals[i]
            # Actions:
            actions.Individual.move(individual, self)
            actions.Individual.eat(individual, self)
            if individual['genes']['do_photosynthesis']:
                actions.Individual.do_photosynthesis(individual, self)

            # Procreation and death of individual:
            n_new = actions.Individual.procreate(individual, self)
            n_deleted = actions.Individual.check_if_die_and_delete(individual,
                                                                   self)
            # Get i pointing to right individual:
            i += 1 + n_new - n_deleted


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
