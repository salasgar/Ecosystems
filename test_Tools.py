
from Tools import *
from math import *

test1 = False # class Matrix
test2 = False # prod, float_range
test3 = False # make_function, merge_dictionaries
test4 = False
test5 = False
test6 = False
test7 = True


if test1:
    print """\n\n TEST class Matrix """

    matrix = Matrix(3, 5, "hello!")
    print matrix

    size = (3, 5)

    matrix = Matrix(*size)
    print matrix

    matrix = Matrix(*size, value = "bye!")  # Matrix(*size, "bye!") gives error. Only named arguments may follow *expression
    print matrix

if test2:
    organism = {'strength': 2.0, 
            'speed': 3.0,
            'procreating frequency': 0.3,
            'attack capacity': 5.0,
            'defense capacity': 4.0,
            'photosynthesis capacity': 10.0,
            'age': 120,
            'procreate?': {'randbool': 0.8},
            'energy reserve': 15.0}   
    function_settings = {'number of organisms': 2, 'predator': 'speed'}
    f = make_function(function_settings)    
    print f(organism, organism)
    function_settings = {'number of organisms': 2,
                '>': (
                    {'*': ({'predator': 'attack capacity'}, {'gauss': (0, 1)})},
                     {'*': ({'prey': 'defense capacity'}, {'gauss': (0, 1)})} )}        
    f = make_function(function_settings)    
    print f(organism, organism)

if test3: 
    print """\n\n TEST make_function(function_settings) """

    living_outlay_dict = {
		'+': [
			{'*': ['attack capacity', 'defense capacity', 1.0]}, 
                  	{'*': ['photosynthesis capacity', -1.0]},
			{'*': ['attack capacity', 'photosynthesis capacity', 25.0]}, 
			0.5]} 

    organism = {'strength': 2.0, 
            'speed': 3.0,
            'procreating frequency': 0.3,
            'attack capacity': 5.0,
            'defense capacity': 2.0,
            'photosynthesis capacity': 10.0,
            'age': 120,
            'procreate?': {'randbool': 0.8},
            'energy reserve': 15.0}    

    function0_settings = organism['procreate?']   
    
    function0 = make_function({'randbool': 0.8})
    #function0 = lambda probability_of_True: (probability_of_True > random())
    print function0(organism)
    
    function1 = {'gauss': 
        ('age', 
        {'uniform': [
            'photosynthesis capacity', 
            'energy reserve']})}  
    print [make_function(function1)(organism) for i in range(10)]    
    print make_function(living_outlay_dict)(organism)   
   
    print " TEST merge_dictionaries "
    A = {1: 'a',
     2: {
         1: 'a',
         2: {1: 'a',
             2: 'b'}
     }}
     
    B = {1: 'fail',
     2: {
         1: {1: 'fail'},
         2: {2: 'fail',
             'ok': 'ok'}},
     3: 'ok'}
     
    merge_dictionaries(dictionary_to_be_completed = A, dictionary_to_complete_with = B)
    print_dictionary(A)    
    
if test4:
    
    f = lambda x: x**2
    
    organism_settings = {
        'strength': 3,
        'gene A': f,
        'gene B': {'call': f, 'x': 7},
        'gene C': {'call': 'gene A', 'x': 'strength'},
        'f': {'**': ('x', 2), 'function of': 'x'},
        'g': {'**': ('a', 'strength'), 'function of': 'a', 'allowed interval': [1, 20]},
        'gene D': {'call': 'g', 'a': 3},
        'abscissas': [3, 5, 10],
        'ordinates': [1, -1, 0],
        'interp': {'function': 'SPLINE',
                   'abscissas': 'abscissas',
                   'ordinates': 'ordinates',
                   'function of': 'x'},
        'monomial': {'*': (5, 'x', 'y'), 'function of': ('x', 'y')}
    }
    
    organism = dict((gene, make_function(gene, 1)) for gene in organism_settings)    
    
    print organism['strength']          # output: 3
    print organism['gene A'](6)         # output: 6**2 = 36
    print organism['gene B'](organism)  # output: 7**2 = 49
    print organism['gene C'](organism)  # output: 3**2 = 9
    print organism['f'](organism)(5)    # output: 5**2 = 25
    print organism['g'](organism)(3)    # output: 3**3 = 27 --> 20  (allowed interval: [1, 20])
    print organism['gene D'](organism)  # output: 3**3 = 27 --> 20  (allowed interval: [1, 20])    
    print organism['interp'](organism)(4)  # output: 0    
    print organism['monomial'](organism)(2, 3)  # output: 5*2*3 = 30
    
    
