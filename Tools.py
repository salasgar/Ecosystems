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
    
    
    
    
    
    
