from Biotope import *
from Tools import *


print """   TEST class Biotope """
biotope_data = {'size': (4, 6)}
fake_ecosystem = {}
fake_organism = {}

B = Biotope(biotope_data, parent_ecosystem = fake_ecosystem)

print B.biotope_data

loc = B.seek_free_location()
while loc:
    print loc,
    B.add_organism(fake_organism, loc)    
    loc = B.seek_free_location()
print "\nend."
for loc in B.random_locations.list:
    if loc[0] + loc[1] < 4:    
        B.delete_organism(loc)  # free upper left corner locations

center = (2, 3)
for radius in float_range(0, 3, 0.1):
    loc = B.seek_free_location_close_to(center, radius)
    print "radius =", radius, "location =", loc, "distance =", B.distance(center, loc)
print "\nend."
        
B.move_organism((3, 3), (0, 0))
    
B.random_locations.reset()

loc = B.seek_free_location()
while loc:
    print loc,
    B.add_organism(fake_organism, loc)    
    loc = B.seek_free_location()
    
