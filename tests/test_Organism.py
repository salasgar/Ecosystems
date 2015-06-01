from Organism import *
from Ecosystem_settings import ecosystem_settings
from Ecosystem_main import Ecosystem


ecosystem = Ecosystem(ecosystem_settings)

print """ Test 1 """
for organism in ecosystem.organisms_list:
    print 'strength:', organism['strength']
    
for organism in ecosystem.organisms_list:
    print organism

for organism in ecosystem.organisms_list:
    print organism.__str__(indent_level = 1)











