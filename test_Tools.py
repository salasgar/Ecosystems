
from Tools import *

print """\n\n TEST class Matrix """

matrix = Matrix(3, 5, "hello!")
print matrix

size = (3, 5)

matrix = Matrix(*size)
print matrix

matrix = Matrix(*size, value = "bye!")  # Matrix(*size, "bye!") gives error. Only named arguments may follow *expression
print matrix

print """\n\n TEST prod(iterable) """

print prod([3, 4, 5]) # gives de product of all numbers in an iterable object:  3 * 4 * 5 = 60

print """\n\n TEST make_function(definition) """

living_outlay_dict = {
		'type': 'outlay function',
		'subtype': 'n-linear function',
		'terms': [
			{'parameters': ['attack capacity', 'defense capacity'], 		'coefficient': 1.0}, 
                  	{'parameters': ['photosynthesis capacity'], 				'coefficient': -1.0},
			{'parameters': ['attack capacity', 'photosynthesis capacity'], 	'coefficient': 25.0}, 
			{'parameters': [], 								'coefficient': 0.5}]} 

organism = {'strength': 2.0, 
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
print make_function(living_outlay_dict)(organism)   