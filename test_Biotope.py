from Biotope import *


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
    B.delete_organism(loc)
    
B.random_locations.reset()

loc = B.seek_free_location()
while loc:
    print loc,
    B.add_organism(fake_organism, loc)    
    loc = B.seek_free_location()