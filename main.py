from GUI import GUI
from Basic_tools import *
from Biotope import Biotope
from Settings import *
from Organism import *
from time import sleep
from Ecosystem import Ecosystem
import logging

logger = logging.getLogger('ecosystems')

def setup_logger():
    logger.setLevel(logging.DEBUG)
    # create a file handler
    handler = logging.FileHandler('ecosystems.log', mode='w')
    handler.setLevel(logging.DEBUG)
    # create a logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(module)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def print_ecosystem_status(ecosystem, time):
    print ("time =", time, "Num of organisms =",
           len(ecosystem.organisms_list))
    if print_ages:
        print [organism['age'] for organism in ecosystem.organisms_list]
    if print_organisms:
        for organism in ecosystem.organisms_list:
            print organism.__str__(
                list_of_attributes=('age',
                                    'energy reserve',
                                    'color'))

def main():
    setup_logger()
    logger.debug('DEBUG')
    print " *"*30, "\nWe start NOW!"
    #all_gene_names = extract_all_gene_names(my_example_of_ecosystem_settings)
    #all_strings = extract_all_strings(my_example_of_ecosystem_settings, exceptions = No_effect_commands + All_action_names)
    #print 'ALL GENES:', all_gene_names
    #print 'ALL STRINGS:', all_strings
    #print 'DIFFERENCE:', [item for item in all_strings if not item in all_gene_names and not item in All_allowed_commands_in_expression]
    enable_graphics = True
    make_sleeps = False
    time_lapse = 1
    Total_time = 200

    ecosystem = Ecosystem(my_example_of_ecosystem_settings)

    if enable_graphics:
        gui = GUI(ecosystem)
    # Loop
    time = 0

    while ((len(ecosystem.organisms_list) > 0) and
           (time < Total_time)):
        # Print ecosystem status:
        if time % time_lapse == 0:
            print_ecosystem_status(ecosystem, time)
            #organism1, organism2 = ecosystem.get_random_organisms(number_of_random_organisms = 2)
            #print_organism(organism1, 'energy reserve')
        # Evolve:
        ecosystem.evolve()
        if enable_graphics:
            gui.handle_events()
            gui.draw_ecosystem()
        if make_sleeps:
            sleep(1.0)  # To remove
        time += 1

    print "Time:", time, "Number of organisms:", len(ecosystem.organisms_list)

    if enable_graphics:
        gui.delete()


if __name__ == '__main__':
    main()
