from GUI import GUI
from Basic_tools import *
from Biotope import *
from Settings import *
from Organism import *
from time import sleep
from Ecosystem import *
from random import *
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


def print_ecosystem_status(ecosystem):
    print ("time =", ecosystem.time, "Num of organisms =",
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
    print " *"*30, "\nWe start NOW!" # ***
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

    """ ***********************  TRIAL ZONE *********************************** 

    f_set = {'extract #biotope sunlight (percentage)': (
                            'normalized location x',
                            'normalized location y',
                            0.8
                        )}                       

    f_2_set = {'#biotope sunlight': ('normalized location x', 'normalized location y')}

    org = choice(ecosystem.organisms_list)
    print_dictionary(org)

    f = ecosystem.function_maker.read_function_settings('#organism', f_set)
    f_2 = ecosystem.function_maker.read_function_settings('#organism', f_2_set)

    print f(org), f_2(org)

    
    for i in range(10):
        org.act()

    print_dictionary(org)



    
    #f_set = ecosystem.settings['constraints']['can procreate']
    #f_set = {'cost': 'procreate'}
    f_set = 'time'
    f = ecosystem.function_maker.read_function_settings('#organism', f_set)

    #print f(ecosystem)
    
    for org in ecosystem.organisms_list:
        print f(org)
    
    error_maker = 1/0
    
     *********************** (TRIAL ZONE) *********************************** """

    
    if enable_graphics:
        gui = GUI(ecosystem)
    # Loop
    print "LOOPING:"
    while ((len(ecosystem.organisms_list) > 0) and
           (ecosystem.time < Total_time)):
        # Print ecosystem status:
        if ecosystem.time % time_lapse == 0:
            print_ecosystem_status(ecosystem)
            #organism1, organism2 = ecosystem.get_random_organisms(number_of_random_organisms = 2)
            #print_organism(organism1, 'energy reserve') # ***
        if Store_data:
            self.data_storer.store_data()        
        # Evolve:
        ecosystem.evolve()
        if enable_graphics:
            gui.handle_events()
            gui.draw_ecosystem()
        if make_sleeps:
            sleep(1.0)  # To remove

    print "Time:", ecosystem.time, "Number of organisms:", len(ecosystem.organisms_list) # ***

    if enable_graphics:
        gui.delete()


if __name__ == '__main__':
    main()














