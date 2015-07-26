from random import random
from copy import deepcopy
from Basic_tools import *
from Function_settings_reader import *

print_methods_names = False

actions_dictionary = {
    'do photosynthesis': lambda organism: organism.do_photosynthesis(),
    'move': lambda organism: organism.move(),
    'hunt': lambda organism: organism.hunt(),
    'interchange substances with the biotope': lambda organism: organism.interchange_substances_with_the_biotope(),
    'interchange substances with other organisms': lambda organism: organism.interchange_substances_with_other_organisms(),
    'fertilize other organisms': lambda organism: organism.fertilize_other_organisms(),
    'fertilize': lambda organism: organism.fertilize_other_organisms(),
    'procreate': lambda organism: organism.procreate(),
    'do internal changes': lambda organism: organism.do_internal_changes(),
    'stay alive': lambda organism: organism.stay_alive(),
    'age': lambda organism: organism.age()
}

class Organism(dict):

    def __init__(self, parent_ecosystem, organism_data = None):
        self.parent_ecosystem = parent_ecosystem
        for key in organism_data:
            self[key] = organism_data[key]
    
    def to_string(self, data):
        if is_number(data):
            return round(float(data), 2).__str__()
        elif is_dict(data):
            return dictionary_to_string(data)
        elif is_function(data):
            return self.to_string(data(self))
        elif hasattr(data, '__iter__'):
            return (self.to_string(item) for item in data)
        else:
            return data.__str__()
        
    def __str__(self, indent_level = 0, list_of_attributes = None):  # Just for debug
        if (list_of_attributes == None) or len(list_of_attributes) == 0:
            return dictionary_to_string(self, indent_level)
        else:
            if isinstance(list_of_attributes, str):
                return list_of_attributes, self.to_string(self[list_of_attributes])             
            elif len(list_of_attributes) == 1:
                return list_of_attributes[0], self.to_string(self[list_of_attributes[0]])
            else:
                
                return ", ".join("{0}: {1}".format(attribute, self[attribute]) for attribute in list_of_attributes if attribute in self)
   
    def add_gene(self, gene_name, gene_settings):
        initial_value_generator = self.parent_ecosystem.function_maker.read_function_settings(
            'initial value', 
            gene_settings['initial value']
        )
        self[gene_name] = initial_value_generator(self)
        if 'value after mutation' in gene_settings:
            self['value after mutation'][gene_name] = \
                self.parent_ecosystem.function_maker.read_function_settings(
                    gene_name, 
                    gene_settings['value after mutation']
                )       
        if 'value in next cycle' in gene_settings:
            self['value in next cycle'][gene_name] = \
                self.parent_ecosystem.function_maker.read_function_settings(
                    gene_name,
                    gene_settings['value in next cycle']
                )       
    
    def add_decision(self, decision_name, decision_settings):
        self[decision_name] = self.parent_ecosystem.function_maker.read_function_settings(
            decision_name,
            decision_settings
        )
    
    def act(self):
        if print_methods_names:
            print 'act'
        #print self['actions list']
        actions_sequence = self['actions sequence']
        for action in actions_sequence:
            decision_name = 'decide ' + action
            if ((decision_name in self) and self[decision_name](self)) or (not decision_name in self):
                constraints = self.parent_ecosystem.constraints
                constraint_name = 'can ' + action
                if ((constraint_name in constraints) and constraints[constraint_name](self)) or (not constraint_name in constraints):
                    actions_dictionary[action](self)                    
        if self.parent_ecosystem.constraints['die'](self):
            #print "dying alone", self.__str__(list_of_attributes = ('category', 'age', 'energy reserve'))
            self.die('natural cause')
                       
    def subtract_costs(self, action, factor = 1):
        if print_methods_names:
            print 'subtract_costs', action
        if action in self.parent_ecosystem.costs:
            for reserve_substance in self.parent_ecosystem.costs[action]:                       
                if reserve_substance in self:
                    if print_costs:
                        print action + " - " + self.__str__(0, ('category', 'age', 'energy reserve')), 
                    self[reserve_substance] = max(0, self[reserve_substance] - factor * self.parent_ecosystem.costs[action][reserve_substance](self)  )                  
                    if print_costs:
                        print "--> " + self.__str__(0, 'energy reserve')

    def interchange_substances_with_the_biotope(self):
        #if print_methods_names:
        #   print 'interchange_substances_with_the_biotope'
        pass

    def interchange_substances_with_other_organisms(self):
        #if print_methods_names:
        #   print 'interchange_substances_with_other_organisms'
        """ 
        Peacefull trade of substances:
            Each organism has a list of offers for other organisms that can 
        buy or not. An organism may want to sell its surplus of certain substances 
        in exchange for other substances that it needs. It offers an 
        amount of substance and a price (i. e. a ratio) in terms of other
        substance.
        
        Not so pacefull interchange of substances:
            An organism can stole a part of substance reserves from other organisms,
        as herbivorous do with plants, or as parasites do with their hosts.
            An organism may also inject a substance to other organism in order
        to kill it or damage it in self-defense of to eat it after it dies.
        """
        pass

    def fertilize_other_organisms(self):
        #if print_methods_names:
        #   print 'fertilize_other_organisms'
        """ To partially transmit its own genes to other organisms that
        accepts them in order to produce a new being that inherit genes from
        both parents
        """
        pass
    
    
    def stay_alive(self):
        #if print_methods_names:
        #   print 'stay_alive'
        #print self['energy reserve'], self['photosynthesis capacity'], "*****", self['actions sequence'](self)
        """ An organism has to spend energy and maybe other substances only to
        stay alive.
        """
        if 'energy reserve' in self:
            energy_reserve = self['energy reserve']
            self.subtract_costs('stay alive', factor = 1)  
            return 'energy reserve: {0} - {1} = {2}'.format(energy_reserve, energy_reserve - self['energy reserve'], self['energy reserve'])          
        else:
            self.subtract_costs('stay alive', factor = 1)          
        
    def move(self):
        if print_methods_names:
            print 'move'
        """
            Check if there is a new available location. If yes
            then: - Update biotope (organisms matrix)
                  - Update location
        """
        # 1. Get a new location:
        new_location = self.parent_ecosystem.biotope.seek_free_location_close_to(center = self['location'], radius = self['speed'])
        # 2. Check if it has found a new location:
        if new_location != None:
            old_location = self['location']
            # 3. Update location
            self['location'] = new_location
            # 4. Update biotope (organisms matrix):
            self.parent_ecosystem.biotope.move_organism(old_location, new_location)
            # 5. The costs are proportional to the distance we have jump:                    
            self.subtract_costs('move', factor = self.parent_ecosystem.biotope.distance(old_location, new_location))
            return 'moved to', new_location
        return "It didn't move"
                        
    def move2(self): 
        """
            Check if there is a new available location. If yes
            then: - Update biotope (organisms matrix)
                  - Update location
        """
        # No todos los organismos tienen por que usar la funcion "seek_free_location_close_to(center, radius)"    
        # para buscar un sitio al que moverse. Algun organismo puede usar una 
        # funcion mas inteligente, que dependa de la concentracion de determinada
        # sustancia o del gradiente de densidad de poblacion de determinada especie.
        # O tambien puede haber otros que decidan moverse siempre en linea recta
        # hasta que se topen con algo. Hay infinidad de maneras de moverse.
        
        # Por eso podriamos usar este metodo en lugar del anterior. La dejo aqui por si lo usamos en un futuro.
        # Esta es una forma alternativa de definir el movimiento. Lo considera
        # un cambio de estado como otro cualquiera. Un organismo puede ser capaz
        # de moverse de una determinada manera al igual que otro organismo puede
        # ser capaz de cambiar cualquier otro gen interno de alguna otra manera.

        # Tenemos que decidir si usamos este metodo move o el anterior. La unica
        # diferencia para el usuario seria la manera de definir el movimiento
        # en ecosystem_settings
        
        # 1. Check if this organism can move itself:
        if 'location' in self['variable genes']:
            # 2. Check if this organism decide to move:
            if self['variable genes']['location']['will change?'](self):
                # 3. Get a new location:
                new_location = self['variable genes']['location']['new value'](self)
                # 4. Check if it has found a new location:
                if new_location != None:
                    old_location = self['location']
                    # 5. Update location
                    self['location'] = new_location
                    # 6. Update biotope (organisms matrix):
                    self.parent_ecosystem.biotope.move_organism(old_location, new_location)
                    # 7. The costs are proportional to the distance we have jump:                    
                    self.subtract_costs('move', factor = self.parent_ecosystem.biotope.distance(old_location, new_location))

    def eat(self, prey):
        if print_methods_names:
            print 'eat'
        for reserve_substance in prey['list of reserve substances']:
            if reserve_substance in self:
                #print 'eating', prey['category'], self[reserve_substance], "+", prey[reserve_substance], "=",                 
                self[reserve_substance] += prey[reserve_substance]
                storage_capacity = self.parent_ecosystem.storage_capacities_dictionary[reserve_substance] 
                if storage_capacity in self:
                    self[reserve_substance] = min(self[reserve_substance], self[storage_capacity])
                #print self['energy reserve']
        self.subtract_costs('eat')
                
    def hunt(self):
        if print_methods_names:
            print 'hunt'
        prey_location = None
        if 'seeking prey technique' in self:            
            prey_location = self['seeking prey technique'](self)
        else:
            if 'decide attack #prey' in self:
                condition = lambda prey: (prey != None) and (prey != self) and self['decide attack #prey'](prey)
            else:
                condition = lambda prey: (prey != None) and (prey != self)
            if 'hunt radius' in self:
                hunt_radius = self['hunt radius']
            else:
                hunt_radius = 1.5
            prey_location = self.parent_ecosystem.biotope.seek_possible_prey_close_to(
                    center = self['location'],
                    radius = hunt_radius,
                    condition = condition)
        if prey_location != None:
            prey = self.parent_ecosystem.biotope.get_organism(prey_location)
            if self.parent_ecosystem.constraints['can kill #predator #prey'](self, prey):
                self.eat(prey)
                prey.die('killed by a predator')  
                result = 'successful hunt'
            else:
                result = 'hunt failed, prey won'
            self.subtract_costs('hunt', factor = self.parent_ecosystem.biotope.distance(self['location'], prey_location))        
        else:
            result = 'hunt failed, prey not found'
        return result
                    
    def mutate(self):
        if print_methods_names:
            print 'mutate'
        for gene in self['value after mutation']:
            # print "MUTATING", gene
            self[gene] = self['value after mutation'][gene](self)

    def do_internal_changes(self):
        if print_methods_names:
            print 'do_internal_changes'
        energy_reserve = self['energy reserve'] # this is for debuggin

        for gene in self['value in next cycle']:
            print 'do_internal_changes', gene
            self[gene] = self['value in next cycle'][gene](self)

        #print 'energy reserve: {0} + {1} = {2}'.format(energy_reserve, self['energy reserve'] - energy_reserve, self['energy reserve']) 
        return 'energy reserve: {0} + {1} = {2}'.format(energy_reserve, self['energy reserve'] - energy_reserve, self['energy reserve'])  # this is for debuggin purposes        

    def procreate(self): 
        if print_methods_names:
            print 'procreate'
        """
            Depending on the reproduction frequency and the energy,
            a baby can be created and added to:
              - the organisms matrix in biotope
              - the list of organisms in parent_ecosystem
            Return true if procreated, else return false.
        """

        if ('can procreate' in self.parent_ecosystem.constraints and 
            not self.parent_ecosystem.constraints['can procreate'](self)):
            return False
        elif ('decide procreate' in self and 
            not self['decide procreate'](self)):
            return False

        procreated = False
        # Get a new location for the new baby:
        if 'radius of procreation' in self:
                radius_of_procreation = self['radius of procreation']
        else:
            radius_of_procreation = 1.5
        new_location = self.parent_ecosystem.biotope.\
            seek_free_location_close_to(center = self['location'], radius = radius_of_procreation)
        if new_location != None: # if there is enough space:
            # Create the baby:
            #print 'making a deep copy'                
            newborn = Organism(self.parent_ecosystem, deep_copy_of_a_dictionary(self))
            """              
            # Utilizamos deep_copy_of_a_dictionary, porque es mucho mas veloz que deepcopy()
            Esto genera un enorme cuello de botella, ralentizando mucho el programa
            """
            newborn['location'] = new_location
            if 'age' in newborn:
                newborn['age'] = 0
            # Trigger mutations:
            newborn.mutate()
            # The parent and the child share reserves:
            if 'energy reserve' in self:
                newborn['energy reserve'] = newborn['energy reserve at birth'] 
            for reserve_substance in self['list of reserve substances']:
                self[reserve_substance] -= newborn[reserve_substance]
            # Add the new organism to the ecosystem:
            self.parent_ecosystem.add_organism(newborn)
            self.subtract_costs('procreate', self.parent_ecosystem.biotope.distance(self['location'], new_location))
            procreated = True
            if print_births:                
                #print 'SELF:'
                #print_dictionary(self)
                #print "\nNEWBORN:"
                #print_dictionary(newborn)
                #a = raw_input('press any key...')
                print "newborn!"
        #else:
            #print "Not enough space"
        return procreated

    def die(self, cause = 'natural deth'):
        if print_methods_names:
            print 'die'
        # self.parent_ecosystem.delete_organism(self) # parent_ecosystem tells biotope to erase organism from it
        if print_deths:        
            print 'dying', self.__str__(list_of_attributes = ('category', 'age', 'energy reserve')), cause        
        elif print_killed and cause == 'killed by a predator':
            print 'dying', self.__str__(list_of_attributes = ('category', 'age', 'energy reserve')), cause                    
        self.parent_ecosystem.new_deads.append(self)






