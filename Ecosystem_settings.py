            
              
ecosystem_settings = {
 'ecosystem name': "Strength vs photosyntesis capacity",
 'biotope': {  # SALAS: ponemos 'biotope settings' ?
	'size': (100, 200), # SALAS: ponemos 'size settings' ?
	'featuremaps': None },
 'organisms': [ # SALAS: ponemos 'organisms settings' ?
     {'category': 'Plants',
         'number of organisms': 1,
         'genes': { # SALAS: ponemos 'genes settings' ?
             'strength': {
                 'initial value': { # SALAS: ponemos 'initial value settings' ?
                     'type': 'random function',
                     'subtype': 'gaussian',
                     'mean': 10, 
                     'variance': 2},
                 'mutability': { # SALAS: ponemos 'mutability settings' ?
                     'absolute variation': {
                         'type': 'random function',
                         'subtype': 'gaussian',
                         'mean': 0.0, 
                         'variance': 0.01},
                     'percentage variation': { # SALAS: ponemos 'percentage variation settings' ?
                         'type': 'random function',
                         'subtype': 'gaussian',
                         'mean': 0.0, 
                         'variance': 2.0},
                     'mutation frequency': 'strength mutation frequency',
                     'allowed interval': [0, 'infinity']
                     }},
             'strength mutation frequency': {
                 'initial value': 0.05,
                 'mutability': {
                     'new value': {
                         'type': 'random function',
                         'subtype': 'uniform distribution',
                         'interval': [0, 0.1]},
                     'mutation frequency': 0.01
                     }},
             'photosynthesis capacity': { # SALAS: etc, etc....
                 'initial value': {
                     'type': 'random function',
                     'subtype': 'uniform distribution',
                     'interval': [10, 30] },
                 'mutability': {
                     'absolute variation': {
                         'type': 'random function',
                         'subtype': 'gaussian',
                         'mean': 0.0, 
                         'variance': 0.15},
                     'mutation frequency': 0.001}  },
             'energy storage capacity': {
                 'initial value': 1000.0,
                 'mutability': {
                     'percentage variation': {
                         'type': 'random function',
                         'subtype': 'uniform distribution',
                         'interval': [-5.0, 5.0]},
                     'mutation frequency': 0.02
                  }}
         },
         'status': {
             'age': 0,
             'energy reserve': 100.0}  },
     {'category': 'Animals',
         'number of organisms': 1,
         'genes': {
             'strength': {
                 'initial value': 10,
                 'mutability': {
                     'variation': {
                         'type': 'random function',
                         'subtype': 'gaussian',
                         'mean': 0.0, 
                         'variance': 0.01},
                     'mutation frequency': 0.05,
                     'allowed interval': [0, 'infinity']}},
             'speed': {
                 'initial value': {
                     'type': 'random function',
                     'subtype': 'discrete distribution',
                     'values': [
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
          'type': 'outlay function',
          'subtype': 'linear function',
          'terms': [
              {'parameter': 'strength', 'coefficient': 3.0}, 
              {'parameter': 'speed', 'coefficient': 0.2}, 
              {'parameter': None, 'coefficient': 5.0}]},
      'moving': {
          'type': 'outlay function',
          'subtype': 'linear function',
          'terms': [
              {'parameter': 'strength', 'coefficient': 1.0}, 
              {'parameter': 'photosynthesis capacity', 'coefficient': 25.0}, 
              {'parameter': 'speed', 'coefficient': 5.0}, 
              {'parameter': 'energy storage capacity', 'coefficient': 0.001}, 
              {'parameter': None, 'coefficient': 1.0}]},
      'procreating': {
          'type': 'outlay function',
          'subtype': 'linear function',
          'terms': [
              {'parameter': 'strength', 'coefficient': 3.0}, 
              {'parameter': 'photosynthesis capacity', 'coefficient': 3.0}, 
              {'parameter': 'speed', 'coefficient': 3.0}, 
              {'parameter': None, 'coefficient': 5.0}]},
      'living': {
          'type': 'outlay function',
          'subtype': 'linear function',
          'terms': [
              {'parameter': 'strength', 'coefficient': 1.0}, 
              {'parameter': 'photosynthesis capacity', 'coefficient': -1.0},
              {'parameter': 'energy storage capacity', 'coefficient': 0.002}, 
              {'parameter': 'speed', 'coefficient': 2.0}, 
              {'parameter': None, 'coefficient': 5.0}]}},

  'constraints': {
   	'procreating': {
		'type': 'interpreted function',
		'subtype': 'organism constraint',
		'a': 'energy reserve',
		'r': ('random number', 'uniform distribution [0, 1]'),
		'expression': "a*r > 100.0"  },
 	'hunting': {
		'type': 'interpreted function',
		'subtype': 'compare predator vs prey',
		'a': ('predator', 'strength'),
		'b': ('prey', 'strength'),
		'r1': ('random number', 'uniform distribution [0, 1]'),
		'r2': ('random number', 'uniform distribution [0, 1]'),
		'expression': "a*r1 > b*r2"  },
	'dying': {
		'type': 'constraint function',
		'subtype': 'thresholds',
            'operator': 'or',
            'terms': [
                {'parameter': 'energy reserve', 
                'operator': '<',
                'threshold': 10.0},
                {'parameter': 'age',
                'operator': '>',
                'random threshold': {
                    'type': 'random function',
                    'subtype': 'gaussian',
                    'mean': 120,
                    'variance': 20}
                    }              
                ]
		} },
}


# Default ecosystem settings		(Estos son los valores por defecto)											
Default_ecosystem_settings = {'ecosystem name': "Ecosystem name",
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
				'type': 'random function',
				'subtype': 'discrete distribution',
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
				'type': 'random function',
				'subtype': 'discrete distribution',
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
			'type': 'random function',
			'subtype': 'gaussian',
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
			'type': 'random function',
			'subtype': 'gaussian',
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
			'type': 'random function',
			'subtype': 'chi-squared',
			'k': 3},
            	'defense capacity': { 
			'type': 'random function',
			'subtype': 'chi-squared',
			'k': 3},
             	'photosynthesis capacity': 20.0,
		'energy reserve at birth': 100.0,
		'minimun energy reserve at procreation': 200.0},
	'status': { 'energy reserve': 200.0} }],
'outlays': {
	'load outlays': "/Pepito/ecosystem_settings/cool ecosystem_settings 2.exp",
	'living': {
		'type': 'outlay function',
		'subtype': 'n-linear function',
		'terms': [
			{'parameters': ['attack capacity', 'defense capacity'], 		'coefficient': 1.0}, 
                  	{'parameters': ['photosynthesis capacity'], 				'coefficient': -1.0},
			{'parameters': ['attack capacity', 'photosynthesis capacity'], 	'coefficient': 25.0}, 
			{'parameters': [], 								'coefficient': 0.5}]} },
'constraints': {
   	'procreating': {
		'type': 'threshold',
		'parameter': 'energy reserve',
		'threshold': 'minimun energy reserve at procreation'},
	'hunting': {
		'type': 'interpreted function',
		'subtype': 'compare predator vs prey',
		'a': ('predator', 'attack capacity'),
		'b': ('prey', 'defense capacity'),
		'r1': ('random number', 'uniform distribution [0, 1]'),
		'r2': ('random number', 'uniform distribution [0, 1]'),
		'expression': "a*r1 > b*r2"  } },
  'mutability': {
	'all genes': {
		'percentage variation': {
			'type': 'random function',
			'subtype': 'gaussian',
			'mean': 0.0, 
			'variance': 0.01},
		'mutation frequency': 0.05,
		'allowed interval': [0, 'infinity']	}
	}
}

# Nota: En este experimento veremos si los mutantes ganan a los no mutantes en la 
# guerra por la supervivencia 




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