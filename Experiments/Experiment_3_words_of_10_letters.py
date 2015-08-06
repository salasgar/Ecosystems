
"""                             EXPERIMENT 3                                """
"""                                                                         """
""" In this experiment we try to check weather it's evolutively good for an """
""" organism to eat its relatives. We provide a method for them to measure  """
""" their consanguinity, using a gene that we call 'indicator of            """
""" conosanguinity'. We define another gene called 'consanguinity threshold,"""
""" that indicates how genetically far away a prey has to be so that the    """
""" predator decides to attack it.                                          """
""" We have observed that the threshold increases a little, meaning that    """
""" predators prevent themselves to eat very close relatives. In order to   """
""" measure the importance of that increment, we have define another gene   """
""" that we call 'consanguinity threshold fake version', that has no effect """
""" at all in the behavior of the organisms, and we have observed that the  """
""" fluctuation of the fake gene is very similar to the one of the real one."""
""" That means that, as far as we know, in this experiment we can't proof   """
""" that it's an advantage to avoid eating relatives.                       """
""" Nevertheless, more extent and precise studies have to be done to        """
""" be sure that this gene has no effect in the survival of a species       """

               
ecosystem_settings = {
    'biotope': {'size': (100, 100)},
                
    'organisms': {
        'number of organisms': 500,
        'genes': {
            'age': {
                'initial value': 0,
                'variability': {'new value': {'+': ('age', 1)}},
                'mutability': {'new value': 0} },
            'generation': {
                'initial value': 0,
                'mutability': {'absolute variation': 1}},
            'indicator of consanguinity': { # 'family mark'
                'initial value': [{'gauss': (0, 10)}, {'gauss': (0, 10)}, {'gauss': (0, 10)}, {'gauss': (0, 10)}],
                'mutability': {
                    'new value': {'vector +': (
                        'indicator of consanguinity',
                        [{'gauss': (0, 10)}, {'gauss': (0, 10)}, {'gauss': (0, 10)}, {'gauss': (0, 10)}]
                        )},
                    'frequency': 0.5}},
            ('consanguinity threshold', 'consanguinity threshold fake version') : {
                'initial value': 0.7,
                'mutability': {'percentage variation': {'gauss': (0, 0.1)}}},
            'photosynthesis capacity': {'initial value': {'uniform': [0, 3000]}},
            'energy storage capacity': {'initial value': {'uniform': [0, 20000]}},
            'energy reserve procreating threshold': {'initial value': {'uniform': [0, 3000]}},
            'energy reserve at birth': {'initial value': {'uniform': [0, 1000]}},
            'speed': {'initial value': {'uniform': [4, 8]}},
            'hunt radius': 1.1,
            'radius of procreation': 1.5,
            'attack capacity': {'initial value': {'uniform': [0, 20]}},
            'defense capacity': {'initial value': {'uniform': [0, 2]}},
            'aggressiveness': {'initial value': {'uniform': [0, 1]}},
            'indicator gene A': 1.0,
            'indicator gene B': 1.0,
            'energy reserve': {
                'initial value': 10000.0,
                'variability': {
                    'new value': {'+': ('energy reserve', 'photosynthesis capacity')},
                    'allowed interval': [0, 'energy storage capacity']
                    }},
            'mutation frequency': {'initial value': {'uniform': [0, 1]}},
            'moving frequency': {'initial value': {'uniform': [0, 1]}},
            'procreating frequency': {'initial value': {'uniform': [0, 1]}},
            'actions sequence': {
                'initial value': [
                    'move',
                    'hunt',
                    'do internal changes',
                    'stay alive',
                    'procreate'],
                'mutability': {
                    'will change?': {'randbool': 'mutate frequency'},
                    'new value': {'shuffle': 'actions sequence'}                
                    }},
            ('speed',
            'hunt radius',
            'radius of procreation',
            'moving frequency',
            'attack capacity',
            'aggressiveness',
            'defense capacity', 
            'photosynthesis capacity',
            'energy storage capacity',
            'energy reserve procreating threshold',
            'energy reserve at birth',
            'mutation frequency'): {
                'mutability': {
                    'will change?': {'randbool': 'mutation frequency'},
                    'percentage variation': {'uniform': [-0.05, 0.05]},
                    'allowed interval': [0, 'infinity'] }},            
            
            'color': [
                {'comment': 'RED component',
                '+': (
                    50, {
                    'roundint': {
                        '*': (
                            200,
                            {'function': 'sigmoid',
                             'parameter': 'consanguinity threshold',
                             'translation': -5.0,
                             'homothety':  4
                    })}})},

                {'comment': 'GREEN component',
                '+': (
                    50, {
                    'roundint': {
                         '*': (
                             200,
                             {'function': 'sigmoid',
                              'parameter': 'consanguinity threshold fake version',
                              'translation': -5.0,
                              'homothety':  4
                    })}})},

                {'comment': 'BLUE component',
                '+': (
                    50, {
                    'roundint': {
                        '*': (
                             0,
                             {'function': 'sigmoid',
                              'parameter': 'mutation frequency',
                              'translation': -3.0,
                              'homothety':  3
                    })}})}]},

        'decisions': {
            'procreate?': {'and': (
                    {'>': ('energy reserve', 'energy reserve procreating threshold')}, 
                    {'randbool': 'procreating frequency'})},
            'move?': {'randbool': 'moving frequency'},
            'hunt?': {'randbool': 'aggressiveness'},
            'attack?': {'number of organisms': 2,
                '>': (
                    {'distance': (
                        {'predator': 'indicator of consanguinity'},
                        {'prey': 'indicator of consanguinity'})},
                    'consanguinity threshold')}
            
                
            }},

     'constraints': {
        'can kill?': {'number of organisms': 2,
                '>': (
                    {'predator': 'attack capacity'}, 
                    {'prey': 'defense capacity'} )},         
        'die?': {'or': (
                {'<': ('energy reserve', 100.0)},
                {'randbool': 0.06} )},
        'procreate?': {'>': (
                'energy reserve',
                {'+': (
                    'energy reserve at birth',
                    {'outlay': 'procreate'},
                    {'outlay': 'stay alive'}                    
                    )})}},
            
    'outlays': {
        'hunt': {'energy reserve': {
            '+': (
                {'*': (0.2, 'attack capacity', 'defense capacity', 'hunt radius')}, 
                {'*': (0.2, 'speed')},
                0.1)}},         
        'move': {'energy reserve': {
            '+': (
                {'*': ('photosynthesis capacity', 'defense capacity', 0.005)}, 
                {'*': ('speed', 0.8)}, 
                {'*': ('energy reserve', 0.005)},
                {'*': ('energy storage capacity', 0.002)}, 
                0.1)}},
        'procreate': {'energy reserve': {
            '+': (
                'energy reserve at birth',
                {'*': ('attack capacity', 'defense capacity', 8.0)}, 
                {'*': ('photosynthesis capacity', 0.8)}, 
                {'*': ('speed', 'radius of procreation', 10.0)}, 
                200)}},
        'stay alive': {'energy reserve': {
            '+': (
                {'*': ('attack capacity', 0.1)}, 
                {'*': ('attack capacity', 'photosynthesis capacity', 0.003)}, 
                {'*': ('defense capacity', 'photosynthesis capacity', 0.03)}, 
                {'*': ('photosynthesis capacity', 'photosynthesis capacity', 0.0004)},
                {'*': ('energy storage capacity', 0.005)}, 
                {'*': ('energy reserve', 0.05)},
                {'*': ('speed', 0.2)}, 
                100)}}}       
}


