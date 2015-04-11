class Biotope:
    @staticmethod
    def change_temperature(Ecosystem):
        pass


class Individual:
    @staticmethod
    def move(individual, ecosystem):
        pass

    @staticmethod
    def eat(individual, ecosystem):
        pass

    @staticmethod
    def do_photosynthesis(individual, ecosystem):
        pass

    @staticmethod
    def procreate(individual, ecosystem):
        pass

    @staticmethod
    def check_if_die_and_delete(individual, ecosystem):
        # Temporary random delete
        from random import random
        if random() > 0.99:
            print ('Deleting %d-th individual:' %
                   ecosystem.individuals.index(individual))
            ecosystem.individuals.remove(individual)
            print 'Num of individuals: %d' % len(ecosystem.individuals)
