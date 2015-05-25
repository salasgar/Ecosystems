
from Ecosystem_settings import *
from Tools import *
from copy import *
from Biotope import *
"""
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

"""

f = lambda:"ey!"

print isinstance(f, FunctionType)

print hasattr(f, '__call__')


K = lambda x: (
    x() if isinstance(x, FunctionType) else x,
    1)

print K(f)

print K('f')

print ".".join(str(5) for i in range(3))

color = make_function(ecosystem_settings['organisms'][0]['genes']['color'], 1)  

print color

print tuple(color[x]({'attack capacity': 5, 'photosynthesis capacity': 300, 'energy reserve': 100}) for x in range(3))
