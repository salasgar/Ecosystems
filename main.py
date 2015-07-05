from GUI import GUI
from Tools import *
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
    # create Ecosystem
    ecosystem = Ecosystem(ecosystem_settings_1)
    enable_graphics = True
    make_sleeps = False
    time_lapse = 1
    Total_time = 200000
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

    if enable_graphics:
        gui.delete()


if __name__ == '__main__':
    main()
