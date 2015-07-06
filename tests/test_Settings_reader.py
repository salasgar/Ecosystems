from Settings_reader import *

# THIS IS ONLY FOR TESTING:
test_organism = {'strength': 2.0,
                 'speed': 3.0,
                 'procreating frequency': 0.3,
                 'attack capacity': 5.0,
                 'defense capacity': lambda organism: 100 - organism['attack capacity'],
                 'photosynthesis capacity': 10.0,
                 'age': 770,
                 'procreate?': {'randbool': 0.8},
                 'energy reserve': 15.0,
                 'energy storage capacity': 1000,
                 'test': 0}

test_organism_2 = {'strength': 2.0,
                 'speed': 3.0,
                 'procreating frequency': 0.3,
                 'attack capacity': 5.0,
                 'defense capacity': lambda organism: 100 - organism['attack capacity'],
                 'photosynthesis capacity': 10.0,
                 'age': 18,
                 'procreate?': {'randbool': 0.8},
                 'energy reserve': 15.0,
                 'energy storage capacity': 1000,
                 'test': 0}

"""
for gene in ['energy reserve', 'strength', 'A', 'B', 'C', 'speed', 'photosynthesis capacity', 'energy storage capacity', 'attack capacity', 'defense capacity', 'procreating frequency', 'age', 'test', 'procreate?']:
    print gene, '-->', get_gene_value_or_string(test_organism, gene)


expr_list = [
    'energy reserve', 
    'string value', 
    'age', 
    '#prey age', 
    '#predator age',
    '#some_data',
    '#prey']

for expression in expr_list:
    f = evaluate_string(expression, ['#predator', '#prey', '#some_data'])
    print expression, '-->', f(test_organism, test_organism_2, 3.14159265)

"""
example_functions_settings = {

    'function a': {'+': (
        {'uniform': [3, 5]},
        {'*': (
            {'randint': [6, 9]},
            1000
        )},
        1000000
    )},

    'function a2': {'+': (
        {'uniform': [3, 5]},
        {'*': (
            {'randint': [6, 9]},
            1000
        )},
        {'*': ('age', 1000000)}
    )},

    'function a3': 'age',

    'function b3 #x #y #z': {'+': (1, '#x')},

    'function b2 #x #y #z': ('#z', '#x'),

    'function b #x #y #z': {'+': (
        {'*': (3, '#x')},
        {'*': (2, '#y')},
        {'*': (5, '#z')}
    )},

    'function c #organism': {'+': (
        {'sqrt': 2},
        '#organism age'
    )}, 

    'function d': {'+': (
        'age',
        'defense capacity'
    )},

    'function e #self #other_organism': {'+': (
        'age',
        '#other_organism age'
    )},

    'function f #self #other_organism #parameter': {'+': (
        'age',
        '#other_organism age',
        '#parameter'
    )}
}

print ("*"*100 + "\n")*3


example_functions = {}

for f in example_functions_settings:
    print f, '-->', remove_tags(f) + '(', get_tags_list(f), ')'
    print example_functions_settings[f]
    example_functions[remove_tags(f)] = make_function(example_functions_settings[f], get_tags_list(f))

print 'function a() =', example_functions['function a']()
print 'function a2(test_organism) =', example_functions['function a2'](test_organism)
print 'function a3(test_organism) =', example_functions['function a3'](test_organism)
print 'function b3(1000, 100, 10) =', example_functions['function b3'](1000, 100, 10)
print 'function b2(1000, 100, 10) =', example_functions['function b2'](1000, 100, 10)
print 'function b(1000, 100, 10) =', example_functions['function b'](1000, 100, 10)
print 'function c(test_organism) =', example_functions['function c'](test_organism)
print 'function d(test_organism) =', example_functions['function d'](test_organism)
print 'function e(test_organism, test_organism_2) =', example_functions['function e'](test_organism, test_organism_2)
print 'function f(test_organism, test_organism_2, 3.14159) =', example_functions['function f'](test_organism, test_organism_2, 3.14159)



