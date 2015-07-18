from GUI import GUI
from Tools import *
from Biotope import Biotope
from Settings import *
from Organism import *
from time import sleep
from Ecosystem import Ecosystem
import logging
import numpy
import pickle
import flufl.lock

logger = logging.getLogger('ecosystems')
lock = flufl.lock.Lock('./GUI_pruebas/map.lock')


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
        R[o_x, o_y] = o_color[0]/256.0
        G[o_x, o_y] = o_color[1]/256.0
        B[o_x, o_y] = o_color[2]/256.0
    RGB_matrix = numpy.dstack((R, G, B))
    lock.lock()
    pickle.dump(RGB_matrix, open('./GUI_pruebas/map.p', 'wb'))
    lock.unlock()


def main():
    setup_logger()
    logger.debug('DEBUG')
    print " *"*30, "\nWe start NOW!"
    # create Ecosystem
    ecosystem = Ecosystem(ecosystem_settings_3)
    enable_graphics = False
    make_sleeps = False
    time_lapse = 1
    Total_time = 2000000
    if enable_graphics:
        gui = GUI(ecosystem)
    # Loop
    time = 0

    while ((len(ecosystem.organisms_list) > 0) and
           (time < Total_time)):
        # Print ecosystem status
        if time % time_lapse == 0:
            print_ecosystem_status(ecosystem, time)
        # Evolve
        ecosystem.evolve()
        if enable_graphics:
            gui.handle_events()
            gui.draw_ecosystem()
        if make_sleeps:
            sleep(1.0)  # To remove
        time += 1
        export_organisms_map(ecosystem)

    if enable_graphics:
        gui.delete()


if __name__ == '__main__':
    main()
