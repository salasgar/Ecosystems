from Tools import *
from copy import *
from Biotope import *

size = (3, 2)
B = Biotope({'size': size}, {})
for i in range(10):
    print B.random_free_locations.list, B.random_free_locations.last_location_index
    loc = B.seek_free_location()
    print B.add_organism({}, location = loc)
    print B.organisms_matrix

for i in range(10):
    loc = B.seek_possible_prey_close_to((1, 1), i)
    B.delete_organism(loc)
    print "\n", B.organisms_matrix
    
for i in range(10):
    print B.random_free_locations.list, B.random_free_locations.last_location_index
    loc = B.seek_free_location_close_to(center = (0,0), radius = 1)
    print B.add_organism({}, location = loc)
    print B.organisms_matrix



