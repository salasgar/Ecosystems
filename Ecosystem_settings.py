   
              
ecosystem_settings_stone_paper_scissors = {
    'ecosystem name': "Strength vs photosyntesis capacity",
    'biotope': { 
        'size': (70, 70),
        'featuremaps': None },
    'organisms': 
        {'number of organisms': 500,
        'genes': { 
            'weapon': {
                'initial value': {            
                    'function': 'discrete distribution',
                    'values list': (
                        {'value': 'stone', 'probability': 1.0/3},                            
                        {'value': 'paper', 'probability': 1.0/3},                            
                        {'value': 'scissors', 'probability': 1.0/3})}
                    },
            'color': {
                'choice': 'weapon',
                'stone': {'literal': (150, 20, 10)}, # brown
                'paper': {'literal': (200, 200, 200)}, # dark white
                'scissors': {'literal': (100, 100, 200)} }, # pale blue
            'procreating frequency': 0.1,
            'speed': 1.1,
            'hunt radius' : 1.1,
            'radius of procreation': 4.1,
            'actions list': ('move', 'hunt', 'procreate')}},
    'constraints': {
        'procreate?': {'<': (
                    {'function': 'uniform distribution', 'interval': [0, 1]}, 
                    'procreating frequency')},  
        'kill?': {'in': (
            {'tuple': ({'predator': 'weapon'}, {'prey': 'weapon'})},
            {'literal': (
                ('stone', 'scissors'),
                ('scissors', 'paper'),
                ('paper', 'stone') )})},
        'die?': {'function': 'random boolean', 'probability': 0.05}
                }  }
                
"""
                'mutability': {
                    'will mutate?': {
                        'choice': 'weapon',
                        'stone': 'stone mutation probability',
                        'paper': 'paper mutation probability',
                        'scissors': 'scissors mutation probability'}}                          
"""
# Default ecosystem settings		(Estos son los valores por defecto)											
         
DEFAULT_SETTINGS = {
    'ecosystem': {
        'ecosystem name': 'DEFAULT ECOSYSTEM NAME',
        'biotope': {'size': (100, 100)},
        'organisms': {'number of organisms': 1,
            'genes': {},
            'status': {}
                },
        'outlays': {},
        'constraints': {
            'procreate?': True,
            'kill?': True,
            'die?': False} },
            
    'seeking prey': {
        'hunt radius': 1.5,
        'seeking prey technique': {
            'function': 'seek random organism',
            'center': 'location',
            'radius': 'hunt radius'}                  
        },
        
    'doing photosynthesis': {
        'photosynthesis capacity': 10.0
        },
        
    'procreating': {
        'procreating frequency': 0.1  # 10%      
        },
         
    'GRAPHICS': {
        'zoom': 4,
        'color function': {
            'show biotope features': False,
            'show organisms': True,
            'organisms color function': {'function': 'default organisms color function'}
            }
        }
    }
 
OLD_DEFAULT_SETTINGS = {
    'ecosystem': {
        'ecosystem name': 'DEFAULT ECOSYSTEM NAME',
        'biotope': {'size': (100, 100)},
        'organisms': {'number of organisms': 1,
            'genes': {
                'speed': 0,
                'moving frequency': 1.0},
            'status': {
                'location': {
                    'initial value': {'function': 'seek free location'},
                    'modifying': {
                        'new value': {
                            'function': 'seek free location close to',
                            'center': 'location',
                            'radius': 'speed'},            
                        'changing frequency': 'moving frequency'}
                    }
                } },
        'outlays': {},
        'constraints': {
            'procreate?': True,
            'kill?': True,
            'die?': False} },
            
    'seeking prey': {
        'hunt radius': 1.5,
        'seeking prey technique': {
            'function': 'seek random organism',
            'center': 'location',
            'radius': 'hunt radius'}                  
        },
        
    'doing photosynthesis': {
        'photosynthesis capacity': 10.0
        },
        
    'procreating': {
        'procreating frequency': 0.1  # 10%      
        },
         
    'GRAPHICS': {
        'zoom': 4,
        'color function': {
            'show biotope features': False,
            'show organisms': True,
            'organisms color function': {'function': 'default organisms color function'}
            }
        }
    }
 

