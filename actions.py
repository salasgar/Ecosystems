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
        # TEMPORARY EXAMPLE
        # add new individuals at the beginning of the list (as a queue)
        # using ecosystem.individuals.insert(0, new_individual)
        from random import random
        if random() > 0.99:
            print ('Oh individual %d-th had a baby:' %
                   ecosystem.individuals.index(individual))
            ecosystem.individuals.insert(0, individual.copy())  # Mutation?
            print 'Num of individuals: %d' % len(ecosystem.individuals)
            return 1
        else:
            return 0

    @staticmethod
    def check_if_die_and_delete(individual, ecosystem):
        # Temporary random delete
        from random import random
        if random() > 0.98:
            print ('%d-th individual DIED:' %
                   ecosystem.individuals.index(individual))
            ecosystem.individuals.remove(individual)
            print 'Num of individuals: %d' % len(ecosystem.individuals)
            return 1
        else:
            return 0
