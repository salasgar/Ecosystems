from Experiment import experiment

def modify_dict(dictionary):
    dictionary['my modification'] = 'Hello'

modify_dict(experiment)
for i in experiment:
    print "experiment[",i, "] =", experiment[i]
    