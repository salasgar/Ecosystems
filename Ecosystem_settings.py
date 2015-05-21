         
DEFAULT_SETTINGS = {
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
        'constraints': {} },
            
    'seeking prey': {
        'maximum attack distance': 1.5,
        'seeking prey technique': {
            'function': 'seek random organism',
            'center': 'location',
            'radius': 'maximum attack distance'}                  
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
        'size': (4, 4),
        'featuremaps': None },
    'organisms': [
        {'category': 'Plants',
        'number of organisms': 0,
        'genes': { 
            'strength': {
                'initial value': { 
                    'function': 'gaussian',
                    'mean': 10, 
                    'variance': 2},
                'mutability': {
                    'absolute variation': {
                        'function': 'gaussian',
                        'mean': 0.0, 
                        'variance': 0.01},
                    'percentage variation': {
                        'function': 'gaussian',
                        'mean': 0.0, 
                        'variance': 2.0},
                    'mutation frequency': 'strength mutation frequency',
                    'allowed interval': [0, 'infinity']
                }},
            'defense capacity': 'strength',
            'strength mutation frequency': {
                'initial value': 0.05,
                'mutability': {
                    'new value': {
                        'function': 'uniform distribution',
                        'interval': [0, 0.1]},
                    'mutation frequency': 0.01
                }},
            'energy reserve procreating threshold': 50,
            'procreating frequency': 0.1,
            'photosynthesis capacity': { # SALAS: etc, etc....
                'initial value': {
                    'function': 'uniform distribution',
                    'interval': [10, 30] },
                'mutability': {
                    'absolute variation': {
                        'function': 'gaussian',
                        'mean': 0.0, 
                        'variance': 0.15},
                    'mutation frequency': 0.001}  },
            'energy storage capacity': {
                'initial value': 1000.0,
                'mutability': {
                    'percentage variation': {
                        'function': 'uniform distribution',
                        'interval': [-5.0, 5.0]},
                    'mutation frequency': 0.02
                }}
        },
        'status': {
            'age': 0,
            'energy reserve': 100.0}  },
        {'category': 'Animals',
        'number of organisms': 3,
        'genes': {
            'average attack capacity': {
                'initial value': 10,
                'mutability': {
                    'variation': {
                        'function': 'gaussian',
                        'mean': 0.0, 
                        'variance': 0.01},
                    'mutation frequency': 0.05,
                    'allowed interval': [0, 'infinity']}},
            'attack capacity': { # This gene is function of the organism itself:
                        'function': 'gaussian',
                        'mean': 'average attack capacity',
                        'variance': 'average attack capacity'},
            'defense capacity': 'attack capacity',
            'procreating frequency': 0.1,
            'energy reserve procreating threshold': 50,
            'speed': {
                'initial value': {
                    'function': 'discrete distribution',
                    'values list': [
                        {'value': 0.0, 'probability': 0.25},
                        {'value': 1.0, 'probability': 0.70},
                        {'value': 5.0, 'probability': 0.05}] }}
        },  
        'status': {
            'age': 0,
            'energy reserve': 100} }
    ],
                    
    'outlays': {
        'hunting': {
            '+': (
                {'*': (3.0, 'strength')}, 
                {'*': (0.2, 'speed')},
                5.0)},         
        'moving': {
            '+': (
                {'*': ('strength', 1.0)}, 
                {'*': ('photosynthesis capacity', 25.0)}, 
                {'*': ('speed', 5.0)}, 
                {'*': ('energy storage capacity', 0.001)}, 
                1.0)},
      'procreating': {
            '+': (
                {'*': ('strength', 3.0)}, 
                {'*': ('photosynthesis capacity', 3.0)}, 
                {'*': ('speed', 3.0)}, 
                5.0)},
      'living': {
            '+': (
                {'*': ('strength', 1.0)}, 
                {'*': ('photosynthesis capacity', -1.0)},
                {'*': ('energy storage capacity', 0.002)}, 
                {'*': ('speed', 2.0)}, 
                5.0)}},

    'constraints': {
        'procreating': {
            'and': (
                {'<': (
                    {'function': 'uniform distribution', 'interval': [0, 1]}, 
                    'procreating frequency')},
                {'>': (
                    'energy reserve',
                    'energy reserve procreating threshold')} )},
                    
        'hunting': {
            '>': (
                {'predator': 'attack capacity'},
                {'prey': 'defense capacity'})},
            
        'dying': {
            'or': (
                {'<': (
                    'energy reserve', 
                    10.0)},
                {'>': (
                    'age',
                    {'function': 'gaussian',
                         'mean': 120,
                         'variance': 20})})}}
 }


# Default ecosystem settings		(Estos son los valores por defecto)											
Default_ecosystem_settings = {
    'ecosystem name': "Ecosystem name",
    'biotope': {
	'size': (100, 200),
	'featuremaps': None },
 'organisms': [{'category': 'General category',
       'number of organisms': 10,
       'genes': {
		'speed': 0.0,
		'mutation frequency': 1.0
		},
    	'status': {
  		'coordinates': {
			'type': 'Biotope call',
			'subtype': 'seek free position'}
		} }],
  'outlays': { },
  'constraints': { },
  'mutability': { }
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

