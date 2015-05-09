from random import random


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
        if function_dict['name'] == 'gaussian':
            mean = function_dict['mean']
            variance = function_dict['variance']
            return lambda: random.gauss(mean, variance)
        elif function_dict['name'] == 'uniform distribution':
            interval = function_dict['interval']
            return lambda: random.uniform(*interval)
        elif function_dict['name'] == 'discrete distribution':
            values = copy.deepcopy(function_dict['values'])
            total = 0
            for pair in values:
                total += pair['probability']
                pair['probability'] = total
            return lambda: choice_value(values, random.random())
        elif function_dict['name'] == 'chi-squared distribution':
            k = function_dict['k']
            coefficient = function_dict['coefficient']
            return lambda: coefficient * math.fsum(random.gauss(0, 1)**2 for i in range(k))
    return lambda: random.random()
    
