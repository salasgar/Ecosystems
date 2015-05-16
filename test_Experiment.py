from Ecosystem_settings import ecosystem_settings
from Tools import *


hunting_outlay_settings = {
          'type': 'outlay function',
          'subtype': 'linear function',
          'terms': [
              {'parameter': 'strength', 'coefficient': 3.0}, 
              {'parameter': 'speed', 'coefficient': 0.2}, 
              {'parameter': None, 'coefficient': 5.0}]}

living_outlay_settings = {
		'type': 'outlay function',
		'subtype': 'n-linear function',
		'terms': [
			{'parameters': ['attack capacity', 'defense capacity'], 		'coefficient': 1.0}, 
                  	{'parameters': ['photosynthesis capacity'], 				'coefficient': -1.0},
			{'parameters': ['attack capacity', 'photosynthesis capacity'], 	'coefficient': 25.0}, 
			{'parameters': [], 								'coefficient': 0.5}]} 
   
dying_constraint_settings = {
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
  
hunting_constraint_settings = {
		'type': 'constraint function',
		'subtype': 'hunting',
            'predator value': {
                'type': 'random function',
                'subtype': 'gaussian',
                'mean': 'strength',
                'variance': 'strength'},
            'operator' : ">",
            'prey value': 'strength'
            }



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

function1 = {
    'type': 'random function',
    'subtype': 'gaussian',
    'mean': 'age',
    'variance': {
        'type': 'random function',
        'subtype': 'uniform distribution',
        'interval': ['photosynthesis capacity', 'energy reserve']
    }}  
print [make_function(function1)(organism) for i in range(10)]    
print make_function(living_outlay_settings)(organism)   
    


""" esta funcion estoy pensando en no usarla:"""
def built_in_function_maker(function_name):
    if function_name == 'uniform distribution [0, 1]':
        return random_function_maker({'type': 'random function', 'subtype': 'uniform distribution', 'interval': [0, 1]})
        #or we can write:
        #return random.uniform([0, 1])
    
    

    
"""
podemos juntar random_function_maker, outlay_function_maker, etc... en un solo metodo: function_maker
e incluirlo como metodo de la clase Ecosystem
"""
    
    
    
hunting_outlay = make_function(hunting_outlay_settings)

living_outlay = make_function(living_outlay_settings)

dying_test = make_function(dying_constraint_settings)

hunting_constraint = make_function(hunting_constraint_settings)

print hunting_outlay(organism), living_outlay(organism), dying_test(organism), hunting_constraint(organism, organism_prey)

