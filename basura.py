# -*- coding: utf-8 -*-
"""
Created on Tue May 12 02:52:25 2015

@author: JuanLuis
"""

print type("c")


def make_function(definition):
    if is_number(definition):
        return lambda organism: definition

definition =9

print type(definition) == str

print isinstance(definition, str)
