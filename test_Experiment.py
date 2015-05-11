from Experiment import experiment
from Tools import *


hunting_outlay_dict = {
          'type': 'outlay function',
          'subtype': 'linear function',
          'terms': [
              {'parameter': 'strength', 'coefficient': 3.0}, 
              {'parameter': 'speed', 'coefficient': 0.2}, 
              {'parameter': None, 'coefficient': 5.0}]}

living_outlay_dict = {
		'type': 'outlay function',
		'subtype': 'n-linear function',
		'terms': [
			{'parameters': ['attack capacity', 'defense capacity'], 		'coefficient': 1.0}, 
                  	{'parameters': ['photosynthesis capacity'], 				'coefficient': -1.0},
			{'parameters': ['attack capacity', 'photosynthesis capacity'], 	'coefficient': 25.0}, 
			{'parameters': [], 								'coefficient': 0.5}]} 
dying_constraint_dict = {
		'type': 'constraint function',
		'subtype': 'thresholds',
            'operator': 'or',
            'terms': [
                {'parameter': 'energy reserve', 
                'operator': '<',
                'threshold': 10.0},
                {'parameter': 'age',
                'operator': '>',
                'random threshold': {
                    'type': 'random function',
                    'subtype': 'gaussian',
                    'mean': 120,
                    'variance': 20}
                    }              
                ]
		}
  
hunting_constraint_dict = {
		'type': 'constraint function',
		'subtype': 'hunting',
		'a': ('predator', 'strength'),
		'b': ('prey', 'strength'),
		'r1': ('random number', 'uniform_distribution [0, 1]'),
		'r2': ('random number', 'uniform_distribution [0, 1]'),
		'expression': "a*r1 > b*r2"  }



organism = {'strength': 2.0, 
            'speed': 3.0,
            'attack capacity': 5.0,
            'defense capacity': 2.0,
            'photosynthesis capacity': 10.0,
            'age': 120,
            'energy reserve': 15.0}    
            
organism_prey = {'strength': 2.0, 
            'speed': 3.0,
            'attack capacity': 5.0,
            'defense capacity': 2.0,
            'photosynthesis capacity': 10.0,
            'age': 120,
            'energy reserve': 15.0}    
            
            
    
hunting_outlay = outlay_function_maker(hunting_outlay_dict)

living_outlay = outlay_function_maker(living_outlay_dict)

dying_test = constraint_function_maker(dying_constraint_dict)

hunting_constraint = constraint_function_maker(hunting_constraint_dict)

print hunting_outlay(organism), living_outlay(organism), dying_test(organism), hunting_constraint(organism, organism_prey)

