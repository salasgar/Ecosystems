class Biotope:
    @staticmethod
    def change_temperature(Ecosystem):
        pass


class Organism:
    @staticmethod
    def move(organism, ecosystem):
        pass

    @staticmethod
    def eat(organism, ecosystem):
        pass

    @staticmethod
    def do_photosynthesis(organism, ecosystem):
        pass

    @staticmethod
    def procreate(organism, ecosystem):
        # TEMPORARY EXAMPLE
        # add new organisms at the beginning of the list (as a queue)
        # using ecosystem.organisms.insert(0, new_organism)
        from random import random
        if random() > 0.99:
            print ('Oh organism %d-th had a baby:' %
                   ecosystem.organisms.index(organism))
            ecosystem.organisms.insert(0, organism.copy())  # Mutation?
            print 'Num of organisms: %d' % len(ecosystem.organisms)
            return 1
        else:
            return 0

    @staticmethod
    def check_if_die_and_delete(organism, ecosystem):
        # Temporary random delete
        from random import random
        if random() > 0.98:
            print ('%d-th organism DIED:' %
                   ecosystem.organisms.index(organism))
            ecosystem.organisms.remove(organism)
            print 'Num of organisms: %d' % len(ecosystem.organisms)
            return 1
        else:
            return 0