ecosystem_settings = {
    'ecosystem name': "Strength vs photosyntesis capacity",
    'biotope': { 
        'size': (60, 60),
        'featuremaps': None },
    'organisms': [
        {'category': 'Plants',
        'number of organisms': 50,
        'genes': { 
            'category': 'plant',
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
                        'parameter': 'energy reserve',
                        'translation': -5.0,
                        'homothety':  0.003
                    })}),
            'longevity': 30,
            'attack capacity': 0,
            'defense capacity': 2,
            'energy reserve procreating threshold': 600,
            'energy reserve at birth': 100,
            'procreating frequency': 0.2,
            'radius of procreation': 1.5,
            'photosynthesis capacity': { # SALAS: etc, etc....
                'initial value': {
                    'function': 'uniform distribution',
                    'interval': [300, 1000] },
                'mutability': {
                    'absolute variation': {
                        'function': 'gaussian',
                        'mean': 0.0, 
                        'variance': 0.15},
                    'mutation frequency': 0.001}  },
            'energy storage capacity': {
                'initial value': 10000.0,
                'mutability': {
                    'percentage variation': {
                        'function': 'uniform distribution',
                        'interval': [-5.0, 5.0]},
                    'mutation frequency': 0.02}},
            'speed': 0},
        'status': {
            'age': 0,
            'energy reserve': 1000.0}  },
        {'category': 'Animals',
        'number of organisms': 50,
        'genes': {
            'category': 'animal',
            'color': (
                {'comment': 'RED component',
                '*': (
                    255,
                    {'function': 'sigmoid',
                        'parameter': 'attack capacity',
                        'translation': -5.0,
                        'homothety':  2
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
                        'parameter': 'energy reserve',
                        'translation': -5.0,
                        'homothety':  0.003
                    })}),
            'longevity': 30,
            'average attack capacity': {
                'initial value': 5,
                'mutability': {
                    'absolute variation': {
                        'function': 'gaussian',
                        'mean': 0.0, 
                        'variance': 0.01},
                    'mutation frequency': 0.05,
                    'allowed interval': [0, 'infinity']}},
            'attack capacity': { # This gene is function of the organism itself:
                        'function': 'gaussian',
                        'mean': 'average attack capacity',
                        'variance': {"/": ('average attack capacity', 4.0)}},
            'hunt radius': 1.5,
            'defense capacity': 40,
            'photosynthesis capacity': 0,
            'procreating frequency': 0.2,
            'radius of procreation': 1.5,
            'energy reserve procreating threshold': 1620,
            'energy storage capacity':  5000,
            'energy reserve at birth': 300,
            'speed': 1.5
        },  
        'status': {
            'age': 0,
            'energy reserve': 5000} }
    ],
                    
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
                0.1)}}},

    'constraints': {
        'procreate?': {
            'and': (
                {'<': (
                    {'function': 'uniform distribution', 'interval': [0, 1]}, 
                    'procreating frequency')},
                {'>': (
                    'energy reserve',
                    'energy reserve procreating threshold')} )},
                    
        'kill?': {
            '>': (
                {'predator': 'attack capacity'},
                {'prey': 'defense capacity'})},
            
        'die?': {
            'or': (
                {'<': (
                    'energy reserve', 
                    10.0)},
                {'>': (
                    'age',
                    {'function': 'gaussian',
                         'mean': 'longevity',
                         'variance': 5})})}}
 }


ecosystem_settings_2	 = {
    'organisms': [
	{'category': 'Mutants',
		'genes': {
            		'strength': 'default',
                  'photosynthesis capacity': 20.0,
                 	'speed': {
				'function': 'discrete distribution',
				'value list': [
					{'value': 0.0, 'frequency': 0.25},
					{'value': 1.0, 'frequency': 0.75}]},  
			'generation': 0 ,
                   	'mutation frequency': 0.1},
		'status': {
                 	'energy reserve': 100.0} },
	{'category': 'No Mutants',
		'genes': {
            		'strength': 'default',
                   	'photosynthesis capacity': 20.0,
                 	'speed': {
				'function': 'discrete distribution',
				'value list': [
					{'value': 0.0, 'frequency': 0.25},
					{'value': 1.0, 'frequency': 0.75}]},  
			'generation': 0,
                   	'mutation frequency': 0.0},
		'status': {
                    'energy reserve': 100.0} }],
  'outlays': {
	'load outlays': "/Pepito/ecosystem_settings/cool ecosystem.eco" },
  'constraints': {},
  'mutability': {
	'strength': {
		'percentage variation': {
			'function': 'gaussian',
			'mean': 0.0, 
			'variance': 0.01},
		'mutation frequency': 0.05,
		'allowed interval': [0, 'infinity']	
		},
	'speed': {
		'type': 'probabilistic automaton',
		'states': {0.0, 1.0},
		'probabilities matrix': [
			[0.99, 0.01],
			[0.02, 0.98]] },
	'generation': {
		'variation': 1},

	'mutability': {
		'percentage variation': {
			'function': 'gaussian',
			'mean': 0.0, 
			'variance': 0.01},
		'allowed interval': [0, 1]
		}
  	}
}

