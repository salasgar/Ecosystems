import Tools
import actions
import initial_settings
from GUI import GUI
from time import sleep  # To remove
import Biotope
import Organism

# Creation of biotope
BIOTOPE_SIZE_X, BIOTOPE_SIZE_Y, REPRODUCTION_FREQUENCY, GLOBAL_LONGEVITY = initial_settings.BIOTOPE_SIZE_X, initial_settings.BIOTOPE_SIZE_Y, initial_settings.REPRODUCTION_FREQUENCY, initial_settings.GLOBAL_LONGEVITY



class Ecosystem(object):
    organisms = []
    newborns = []
    biotope = None

    def __init__(self, biotope_size_x, biotope_size_y):
        self.biotope = Biotope.Biotope(biotope_size_x, biotope_size_y)
        self.biotope.set_Ecosystem(self)
        
    def create_organisms(self, org_list):
        for (N, Data) in org_list:
            for i in range(N):
                new_loc = self.biotope.seek_free_pos()
                if new_loc != None:
                    new_org = Organism.Organism(Data)
                    new_org.setLocation(new_loc)
                    self.organisms.append(new_org)

    def evolve(self):
        # Biotope actions
        actions.BiotopeActions.change_temperature(self)  # Temporal

        # Organisms actions
        i = 0
        while i < len(self.organisms):
            organism = self.organisms[i]
            # Actions:
            actions.OrganismActions.move(organism, self) # Temporal
            actions.OrganismActions.eat(organism, self) # Temporal
            if organism['genes']['do_photosynthesis']:
                actions.OrganismActions.do_photosynthesis(organism, self) # Temporal
            
            # Procreation and death of organism:
            organism.procreate(self)
            organism.age(self)
            
            # Get i pointing to right organism:
            i = i + 1
        self.organisms += self.newborns
        self.newborns = []
        # print 'Num of organisms + newborns: %d' % len(self.organisms)


def main():
    # create Ecosystem
    ecosystem = Ecosystem(BIOTOPE_SIZE_X, BIOTOPE_SIZE_Y)
    # Add initial organisms to the ecosystem:
    ecosystem.create_organisms(initial_settings.initial_organisms)
    
    gui = GUI()
    # Loop
    time = 0
    while (len(ecosystem.organisms) > 0) and (time < 300):  # TODO: Define correct condition
        ecosystem.evolve()
        gui.handle_events(ecosystem)
        gui.draw_ecosystem(ecosystem)
        sleep(0.1)  # To remove
        time += 1
        if time%10 == 0:
            print "time =", time, "Num of organisms =", len(ecosystem.organisms)
    gui.delete()

if __name__ == '__main__':
    main()
