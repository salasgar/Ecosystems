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

def make_function(definition):
    if is_number(definition):
        return lambda organism: definition
    elif isinstance(definition, str):
        return lambda organism: organism[definition]
    elif isinstance(definition, dict):
        if 'type' in definition.keys():
            # RANDOM FUNCTIONS:
            if definition['type'] == 'random function':
                if definition['subtype'] == 'gaussian':
                    mean = make_function(definition['mean'])
                    variance = make_function(definition['variance'])
                    return lambda organism: random.gauss(mean(organism), variance(organism))
                elif definition['subtype'] == 'uniform distribution':
                    a = make_function(definition['interval'][0])
                    b = make_function(definition['interval'][1])
                    return lambda organism: random.uniform(a(organism), b(organism))
                elif definition['subtype'] == 'discrete distribution':
                    def choice_value(values, r):
                        i = 0
                        while r > values[i]['probability']:
                            i += 1
                        return values[i]['value']
                    values = copy.deepcopy(definition['values'])
                    total = 0
                    for pair in values:
                        total += pair['probability']
                        pair['probability'] = total
                    return lambda organism: choice_value(values, random.random())
                elif definition['subtype'] == 'chi-squared distribution':
                    coefficient = make_function(definition['coefficient'])
                    k = make_function(definition['k'])
                    return lambda organism: coefficient(organism) * math.fsum(random.gauss(0, 1)**2 for i in range(k(organism)))
                else:
                    return lambda organism: random.random()
             
            # OUTAY FUNCTIONS:
            elif definition['type'] == 'outlay function':
                if definition['subtype'] == 'linear function':
                    independent_term = 0
                    dependent_terms = []
                    for term in definition['terms']:
                        if term['parameter'] == None:
                            independent_term = make_function(term['coefficient'])
                        else:
                            dependent_terms.append((term['parameter'], make_function(term['coefficient'])))
                    return lambda organism: sum([(organism[parameter] * coefficient(organism)) for (parameter, coefficient) in dependent_terms], independent_term(organism))
                elif definition['subtype'] == 'n-linear function':
                    terms = [(term['parameters'], make_function(term['coefficient'])) for term in definition['terms']]
                    return lambda organism: sum([(prod([organism[parameter] for parameter in parameters])*coeficient(organism)) for (parameters, coeficient) in terms])
                return lambda organism: 0
                
                # CONSTRAINT FUNCTIONS:
                if function_dict['type'] == 'constraint function':
                    if function_dict['subtype'] == 'thresholds':
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
                        if len(function_dict['terms']) == 0:
                            return 'Error in constraint function from input data'
                        if function_dict['operator'] == 'and':
                            bool_operator = lambda x, y: (x and y)
                        elif function_dict['operator'] == 'or':
                            bool_operator = lambda x, y: (x or y)
                        else:
                            bool_operator = lambda x, y: logical_xor(x, y)
                        terms = [make_term(term) for term in function_dict['terms']]
                        return lambda organism: reduce(bool_operator, [term(organism) for term in terms[1:]], terms[0](organism))    
                    elif function_dict['subtype'] == 'hunting':
                        if is_number(function_dict['predator value']):
                            predator_value = lambda predator: function_dict['predator value']
                        elif isinstance(function_dict['predator value'], dict):
                            predator_value = random_function_maker(function_dict['predator value'])
                        else:
                            predator_value = lambda predator: predator[function_dict['predator value']]
            
                        return lambda predator, prey: True or False  # To do
                        pass




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
    
