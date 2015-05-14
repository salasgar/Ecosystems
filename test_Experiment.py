from Experiment import experiment
from Tools import *


hunting_outlay_definition = {
          'type': 'outlay function',
          'subtype': 'linear function',
          'terms': [
              {'parameter': 'strength', 'coefficient': 3.0}, 
              {'parameter': 'speed', 'coefficient': 0.2}, 
              {'parameter': None, 'coefficient': 5.0}]}

living_outlay_definition = {
		'type': 'outlay function',
		'subtype': 'n-linear function',
		'terms': [
			{'parameters': ['attack capacity', 'defense capacity'], 		'coefficient': 1.0}, 
                  	{'parameters': ['photosynthesis capacity'], 				'coefficient': -1.0},
			{'parameters': ['attack capacity', 'photosynthesis capacity'], 	'coefficient': 25.0}, 
			{'parameters': [], 								'coefficient': 0.5}]} 
   
dying_constraint_definition = {
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
  
hunting_constraint_definition = {
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
print make_function(living_outlay_definition)(organism)   
    


""" esta funcion estoy pensando en no usarla:"""
def built_in_function_maker(function_name):
    if function_name == 'uniform distribution [0, 1]':
        return random_function_maker({'type': 'random function', 'subtype': 'uniform distribution', 'interval': [0, 1]})
        #or we can write:
        #return random.uniform([0, 1])
    
    
def outlay_function_maker(function_definition):
    if function_definition['type'] == 'outlay function':
        if function_definition['subtype'] == 'linear function':
            independent_term = 0
            dependent_terms = []
            for term in function_definition['terms']:
                if term['parameter'] == None:
                    independent_term = term['coefficient']
                else:
                    dependent_terms.append((term['parameter'], term['coefficient']))
            return lambda organism: sum([(organism[parameter] * coefficient) for (parameter, coefficient) in dependent_terms], independent_term)
        elif function_definition['subtype'] == 'n-linear function':
            return lambda organism: sum([(prod([organism[parameter] for parameter in term['parameters']])*term['coefficient']) for term in function_definition['terms']])
    return lambda organism: 0

def constraint_function_maker(function_definition):
    if function_definition['type'] == 'constraint function':
        if function_definition['subtype'] == 'thresholds':
            def make_term(term):
                if term['operator'] == '>':
                    compare = lambda x, y: (x > y)
                elif term['operator'] == '<':
                    compare = lambda x, y: (x < y)
                else:
                    return 'error: unknown operator ' + term['operator']
                if 'threshold' in term.keys():
                    threshold = lambda: term['threshold']
                elif 'random threshold' in term.keys():
                    threshold = random_function_maker(term['random threshold'])
                return lambda organism: compare(organism[term['parameter']], threshold())
            if len(function_definition['terms']) == 0:
                return 'Error in constraint function from input data'
            if function_definition['operator'] == 'and':
                bool_operator = lambda x, y: (x and y)
            elif function_definition['operator'] == 'or':
                bool_operator = lambda x, y: (x or y)
            else:
                bool_operator = lambda x, y: (x or y) # buscar operador xor en python
            terms = [make_term(term) for term in function_definition['terms']]
            return lambda organism: reduce(bool_operator, [term(organism) for term in terms[1:]], terms[0](organism))    
        elif function_definition['subtype'] == 'hunting':
            
            
            return lambda predator, prey: True or False  # To do
            pass

    
"""
podemos juntar random_function_maker, outlay_function_maker, etc... en un solo metodo: function_maker
e incluirlo como metodo de la clase Ecosystem
"""
    
    
    
hunting_outlay = outlay_function_maker(hunting_outlay_definition)

living_outlay = outlay_function_maker(living_outlay_definition)

dying_test = constraint_function_maker(dying_constraint_definition)

hunting_constraint = constraint_function_maker(hunting_constraint_definition)

print hunting_outlay(organism), living_outlay(organism), dying_test(organism), hunting_constraint(organism, organism_prey)

