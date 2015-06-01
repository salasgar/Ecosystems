
"""      EXPERIMENT 2      """
"""

    En este experimento se dejará "rienda suelta" a la selección natural para que ella misma
configure las características de las distintas especies del ecosistema, que derivarán todas ellas
de una sola. El propio Experiment deberá ir variando los 'outlays' hasta encontrar unos valores 
para los cuales se genere un ecosistema estable que sustente una abundante biodiversidad. 
"""

               


COMENTARIO PARA EMILIO:

Sólo una cosa más para cuando leas este ecosystem_settings:

Con el programa tal y como lo tenemos ahora, un usuario podría poner, por ejemplo, 
lo siguiente (aunque no sería muy recomendable):
    ('gen A', 'gen B'): {'initial value': 8},
    ('gen B', 'gen C'): {'mutability': {'new value': 0}},
    'gen C': 14
y significaría que les ha dado un valor inicial a 'gen A' y 'gen B',
ha definido una mutabilidad para 'gen B' y 'gen C' y un valor inicial para gen C.
Es decir, que un mismo gen puede aparecer varias veces en la definición y se
van agregando cosas a su definición. Hacerlo así es una guarrada. Pero eso DEPENDE 
DEL USUARIO, que sea un guarro o no. Es decir, en este ejemplo lo mejor que podría 
haber hecho el usuario es definirlo así, que también lo entendería nuestro programa 
ahora mismo:
    'gen A': 8,
    'gen B': {
        'initial value': 8,
        'mutability': {'new value': 0}
        },
    'gen C': {
        'initial value': 14,
        'mutability': {'new value': 0} 
        }
Lo de agrupar genes para definirlos todos a la vez solo es para evitar redundancias.
Si al usuario no le gusta hacer eso, pues que no lo haga. Siempre puede hacer "copy-paste"
y repetir un montón de veces la misma mutabilidad para un montón de genes.

Intenta crear un ecosystem_settigs que haga exactamente lo mismo que el siguiente
pero que tenga una sintaxis que consideres más clara:


ecosystem_settings = {
    'biotope': {'size': (100, 100)},
                
    'organisms': {
        'number of organisms': 200,
        'genes': {
            'age': {
                'initial value': 0,
                'variability': {'new value': {'+': ('age', 1)}},
                'mutability': {
                    '&will mutate?': {'>': ('age', 1000)},
                    'new value': 0} },
            'photosynthesis capacity': {'initial value': {'uniform': [0, 3000]}},
            'energy storage capacity': {'initial value': {'uniform': [0, 20000]}},
            'energy reserve procreating threshold': {'initial value': {'uniform': [0, 3000]}},
            'energy reserve at birth': {'initial value': {'uniform': [0, 1000]}},
            'speed': {'initial value': {'uniform': [0, 4]}},
            'hunt radius': {'new value': 1.1},
            'radius of procreation': 1.5,
            'attack capacity': {'initial value': {'uniform': [0, 20]}},
            'defense capacity': {'initial value': {'uniform': [0, 20]}},
            'aggressiveness': {'initial value': {'uniform': [0, 1]}},
            'indicator gene A': 1.0,
            'indicator gene B': 1.0,
            'energy reserve': {
                'initial value': 10000.0,
                'variability': {
                    'new value': {'+': ('energy reserve',
                                        'photosynthesis capacity')},
                    'allowed interval': [0, 'energy storage capacity']
                    }},
            'mutation frequency': {'initial value': {'uniform': [0, 1]}},
            'moving frequency': {'initial value': {'uniform': [0, 1]}},
            'procreating frequency': {'initial value': {'uniform': [0, 1]}},
            '&actions sequence': {
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
            'mutation frequency',
            'indicator gene A',
            'indicator gene B'): {
                'mutability': {
                    'will change?': {'randbool': 'mutation frequency'},
                    'percentage variation': {'uniform': [-0.05, 0.05]},
                    'allowed interval': [0, 'infinity'] }},            
            
            'color': [
                {'comment': 'RED component',
                '+': (
                    20, {
                    'roundint': {
                        '*': (
                            200,
                            {'function': 'sigmoid',
                             'parameter': 'attack capacity',
                             'translation': -5.0,
                             'homothety':  0.5
                    })}})},

                {'comment': 'GREEN component',
                '+': (
                    20, {
                    'roundint': {
                         '*': (
                             200,
                             {'function': 'sigmoid',
                              'parameter': 'photosynthesis capacity',
                              'translation': -5.0,
                              'homothety':  0.005
                    })}})},

                {'comment': 'BLUE component',
                '+': (
                    20, {
                    'roundint': {
                        '*': (
                             200,
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
            'hunt?': {'randbool': 'aggressiveness'}
            
                
            }},

     'constraints': {
        'can kill?': {'number of organisms': 2,
                '>': (
                    {'predator': 'attack capacity'}, 
                    {'prey': 'defense capacity'} )},         
        'die?': {'or': (
                {'<': ('energy reserve', 100.0)},
                {'randbool': 0.0005} )},
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


""" A VARIATION OF THE PREVIOUS EXAMPLE: """
from Tools import *
ecosystem_settings2 = deep_copy_of_a_dictionary(ecosystem_settings)
ecosystem_settings2['constraints']['die?'] = {'or': (
                {'<': ('energy reserve', 100.0)},
                {'randbool': 0.03} )}
ecosystem_settings2['outlays']['procreate'] = {'energy reserve': {
            '+': (
                'energy reserve at birth',
                {'*': ('attack capacity', 'defense capacity', 9.0)}, 
                {'*': ('photosynthesis capacity', 1.0)}, 
                {'*': ('speed', 0.1)}, 
                200)}}
ecosystem_settings2['organisms']['genes']['color'][2] = {'comment': 'BLUE component',
                '+': (
                    20, {
                    'roundint': {
                        '*': (
                             200,
                             {'function': 'sigmoid',
                              'parameter': 'defense capacity',
                              'translation': -5.0,
                              'homothety':  0.5
                    })}})}
ecosystem_settings2[('speed',
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
            'mutation frequency',
            'indicator gene A',
            'indicator gene B')] = {
                'mutability': {
                    'will change?': {'randbool': 'mutation frequency'},
                    'percentage variation': {'uniform': [-0.07, 0.07]},
                    'absolute variation': {'uniform': [-0.3, 0.3]},
                    'allowed interval': [0, 'infinity'] }}
ecosystem_settings2['biotope']['size'] = (200, 200)
""" este ecosistema, cuando madura, se hace estable y biodiverso """


ecosystem_settings3 = deep_copy_of_a_dictionary(ecosystem_settings2)

ecosystem_settings3[('speed',
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
            'mutation frequency',
            'indicator gene A',
            'indicator gene B')] = {
                'mutability': {
                    'will change?': {'randbool': 'mutation frequency'},
                    'percentage variation': {'gauss': [0, 0.07]},
                    'absolute variation': {'gauss': [0, 0.3]},
                    'allowed interval': [0, 'infinity'] }}




"""            
            
            ,
            'attack?': {'number of organisms': 2,
                '>': (
                    {'distance': (
                        {'predator': 'family mark'},
                        {'prey': 'family mark'})},
                    'consanguinity threshold')}
                    
"""