def constraint_function_maker(function_dict):
    if function_dict['type'] == 'constraint function':
        if function_dict['subtype'] == 'thresholds':
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
            if len(function_dict['terms']) == 0:
                return 'Error in constraint function from input data'
            if function_dict['operator'] == 'and':
                bool_operator = lambda x, y: (x and y)
            elif function_dict['operator'] == 'or':
                bool_operator = lambda x, y: (x or y)
            else:
                bool_operator = lambda x, y: logical_xor(x, y)
            terms = [make_term(term) for term in function_dict['terms']]
            return lambda organism: reduce(bool_operator, [term(organism) for term in terms[1:]], terms[0](organism))    
        elif function_dict['subtype'] == 'hunting':
            if is_number(function_dict['predator value']):
                predator_value = lambda predator: function_dict['predator value']
            elif isinstance(function_dict['predator value'], dict):
                predator_value = random_function_maker(function_dict['predator value'])
            else:
                predator_value = lambda predator: predator[function_dict['predator value']]
            
            return lambda predator, prey: True or False  # To do
            pass

def random_function_maker(function_dict):
    def choice_value(values, r):
        i = 0
        while r > values[i]['probability']:
            i += 1
        return values[i]['value']   
    if function_dict['type'] == 'random function':
        if function_dict['subtype'] == 'gaussian':
            mean = function_dict['mean']
            variance = function_dict['variance']
            return lambda: random.gauss(mean, variance)
        elif function_dict['subtype'] == 'uniform distribution':
            interval = function_dict['interval']
            return lambda: random.uniform(*interval)
        elif function_dict['subtype'] == 'discrete distribution':
            values = copy.deepcopy(function_dict['values'])
            total = 0
            for pair in values:
                total += pair['probability']
                pair['probability'] = total
            return lambda: choice_value(values, random.random())
        elif function_dict['subtype'] == 'chi-squared distribution':
            k = function_dict['k']
            coefficient = function_dict['coefficient']
            return lambda: coefficient * math.fsum(random.gauss(0, 1)**2 for i in range(k))
    return lambda: random.random()

""" esta funcion estoy pensando en no usarla:"""
def built_in_function_maker(function_name):
    if function_name == 'uniform distribution [0, 1]':
        return random_function_maker({'type': 'random function', 'subtype': 'uniform distribution', 'interval': [0, 1]})
        #or we can write:
        #return random.uniform([0, 1])
    
    
def outlay_function_maker(function_dict):
    if function_dict['type'] == 'outlay function':
        if function_dict['subtype'] == 'linear function':
            independent_term = 0
            dependent_terms = []
            for term in function_dict['terms']:
                if term['parameter'] == None:
                    independent_term = term['coefficient']
                else:
                    dependent_terms.append((term['parameter'], term['coefficient']))
            return lambda organism: sum([(organism[parameter] * coefficient) for (parameter, coefficient) in dependent_terms], independent_term)
        elif function_dict['subtype'] == 'n-linear function':
            return lambda organism: sum([(prod([organism[parameter] for parameter in term['parameters']])*term['coefficient']) for term in function_dict['terms']])
    return lambda organism: 0

def constraint_function_maker(function_dict):
    if function_dict['type'] == 'constraint function':
        if function_dict['subtype'] == 'thresholds':
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
            if len(function_dict['terms']) == 0:
                return 'Error in constraint function from input data'
            if function_dict['operator'] == 'and':
                bool_operator = lambda x, y: (x and y)
            elif function_dict['operator'] == 'or':
                bool_operator = lambda x, y: (x or y)
            else:
                bool_operator = lambda x, y: (x or y) # buscar operador xor en python
            terms = [make_term(term) for term in function_dict['terms']]
            return lambda organism: reduce(bool_operator, [term(organism) for term in terms[1:]], terms[0](organism))    
        elif function_dict['subtype'] == 'hunting':
            
            
            return lambda predator, prey: True or False  # To do
            pass

    
"""
podemos juntar random_function_maker, outlay_function_maker, etc... en un solo metodo: function_maker
e incluirlo como metodo de la clase Ecosystem
"""
    
    
    
hunting_outlay = outlay_function_maker(hunting_outlay_dict)

living_outlay = outlay_function_maker(living_outlay_dict)

dying_test = constraint_function_maker(dying_constraint_dict)

hunting_constraint = constraint_function_maker(hunting_constraint_dict)

print hunting_outlay(organism), living_outlay(organism), dying_test(organism), hunting_constraint(organism, organism_prey)

