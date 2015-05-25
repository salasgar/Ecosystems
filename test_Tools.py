
from Tools import *
from math import *

test1 = False # class Matrix
test2 = False # prod, float_range
test3 = False # make_function, merge_dictionaries

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
    print """\n\n TEST prod(iterable) """

    print prod([3, 4, 5]) # gives de product of all numbers in an iterable object:  3 * 4 * 5 = 60

    print """\n\n TEST float_range(start, stop, step) """
    for x in float_range(12, 11, -0.11):
        print x

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
            'attack capacity': 5.0,
            'defense capacity': 2.0,
            'photosynthesis capacity': 10.0,
            'age': 120,
            'energy reserve': 15.0}    
            
    function1 = {
        'function': 'gaussian',
        'mean': 'age',
        'variance': {
            'function': 'uniform distribution',
            'interval': ['photosynthesis capacity', 'energy reserve']}}  
    print [make_function(function1, number_of_arguments = 1)(organism) for i in range(10)]    
    print make_function(living_outlay_dict, number_of_arguments = 1)(organism)   
   
    print """ TEST merge_dictionaries """
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
   
    