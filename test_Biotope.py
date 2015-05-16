from Biotope import *
from Tools import *
from random import *
from copy import *


print """   TEST class Biotope """
biotope_settings = {'size': (4, 6)}
fake_ecosystem = {}
fake_organism = {}

B = Biotope(biotope_settings, parent_ecosystem = fake_ecosystem)

print B.settings

loc = B.seek_free_location()
while loc:
    print loc,
    B.add_organism(fake_organism, loc)    
    loc = B.seek_free_location()
print "\nend."
for loc in B.random_free_locations.list:
    if loc[0] + loc[1] < 4:    
        B.delete_organism(loc)  # free upper left corner locations

center = (2, 3)
for radius in float_range(0, 3, 0.1):
    loc = B.seek_free_location_close_to(center, radius)
    print "radius =", radius, "location =", loc, "distance =", B.distance(center, loc)
print "\nend."
        
B.move_organism((3, 3), (0, 0))
    
B.random_free_locations.reset()

loc = B.seek_free_location()
while loc:
    print loc,
    B.add_organism({}, loc)    
    loc = B.seek_free_location()
print B.organisms_matrix
print B.random_free_locations.list
print B.organisms_matrix

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


print "\n"*3, """ three different definitionss of distance: """
size = (25, 25)
biotope_settings['size'] = size
B = Biotope(biotope_settings, fake_ecosystem)
center = (choice(range(size[0])), choice(range(size[1])))
matrix = Matrix(*size)
for x in range(size[0]):
    for y in range(size[1]):
        matrix[x, y] = round(B.distance((x, y), center, mode = 'circle'))/10
print "\n"*3, matrix
for x in range(size[0]):
    for y in range(size[1]):
        matrix[x, y] = round(B.distance((x, y), center, mode = 'square'))/10
print "\n"*3, matrix
for x in range(size[0]):
    for y in range(size[1]):
        matrix[x, y] = round(B.distance((x, y), center, mode = 'tilted square'))/10
print "\n"*3, matrix

""""""

print "\n"*3, """ SEEK LOCATION """
size = (5, 5)
biotope_settings['size'] = size
B = Biotope(biotope_settings, fake_ecosystem)
center = (choice(range(size[0])), choice(range(size[1])))
B.add_organism(fake_organism, center)
for i in range(10):
    B.add_organism(deepcopy(fake_organism))
print B.organisms_matrix
"""
for radius in float_range(0, 5, 0.1):
    new_baby_location = B.seek_free_location_close_to(center, radius)
    if new_baby_location != None:
        B.add_organism(fake_organism, new_baby_location)
        print new_baby_location, B.organisms_matrix[new_baby_location]
    else:
        print "No baby"
"""
for radius in float_range(0, 2, 0.1):
    prey_location = B.seek_possible_prey_close_to(center, radius)        
    if prey_location != None:
        print prey_location, B.organisms_matrix[prey_location]
        B.delete_organism(prey_location)
    else:
        print "No prey"
    




































