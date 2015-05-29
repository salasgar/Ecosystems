
"""      EXPERIMENT 2      """
"""

    En este experimento se dejará "rienda suelta" a la selección natural para que ella misma
configure las características de las distintas especies del ecosistema, que derivarán todas ellas
de una sola. El propio Experiment deberá ir variando los 'outlays' hasta encontrar unos valores 
para los cuales se genere un ecosistema estable que sustente una abundante biodiversidad. 
"""

ecosystem_settings = {
    'biotope': {'size': (70, 70)},
                
    'organisms': {
        'number of organisms': 1000,
        'genes': {
            'photosynthesis capacity': {'initial value': 100.0},
            'energy storage capacity': {'initial value': 10000.0},
            'energy reserve procreating threshold': {'initial value': 2000.0},
            'energy reserve at birth': {'initial value': 1000.0},
            'mutation frequency': {'initial value': 0.01},
            'move?': {'randbool': 'moving frequency'},
            'procreate?': {'>': ('energy reserve', 'energy reserve procreating threshold')}, 
            'hunt?': {'randbool': 'aggressiveness'},
            'color': (
                {'comment': 'RED component',
                '*': (
                    255,
                    {'function': 'sigmoid',
                        'parameter': 'attack capacity',
                        'translation': -50.0,
                        'homothety':  0.2
                    })},

                {'comment': 'GREEN component',
                '*': (
                    255,
                    {'function': 'sigmoid',
                        'parameter': 'photosynthesis capacity',
                        'translation': -1.0,
                        'homothety':  0.01
                    })},

                {'comment': 'BLUE component',
                '*': (
                    255,
                    {'function': 'sigmoid',
                        'parameter': 'mutation frequency',
                        'translation': -5.0,
                        'homothety':  3
                    })})},
        'status': {},
        'mutabilities': {
            ('speed',
            'moving frequency',
            'attack capacity',
            'aggressiveness',
            'hunt radius',
            'defense capacity', 
            'photosynthesis capacity',
            'energy storage capacity',
            'energy reserve procreating threshold',
            'energy reserve at birth',
            'radius of procreation',
            'mutation frequency',
            'indicator gene A',
            'indicator gene B'): {
                'will mutate?': {'randbool': 'mutation frequency'},
                'percentage variation': {'uniform': [-0.01, 0.01]},
                'allowed interval': [0, 'infinity'] }},
        'initial values': {
            ('speed',
            'hunt radius',
            'radius of procreation'): 1.5,
            ('attack capacity',
            'aggressiveness',
            'defense capacity',
            'indicator gene A',
            'indicator gene B'): 0.1,
            'energy reserve': 1000},

     'constraints': {
        'kill?': {'>': (
                {'*': ({'predator': 'attack capacity'}, {'function': 'gaussian'})},
                {'*': ({'prey': 'defense capacity'}, {'function': 'gaussian'})} )},         
        'die?': {'or': (
                {'<': ('energy reserve', 50.0)},
                {'randbool': 0.001} )} },
            
    'outlays': {
        'hunt': {'energy reserve': {
            '+': (
                {'*': (0.3, 'attack capacity')}, 
                {'*': (0.2, 'speed')},
                0.1)}},         
        'move': {'energy reserve': {
            '+': (
                {'*': ('photosynthesis capacity', 0.005)}, 
                {'*': ('speed', 0.08)}, 
                {'*': ('energy reserve', 0.05)},
                {'*': ('energy storage capacity', 0.002)}, 
                0.1)}},
        'procreate': {'energy reserve': {
            '+': (
                {'*': ('attack capacity', 0.8)}, 
                {'*': ('photosynthesis capacity', 0.3)}, 
                {'*': ('speed', 0.1)}, 
                0.05)}},
        'stay alive': {'energy reserve': {
            '+': (
                {'*': ('attack capacity', 0.3)}, 
                {'*': ('photosynthesis capacity', -0.01)},
                {'*': ('energy storage capacity', 0.002)}, 
                {'*': ('energy reserve', 0.05)},
                {'*': ('speed', 0.2)}, 
                0.1)}}}       
}
  





