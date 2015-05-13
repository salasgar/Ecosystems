import random
from functools import reduce

def is_number(x):
    try:
        x + 1
        return True
    except TypeError:
        return False

def prod(iterable): # Calculates the product of all the elements in the iterable
    return reduce((lambda x, y: x * y), iterable, 1)

def signed_random():
    return 2*random() - 1


def create_empty_list_of_lists(size_x, size_y):
    return [[None] * size_y for i in range(size_x)]


class Matrix(object):
    data = []
    size_x = 0
    size_y = 0

    def __init__(self, size_x, size_y, value=None):
        self.data = [[value] * size_y for i in range(size_x)]
        # No usar [[None] * size_y] * size_x, ya que no hace copia profunda
        self.size_x = size_x
        self.size_y = size_y

    def __getitem__(self, coordinates):
        x, y = coordinates
        return self.data[x % self.size_x][y % self.size_y]

    def __setitem__(self, coordinates, value):
        x, y = coordinates
        self.Data[x % self.size_x][y % self.size_y] = value

    def __str__(self):
        return "\n".join(str(self.Data[i]) for i in range(len(self.Data)))

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


    
    
    
    
