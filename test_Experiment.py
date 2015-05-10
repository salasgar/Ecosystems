from Experiment import experiment
from Tools import *


hunting = {
          'type': 'outlay function',
          'name': 'linear function',
          'terms': [
              {'parameter': 'strength', 'coefficient': 3.0}, 
              {'parameter': 'speed', 'coefficient': 0.2}, 
              {'parameter': None, 'coefficient': 5.0}]}

living = {
		'type': 'outlay function',
		'name': 'n-linear function',
		'terms': [
			{'parameters': ['attack capacity', 'defense capacity'], 		'coefficient': 1.0}, 
                  	{'parameters': ['photosynthesis capacity'], 				'coefficient': -1.0},
			{'parameters': ['attack capacity', 'photosynthesis capacity'], 	'coefficient': 25.0}, 
			{'parameters': [], 								'coefficient': 0.5}]} 

organism = {'strength': 2.0, 
            'speed': 3.0,
            'attack capacity': 5.0,
            'defense capacity': 2.0,
            'photosynthesis capacity': 10.0}

def outlay_function_maker(function_dict):
    if function_dict['type'] == 'outlay function':
        print function_dict['name']
        if function_dict['name'] == 'linear function':
            independent_term = 0
            dependent_terms = []
            for term in function_dict['terms']:
                if term['parameter'] == None:
                    independent_term = term['coefficient']
                else:
                    dependent_terms.append((term['parameter'], term['coefficient']))
            return lambda organism: sum([(organism[parameter] * coefficient) for (parameter, coefficient) in dependent_terms], independent_term)
        elif function_dict['name'] == 'n-linear function':
            return lambda organism: sum([(prod([organism[parameter] for parameter in term['parameters']])*term['coefficient']) for term in function_dict['terms']])
    return lambda organism: 0
            

hunting_outlay = outlay_function_maker(hunting)

living_outlay = outlay_function_maker(living)

print hunting_outlay(organism), living_outlay(organism)


print prod([2, 3, 4]), prod([])