if test5:

    compare_functions = lambda f1, f2, x: (f1(x) > f2(x))
    
    ecosystem_settings_ = {
        'organisms': {
            ('attack capacity vertexes', 
            'defense capacity vertexes'): {
                'initial value': {'tuple': ((0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1))},
                'mutability': {} },
            'attack capacity': {
                'function': 'SPLINE',
                'vertexes': 'attack capacity vertexes',
                'function of': 'x',
                'domain': [0, 5]},
            'defense capacity': {
                'function': 'SPLINE',
                'vertexes': 'defense capacity vertexes',
                'function of': 'x',       
                'domain': [0, 5]} },
        'constraints': {
            'kill?': {
                'call': 'compare functions',
                'f1': {'predator', 'attack capacity'},
                'f2': {'prey', 'defense capacity'},
                'x': {'gauss': (4, 0.5),
                      'allowed interval': [0, 5]}} } } 
    
    
if test6:
    organism_settings = {'strength': 2.0, 
            'speed': 3.0,
            'procreating frequency': 0.3,
            'mutate frequency': 0.2,
            'attack capacity': 5.0,
            'defense capacity': 2.0,
            'photosynthesis capacity': 10.0,
            'age': 120,
            'procreate?': {'randbool': 0.8},
            'energy reserve': 15.0,
            'actions sequence': {
                'initial value': [
                    'move',
                    'hunt',
                    'interchange substances with the biotope',
                    'interchange substances with other organisms',
                    'fertilize',
                    'do internal changes',
                    'stay alive',
                    'procreate'],
                'mutability': {
                    'will mutate?': {'randbool': 'mutate frequency'},
                    'new value': {'shuffle': 'actions sequence'}                
                    }}}
    organism = {} 
    for item in organism_settings:
        if isinstance(organism_settings[item], dict) and 'initial value' in organism_settings[item]:
            ivg = make_function(organism_settings[item]['initial value'], 1)
            if is_function(ivg):            
                organism[item] = ivg(organism)
            elif hasattr(ivg, '__iter__'):   
                organism[item] = [sub_item(organism) for sub_item in ivg]
            else:
                organism[item] = ivg
        else:
            organism[item] = organism_settings[item]

    mutability = {
        'will mutate?': make_function(organism_settings['actions sequence']['mutability']['will mutate?'], 1),                    
        'new value': make_function(organism_settings['actions sequence']['mutability']['new value'], 1)}
        
    print "mutability['will mutate?'] =", mutability['will mutate?'](organism)
    print "mutability['new value'] =", mutability['new value'](organism)

if test7:
    from Organism import *
    
    organism_settings = {
            'speed': 3.0,
            'attack capacity': 5.0,
            'defense capacity': 2.0,
            'photosynthesis capacity': 10.0,
            'age': 120,    
            'color': ['speed', 7, {'+': ('speed', 100)}]
    }
    
    all_genes = extract_genes_names(organism_settings)
    organism = Organism({}, {})
    for gene in organism_settings:
        organism.add_gene(gene, organism_settings[gene], all_genes)
    
    print_dictionary( organism)
                    
    color = make_function(organism_settings['color'])
    print color(organism)
    print organism['color'](organism)