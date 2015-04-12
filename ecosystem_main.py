import actions
import initial_settings
from GUI import GUI
from time import sleep  # To remove


class Ecosystem(object):

    def __init__(self, organisms, biotope):
        self.organisms = organisms
        self.biotope = biotope
        self.biotope.set_Ecosystem(self)

    def evolve(self):
        # Biotope actions
        actions.BiotopeActions.change_temperature(self)

        # Organisms actions
        i = 0
        while i < len(self.organisms):
            organism = self.organisms[i]
            # Actions:
            actions.OrganismActions.move(organism, self)
            actions.OrganismActions.eat(organism, self)
            if organism['genes']['do_photosynthesis']:
                actions.OrganismActions.do_photosynthesis(organism, self)
            
            # Procreation and death of organism:
            n_new = actions.OrganismActions.procreate(organism, self)
            n_deleted = actions.OrganismActions.check_if_die_and_delete(organism,
                                                                 self)
            # Get i pointing to right organism:
            i = i + 1 + n_new - n_deleted


def main():
    # create Ecosystem
    ecosystem = Ecosystem(initial_settings.organisms,
                          initial_settings.biotope)
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
