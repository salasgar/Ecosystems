from Tools import *

print type("c")


def make_function(definition):
    if is_number(definition):
        return lambda organism: definition

definition =9

print type(definition) == str

print isinstance(definition, str)

print sqrt(25)