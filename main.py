from GUI import GUI
import os
from Basic_tools import *
from Biotope import *
from Settings import *
from Organism import *
from time import sleep
from Ecosystem import *
from random import *
import logging
import numpy
import pickle
import flufl.lock

logger = logging.getLogger('ecosystems')
lock = flufl.lock.Lock('./GUI_pruebas/map.lock')
commands_file_path = './ecosystem.commands'  # JUST FOR DEBUG


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
    if print_number_of_deths:
        print 'Number of deths:', ecosystem.number_of_new_deths,
    if print_number_of_births:
        print 'New births:', ecosystem.number_of_new_births,
    if print_metabolic_speed > 0:
        org_list = ecosystem.get_random_organisms(print_metabolic_speed)
        for org in org_list:
            print_organism(org, 'metabolic speed', 'metabolic time')


def export_organisms_map(ecosystem):
    size_x = ecosystem.size_x()
    size_y = ecosystem.size_y()
    R = numpy.zeros((size_x, size_y))
    G = numpy.zeros((size_x, size_y))
    B = numpy.zeros((size_x, size_y))
    for organism in ecosystem.organisms_list:
        # Get organism information
        # TODO: access by organism.get_x() or similar
        o_x = organism['location'][0]
        o_y = organism['location'][1]
        # Draw organism
        # TODO: Define proper color
        if 'color' in organism:
            o_color = organism['color'](organism)
            # print o_color
        elif organism['speed'] == 0.0:
            o_color = (0, 150, 0)
        else:
            o_color = (200, 200, 200)
        R[o_x, o_y] = o_color[0] / 256.0
        G[o_x, o_y] = o_color[1] / 256.0
        B[o_x, o_y] = o_color[2] / 256.0
    RGB_matrix = numpy.dstack((R, G, B))
    lock.lock()
    pickle.dump(RGB_matrix, open('./GUI_pruebas/map.p', 'wb'))
    lock.unlock()


def main():
    commands_lock = flufl.lock.Lock(commands_file_path + '.lock')
    setup_logger()
    logger.debug('DEBUG')
    print " *" * 30, "\nWe start NOW!"  # ***
    # all_gene_names = extract_all_gene_names(my_example_of_ecosystem_settings)
    # all_strings = extract_all_strings(
    #    my_example_of_ecosystem_settings,
    #    exceptions = No_effect_directives + All_action_names)
    # print 'ALL GENES:', all_gene_names
    # print 'ALL STRINGS:', all_strings
    # print 'DIFFERENCE:', [
    #    item
    #    for item in all_strings
    #    if not item in all_gene_names and \
    #        not item in All_allowed_directives_in_expression]
    enable_graphics = False  # True
    make_sleeps = False
    time_lapse = 4
    Total_time = 5000

    ecosystem = Ecosystem(my_example_of_ecosystem_settings,
                          Elements_to_store)

    ecosystem.minimum_population_allowed = 200

    """ ***********************  TRIAL ZONE ****************************

    ecosystem.evolve()

    org = ecosystem.get_random_organisms(1)[0]

    print_dictionary(
        evaluate_functions_of_a_dictionary(
            org['offers to sell'], org
            )
        )

    f_set = {'-': ('nutrient A reserve', 'minimum nutrient A reserve for procreating')}
    f = ecosystem.function_maker.read_function_settings(
        '#organism',
        f_set)


    print_organism(org, 'nutrient A reserve', 'minimum nutrient A reserve for procreating')
    print_organism(org, 'nutrient A surplus')

    print f(org)

    print org['value in next cycle']['nutrient A surplus'](org)

    exit()

    f_set = {'curve from 0 to 1': 'photosynthesis capacity'}

    f = ecosystem.function_maker.read_function_settings(
        'output function #organism #input',
        f_set)

    for org in ecosystem.organisms_list:
        print f(org, 5)

    exit()

    f_set = {'extract #biotope sunlight (percentage)': (
                            'normalized location x',
                            'normalized location y',
                            0.8
                        )}

    f_2_set = {
        '#biotope sunlight': (
            'normalized location x',
            'normalized location y'
            )
        }

    org = choice(ecosystem.organisms_list)
    print_dictionary(org)

    f = ecosystem.function_maker.read_function_settings('#organism', f_set)
    f_2 = ecosystem.function_maker.read_function_settings('#organism', f_2_set)

    print f(org), f_2(org)

    for i in range(10):
        org.act()

    print_dictionary(org)

    # f_set = ecosystem.settings['constraints']['can procreate']
    # f_set = {'cost': 'procreate'}
    f_set = 'time'
    f = ecosystem.function_maker.read_function_settings('#organism', f_set)

    # print f(ecosystem)

    for org in ecosystem.organisms_list:
        print f(org)

    exit()

    *********************** (TRIAL ZONE) ************************** """
    status = ''
    if enable_graphics:
        gui = GUI(ecosystem)
    # Loop
    print "LOOPING:"
    # COMMANDS MANAGEMENT (temporary, just debug):
    # TODO: Think a better place for commands management.
    while ((len(ecosystem.organisms_list) > 0) and
           (ecosystem.time < Total_time)):
        if os.path.exists(commands_file_path):
            commands_lock.lock()
            with open(commands_file_path, 'r') as f:
                status = f.readline()
            commands_lock.unlock()
        if status == 'PAUSE':
            sleep(0.5)
            continue
        # Print ecosystem status:
        if ecosystem.time % time_lapse == 0:
            print_ecosystem_status(ecosystem)
            # organism1, organism2 = ecosystem.get_random_organisms(
            #    number_of_random_organisms = 2)
        Store_data = True
        if Store_data:
            ecosystem.data_storer.store_data('./experiments_histories')
        # Evolve:
        ecosystem.evolve()
        if enable_graphics:
            gui.handle_events()
            gui.draw_ecosystem()
        if make_sleeps:
            sleep(1.0)  # To remove
        if ecosystem.population() < ecosystem.minimum_population_allowed:
            n = ecosystem.minimum_population_allowed - ecosystem.population()
            ecosystem.create_new_organisms(n)
            print n, "organisms created",

    print "Time:", ecosystem.time, "Number of organisms:", \
        len(ecosystem.organisms_list)  # ***

    if enable_graphics:
        gui.delete()


if __name__ == '__main__':
    main()
