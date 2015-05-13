from Tools import *
from copy import *

print type("c")


def make_function(definition):
    if is_number(definition):
        return lambda organism: definition

definition = 9

print type(definition) == str

print isinstance(definition, str)

print sqrt(25)

make_copy = lambda definition: (definition + 1) 

A = lambda: make_copy(definition)

definition = 47

print A()

B = [lambda: i for i in range(9)]

print [B[i]() for i in range(9)]

cosa(*jdfda, ekjf)