

""" In this file we define some features of an ecosystem, to provide the user of built-in components
that he may want to combine to form his 'ecosystem_setings'. For example, like this:


ecosystem_settings = {
    'biotope': {{'load': 'basic biotope 3'},
                'size': (100, 100)},
    'organisms': [
        {
            'category': 'simple plants',
            {'load': 'doing photosynthesis 1'},
            {'load': 'procreating 1'}
        },
        
        {
            'category': 'complex plants',
            {'load': 'doing photosynthesis 2'},
            {'load': 'procreating in a strange way'}
        }
        
        ]
    }


"""

parts_of_organisms_settings = {
    'doing phtonosynthesis 1': {
        'genes': {
            'photosynthesis capacity': {'uniform': [0, 500]}},
        'status': {        
            'energy reserve': {
                'initial value': 10000,
                'modifying': {
                    'new value': {'+': ('energy reserve', 'photosynthesis capacity')}}} }},
                                  
    'doing phtonosynthesis 2': {
        'genes': {
            'photosynthesis capacity': {
                'initial value': {'uniform': [0, 500]},
                'mutability':{
                    'will mutate?': {'randbool': 'photosynthesis capacity mutation probability'},
                    'percentage variation': {'gauss': (0.0, 0.1), 'allowed interval': [-1, 2]},
                    'allowed interval': [0, 'infinity']
                    }},
            'photosynthesis capacity mutation probability': 0.01},
        'status': {        
            'energy reserve': {
                'initial value': 10000,
                'modifying': {
                    'new value': {'+': (
                        'energy reserve', 
                        {'gauss': ('photosynthesis capacity', 10.0)})}} }}}
    # to do: Add more built-in settings
    }
                                  
                                  