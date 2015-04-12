import actions
import experiment_settings
from GUI import GUI
from time import sleep  # To remove


class Ecosystem(object):

    def __init__(self, organisms, biotope):
        self.organisms = organisms
        self.biotope = biotope

    def evolve(self):
        # Biotope actions
        actions.Biotope.change_temperature(self)

        # Organisms actions
        i = 0
        while i < len(self.organisms):
            organism = self.organisms[i]
            # Actions:
            actions.Organism.move(organism, self)
            actions.Organism.eat(organism, self)
            if organism['genes']['do_photosynthesis']:
                actions.Organism.do_photosynthesis(organism, self)

            # Procreation and death of organism:
            n_new = actions.Organism.procreate(organism, self)
            n_deleted = actions.Organism.check_if_die_and_delete(organism,
                                                                 self)
            # Get i pointing to right organism:
            i = i + 1 + n_new - n_deleted


def main():
    # create Ecosystem
    ecosystem = Ecosystem(experiment_settings.organisms,
                          experiment_settings.biotope)
    gui = GUI()
    # Loop
    while len(ecosystem.organisms) > 0:  # TODO: Define correct condition
        ecosystem.evolve()
        gui.handle_events(ecosystem)
        gui.draw_ecosystem(ecosystem)
        sleep(0.1)  # To remove
    gui.delete()


if __name__ == '__main__':
    main()