# Nota: En este experimento veremos si los mutantes ganan a los no mutantes en la 
# guerra por la supervivencia 


ecosystem_settings_3 = {
    'organisms': [
	{'genes': {
            	'attack capacity': { 
			'function': 'chi-squared',
			'k': 3},
            	'defense capacity': { 
			'function': 'chi-squared',
			'k': 3},
             	'photosynthesis capacity': 20.0,
		'energy reserve at birth': 100.0,
		'minimun energy reserve at procreation': 200.0},
	'status': { 'energy reserve': 200.0} }],
'outlays': {
	'load outlays': "/Pepito/ecosystem_settings/cool ecosystem_settings 2.exp",
	'living': {
		'function': 'n-linear function',
		'terms': [
			{'*': ['attack capacity', 'defense capacity', 		 1.0]}, 
                  	{'*': ['photosynthesis capacity', 				-1.0]},
			{'*': ['attack capacity', 'photosynthesis capacity', 	25.0]}, 
			0.5]} },
'constraints': {
   	'procreating': {
		'type': 'threshold',
		'*': 'energy reserve',
		'threshold': 'minimun energy reserve at procreation'},
	'hunting': {
		'function': 'compare predator vs prey',
		'a': ('predator', 'attack capacity'),
		'b': ('prey', 'defense capacity'),
		'r1': ('random number', 'uniform distribution [0, 1]'),
		'r2': ('random number', 'uniform distribution [0, 1]'),
		'expression': "a*r1 > b*r2"  } },
  'mutability': {
	'all genes': {
		'percentage variation': {
			'function': 'gaussian',
			'mean': 0.0, 
			'variance': 0.01},
		'mutation frequency': 0.05,
		'allowed interval': [0, 'infinity']	}
	}
}

# Nota: En este experimento veremos cual es la mejor tecnica para jugar a
# piedra, papel, tijera: 

ecosystem_settings4 = {
    'constraints': {
        'hunting': {'or': (
            {'and': (
                {'==': (
                    {'predator': 'weapon'},
                    {'string': 'stone'})},      
                {'==': (
                    {'prey': 'weapon'},
                    {'string': 'scissors'})} )},
            
            {'and': (
                {'==': (
                    {'predator': 'weapon'},
                    {'string': 'scissors'})},      
                {'==': (
                    {'prey': 'weapon'},
                    {'string': 'paper'})} )},
            
            {'and': (
                {'==': (
                    {'predator': 'weapon'},
                    {'string': 'paper'})},      
                {'==': (
                    {'prey': 'weapon'},
                    {'string': 'stone'})} )})}}}
                    
ecosystem_settings4B = {
    'constraings': {
        'hunting': {'in': (
            ({'predator': 'weapon'}, {'prey': 'weapon'}),
            (({'literal': 'stone'},    {'literal': 'scissors'}),
             ({'literal': 'scissors'}, {'literal': 'paper'}),
             ({'literal': 'paper'},    {'literal': 'stone'})))}        
    }}



def print_ecosystem_settings(ecosystem_settings, indent_level = 0):
    if type(ecosystem_settings) == dict:
        print "    "*indent_level, '{' # This line could be removed
        for key in ecosystem_settings.keys():
            if hasattr(ecosystem_settings[key], '__iter__'):
                print "    "*indent_level, str(key)+":"
                print_ecosystem_settings(ecosystem_settings[key], indent_level + 1)
            else:
                print "    "*indent_level, str(key)+": ", ecosystem_settings[key]  
        print "    "*indent_level, '}' # This line also could be removed
    elif hasattr(ecosystem_settings, '__iter__'):
        for element in ecosystem_settings:
            print_ecosystem_settings(element, indent_level + 1)
    else:
        print "   "*indent_level, ecosystem_settings

"""   
    
for E in (Default_ecosystem_settings, ecosystem_settings, ecosystem_settings_2, ecosystem_settings_3):
    print "\n\n\n"
    print_ecosystem_settings(E)
    

"""
ecosystem_settings = {
    'ecosystem name': "Strength vs photosyntesis capacity",
    'biotope': { 
        'size': (70, 70),
        'featuremaps': None },
    'organisms': 
        {'number of organisms': 500,
        'genes': { 
            'weapon': {
                'initial value': {            
                    'function': 'discrete distribution',
                    'values list': (
                        {'value': 'stone', 'probability': 1.0/3},                            
                        {'value': 'paper', 'probability': 1.0/3},                            
                        {'value': 'scissors', 'probability': 1.0/3})},
                'mutability': {
                    'new value': {
                        'choice': 'weapon',
                        'stone': {
                            'function': 'discrete distribution',
                            'values list': (
                                {'value': 'stone', 'probability': 'remain stone probability'},                            
                                {'value': 'paper', 'probability': 'stone to paper probability'},                            
                                {'value': 'scissors', 'probability': 'stone to scissors probability'})},
                        'paper': {
                            'function': 'discrete distribution',
                            'values list': (
                                {'value': 'stone', 'probability': 'paper to stone probability'},                            
                                {'value': 'paper', 'probability': 'remain paper probability'},                            
                                {'value': 'scissors', 'probability': 'paper to scissors probability'})},
                        'scissors': {
                            'function': 'discrete distribution',
                            'values list': (
                                {'value': 'stone', 'probability': 'scissors to stone probability'},                            
                                {'value': 'paper', 'probability': 'scissors to paper probability'},                            
                                {'value': 'scissors', 'probability': 'remain scissors probability'})} }}},                         
            'stone to paper probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'paper to scissors probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'scissors to stone probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'stone to scissors probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'scissors to paper probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'paper to stone probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'remain stone probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'remain paper probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'remain scissors probability': {
                'initial value': {'uniform': [0, 1]},
                'mutability': {'percentage variation': {'gauss': (0, 0.08)}, 'allowed interval': [0, 1]}},
            'color': {
                'choice': 'weapon',
                'stone': {'tuple': (
                    {'+': (20, {'*': (200, 'stone to paper probability')})}, 
                    {'+': (20, {'*': (200, 'stone to scissors probability')})}, 
                    {'+': (20, {'*': (200, 'remain stone probability')})})}, 
                'paper': {'tuple': (
                    {'+': (20, {'*': (200, 'paper to scissors probability')})}, 
                    {'+': (20, {'*': (200, 'paper to stone probability')})}, 
                    {'+': (20, {'*': (200, 'remain paper probability')})})}, 
                'scissors': {'tuple': (
                    {'+': (20, {'*': (200, 'scissors to stone probability')})}, 
                    {'+': (20, {'*': (200, 'scissors to paper probability')})}, 
                    {'+': (20, {'*': (200, 'remain scissors probability')})})}},
            'procreating frequency': 0.1,
            'speed': {
                'initial value': {'uniform': [0, 10]},
                'mutability': {
                    'will mutate?': {'function': 'random boolean', 'probability': 0.1},
                    'percentage variation': {'gauss': (0, 0.08)},
                    'allowed interval': [0, 10]
                    }
                },
            'hunt radius' : 1.1,
            'radius of procreation': 4.1,
            'actions list': ('move', 'hunt', 'procreate')}},
    'constraints': {
        'procreate?': {'<': (
                    {'function': 'uniform distribution', 'interval': [0, 1]}, 
                    'procreating frequency')},  
        'kill?': {'in': (
            {'tuple': ({'predator': 'weapon'}, {'prey': 'weapon'})},
            {'literal': (
                ('stone', 'scissors'),
                ('scissors', 'paper'),
                ('paper', 'stone') )})},
        'die?': {'function': 'random boolean', 'probability': 0.05}
                }  }


