from random import random
from copy import deepcopy
from Tools import *

actions_dictionary = {
    'do photosynthesis': lambda organism: organism.do_photosynthesis(),
    'move': lambda organism: organism.move(),
    'hunt': lambda organism: organism.hunt(),
    'interchange substances with the biotope': lambda organism: organism.interchange_substances_with_the_biotope(),
    'interchange substances with other organisms': lambda organism: organism.interchange_substances_with_other_organisms(),
    'fertilize other organisms': lambda organism: organism.fertilize_other_organisms(),
    'procreate': lambda organism: organism.procreate(),
    'do internal changes': lambda organism: organism.do_internal_changes(),
    'stay alive': lambda organism: organism.stay_alive(),
    'age': lambda organism: organism.age()
}

def make_mutability(gene, mutability_settings):    
    #print 'make_mutability'
    if 'new value' in mutability_settings:
        calculate_new_value = make_function(mutability_settings['new value'], number_of_organisms = 1)
    elif 'absolute variation' in mutability_settings:
        absolute_variation = make_function(mutability_settings['absolute variation'], number_of_organisms = 1)
        if 'percentage variation' in mutability_settings:
            percentage_variation = make_function(mutability_settings['percentage variation'], number_of_organisms = 1)
            calculate_new_value = lambda organism: organism[gene] * (1 + percentage_variation(organism)) + absolute_variation(organism)
        else:
            calculate_new_value = lambda organism: organism[gene] + absolute_variation(organism)
    elif 'percentage variation' in mutability_settings:
        percentage_variation = make_function(mutability_settings['percentage variation'], number_of_organisms = 1)
        calculate_new_value = lambda organism: organism[gene] * (1 + percentage_variation(organism))
    else:
        calculate_new_value = lambda organism: organism[gene] # (no mutation) 
    if 'mutation frequency' in mutability_settings:
        mutation_frequency = make_function(mutability_settings['mutation frequency'], number_of_organisms = 1)
        will_mutate = lambda organism: (random() < mutation_frequency(organism))
    elif 'will mutate?' in mutability_settings:
        will_mutate = make_function(mutability_settings['will mutate?'], number_of_organisms = 1)
    else: 
        will_mutate = lambda organism: True
    if 'allowed interval' in mutability_settings:
        interval = mutability_settings['allowed interval']
        new_value = lambda organism: bounded_value(calculate_new_value(organism), *interval)
    else:
        new_value = calculate_new_value
    return {'will mutate?': will_mutate, 'new value': new_value}
        
def make_modifying_status(status, modifying_settings):    
    #print 'make_modifying_status'
    if 'new value' in modifying_settings:
        calculate_new_value = make_function(modifying_settings['new value'], number_of_organisms = 1)
    elif 'absolute variation' in modifying_settings:
        absolute_variation = make_function(modifying_settings['absolute variation'], number_of_organisms = 1)
        if 'percentage variation' in modifying_settings:
            percentage_variation = make_function(modifying_settings['percentage variation'], number_of_organisms = 1)
            calculate_new_value = lambda organism: organism[status] * (1 + percentage_variation(organism)) + absolute_variation(organism)
        else:
            calculate_new_value = lambda organism: organism[status] + absolute_variation(organism)
    elif 'percentage variation' in modifying_settings:
        percentage_variation = make_function(modifying_settings['percentage variation'], number_of_organisms = 1)
        calculate_new_value = lambda organism: organism[status] * (1 + percentage_variation(organism))
    else:
        calculate_new_value = lambda organism: organism[status] # (no change) 
    if 'changing frequency' in modifying_settings:
        changing_frequency = make_function(modifying_settings['changing frequency'], number_of_organisms = 1)
        will_change = lambda organism: (random() < changing_frequency(organism))
    elif 'will change?' in modifying_settings:
        will_change = make_function(modifying_settings['will change?'], number_of_organisms = 1)
    else:
        will_change = lambda organism: True
    if 'allowed interval' in modifying_settings:
        interval = modifying_settings['allowed interval']
        new_value = lambda organism: bounded_value(calculate_new_value(organism), *interval)
    else:
        new_value = calculate_new_value
    return {'will change?': will_change, 'new value': new_value}

class Organism(dict):

    def __init__(self, parent_ecosystem, organism_data = None):
        self.parent_ecosystem = parent_ecosystem
        for key in organism_data:
            self[key] = organism_data[key]
    
    def to_string(self, data):
        if is_number(data):
            return round(float(data), 2).__str__()
        elif isinstance(data, dict):
            return dictionary_to_string(data)
        elif isinstance(data, FunctionType):
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
                return " ".join((attribute, self.to_string(self[attribute])).__str__() for attribute in list_of_attributes if attribute in self)
   
    def add_gene(self, gene, gene_settings, all_genes):
        if isinstance(gene_settings, dict):
            if 'initial value' in gene_settings:
                initial_value_generator = make_function(gene_settings['initial value'], number_of_organisms = 1)
                self[gene] = initial_value_generator(self)
            else: # the gene is a function:
                self[gene] = make_function(gene_settings, number_of_organisms = 1)         
            if 'mutability' in gene_settings:
                self['mutating genes'][gene] = make_mutability(gene, gene_settings['mutability'])       
        else:
            if isinstance(gene_settings, str) and gene_settings in all_genes:
                self[gene] = make_function(gene_settings, number_of_organisms = 1)
            else:
                self[gene] = gene_settings

    def add_status(self, status, status_settings, all_status):
        if isinstance(status_settings, dict):
            if 'initial value' in status_settings:
                initial_value_statusrator = make_function(status_settings['initial value'], number_of_organisms = 1)
                self[status] = initial_value_statusrator(self)
            else: # the status is a function:
                self[status] = make_function(status_settings, number_of_organisms = 1)         
            if 'modifying' in status_settings:
                self['modifying status'][status] = make_modifying_status(status, status_settings['mutability'])       
        else:
            if isinstance(status_settings, str) and status_settings in all_status:
                self[status] = make_function(status_settings, number_of_organisms = 1)
            else:
                self[status] = status_settings

        
    def act(self):
        #print 'act'
        #print self['actions list']
        for action in self['actions sequence']:
            actions_dictionary[action](self)
        if self.parent_ecosystem.constraints['die?'](self):
            #print "dying alone", self.__str__(list_of_attributes = ('category', 'age', 'energy reserve'))
            self.die('natural cause')
                       
    def subtract_outlays(self, action, factor = 1):
        #print 'subtract_outlays', action
        if action in self.parent_ecosystem.outlays:
            for reserve_substance in self.parent_ecosystem.outlays[action]:                       
                if reserve_substance in self:
                    if print_outlays:
                        print action + " - " + self.__str__(0, ('category', 'age', 'energy reserve')), 
                    self[reserve_substance] = max(0, self[reserve_substance] - factor * self.parent_ecosystem.outlays[action][reserve_substance](self)  )                  
                    if print_outlays:
                        print "--> " + self.__str__(0, 'energy reserve')

    def interchange_substances_with_the_biotope(self):
        #print 'interchange_substances_with_the_biotope'
        pass

    def interchange_substances_with_other_organisms(self):
        #print 'interchange_substances_with_other_organisms'
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
        #print 'fertilize_other_organisms'
        """ To partially transmit its own genes to other organisms that
        accepts them in order to produce a new being that inherit genes from
        both parents
        """
        pass
    
    
    def stay_alive(self):
        #print 'stay_alive'
        """ An organism has to spend energy and maybe other substances only to
        stay alive.
        """
        self.subtract_outlays('stay alive', factor = 1)            

    def move(self):
        #print 'move'
        """
            Check if there is a new available location. If yes
            then: - Update biotope (organisms matrix)
                  - Update location
        """
        # 1. Check if this organism can move itself:
        if 'speed' in self:
            # 2. Check if this organism decide to move:
            if (('move?' in self) and self['move?']()) or not 'move?' in self:
                # 3. Get a new location:
                new_location = self.parent_ecosystem.biotope.seek_free_location_close_to(self['location'], self['speed'])
                # 4. Check if it has found a new location:
                if new_location != None:
                    old_location = self['location']
                    # 5. Update location
                    self['location'] = new_location
                    # 6. Update biotope (organisms matrix):
                    self.parent_ecosystem.biotope.move_organism(old_location, new_location)
                    # 7. The outlays are proportional to the distance we have jump:                    
                    self.subtract_outlays('move', factor = self.parent_ecosystem.biotope.distance(old_location, new_location))

                        
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
        # ser capaz de cambiar cualquier otro status interno de alguna otra manera.

        # Tenemos que decidir si usamos este metodo move o el anterior. La unica
        # diferencia para el usuario seria la manera de definir el movimiento
        # en ecosystem_settings
        
        # 1. Check if this organism can move itself:
        if 'location' in self['modifying status']:
            # 2. Check if this organism decide to move:
            if self['modifying status']['location']['will change?'](self):
                # 3. Get a new location:
                new_location = self['modifying status']['location']['new value'](self)
                # 4. Check if it has found a new location:
                if new_location != None:
                    old_location = self['location']
                    # 5. Update location
                    self['location'] = new_location
                    # 6. Update biotope (organisms matrix):
                    self.parent_ecosystem.biotope.move_organism(old_location, new_location)
                    # 7. The outlays are proportional to the distance we have jump:                    
                    self.subtract_outlays('move', factor = self.parent_ecosystem.biotope.distance(old_location, new_location))

    def eat(self, prey):
        #print 'eat'
        for reserve_substance in prey['list of reserve substances']:
            if reserve_substance in self:
                #print 'eating', prey['category'], self[reserve_substance], "+", prey[reserve_substance], "=",                 
                self[reserve_substance] += prey[reserve_substance]
                storage_capacity = self.parent_ecosystem.storage_capacities_dictionary[reserve_substance] 
                if storage_capacity in self:
                    self[reserve_substance] = min(self[reserve_substance], self[storage_capacity])
                #print self['energy reserve']
        self.subtract_outlays('eat')
                
    def hunt(self):
        #print 'hunt'
        if (('hunt?' in self) and self['hunt?']()) or not 'hunt?' in self:
            prey_location = None
            if 'seeking prey technique' in self:            
                prey_location = self['seeking prey technique'](self)
            else:
                prey_location = self.parent_ecosystem.biotope.seek_possible_prey_close_to(
                    center = self['location'],
                    radius = self['hunt radius']) # the radius should be in the genes
            if prey_location != None:
                prey = self.parent_ecosystem.biotope.get_organism(prey_location)
                if self.parent_ecosystem.constraints['kill?'](predator = self, prey = prey):
                    self.eat(prey)
                    prey.die('killed by a predator')  
                self.subtract_outlays('hunt', factor = self.parent_ecosystem.biotope.distance(self['location'], prey_location))

    def do_photosynthesis(self):
        """ This method is completely unnecessary, because we can define it in ecosystem_settings:
        
        'organisms': {
            'category': 'Little pretty plants',
            'energy reserve': {
                'initial value': 10000,
                'modifying': {'new value': {'+': ('energy reserve', 'photosynthesis capacity')}}},
            'attack capacity': ....
            ...
            
            }
            
        Furthermore, the user can define it in many different ways. For example:
        
        'organisms': {
            'category': 'Little pretty plants',
            'energy reserve': {
                'initial value': 10000,
                'modifying': {
                    'new value': {'+': (
                        'energy reserve', 
                        {'gauss': ('photosynthesis capacity', 20.0)})},
                    'allowed interval': [0, 'infinity']}},
            'attack capacity': ....
            ...
            
            
        'organisms': {
            'category': 'Little pretty plants',
            'energy reserve': {
                'initial value': 10000,
                'modifying': {'new value': {'+': (
                    'energy reserve', 
                    {'*': (
                        'photosynthesis capacity',
                        {'amount of substance': 'sunlight',
                        'location': 'location'})}
                    )}}},
            'attack capacity': ....
            ...


        'organisms': {
            'category': 'Little pretty plants',
            'energy reserve': {
                'initial value': 10000,
                'modifying': {
                    'new value': {'+': (
                        'energy reserve', 
                        {'sqrt': 'photosynthesis capacity'})},
                    'allowed interval': [0, 'infinity']}},
            'attack capacity': ....
            ...
            
        The user can also define it in the constraints:
        
        'stay alive': {'energy reserve': {
            '+': (
                {'*': ('photosynthesis capacity', -1)}, 
                {'*': ('attack capacity', 0.3)}, 
                {'*': ('photosynthesis capacity', 'photosynthesis capacity', 0.0008)},
                {'*': ('energy storage capacity', 0.002)}, 
                {'*': ('energy reserve', 0.05)},
                {'*': ('speed', 0.2)}, 
                0.1)}}} 
        
        
        Shall I remove it?
        """ 
        #print 'do_photosynthesis'
        if ('photosynthesis capacity' in self) and ('energy reserve' in self):
            if isinstance(self['photosynthesis capacity'], FunctionType):               
                self['energy reserve'] += self['photosynthesis capacity'](self)
            else:
                #print "photo!", self['photosynthesis capacity']
                self['energy reserve'] += self['photosynthesis capacity']
            if ('energy storage capacity' in self):
                if isinstance(self['energy storage capacity'], FunctionType):                   
                    self['energy reserve'] = min(self['energy reserve'], self['energy storage capacity'](self))   
                else:
                    self['energy reserve'] = min(self['energy reserve'], self['energy storage capacity'])   
        
    def mutate(self):
        #print 'mutate'
        for mutating_gene in self['mutating genes']:
            if self['mutating genes'][mutating_gene]['will mutate?'](self):
                self[mutating_gene] = self['mutating genes'][mutating_gene]['new value'](self)

    def do_internal_changes(self):
        #print 'do_internal_changes'
        for modifying_status in self['modifying status']:
            if self['modifying status'][modifying_status]['will change?'](self):
                self[modifying_status] = self['modifying status'][modifying_status]['new value'](self)

    def procreate(self): 
        #print 'procreate'
        """
            Depending on the reproduction frequency and the energy,
            a baby can be created and added to:
              - the organisms matrix in biotope
              - the list of organisms in parent_ecosystem
            Return true if procreated, else return false.
        """
        procreated = False
        # Check weather the organism can procreate:
        if ('procreate?' in self.parent_ecosystem.constraints and self.parent_ecosystem.constraints['procreate?'](self)) or ('procreate?' in self and self['procreate?'](self)):
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
                """              
                #Esto genera un enorme cuello de botella, ralentizando mucho el programa:
                newborn = deepcopy(self)
                """
                newborn = Organism(self.parent_ecosystem, deep_copy_of_a_dictionary(self))
                #print 'deep copy made!'
                if print_births:                
                    print 'SELF:'
                    print_dictionary(self)
                    print "\nNEWBORN:"
                    print_dictionary(newborn)
                newborn['location'] = new_location
                if 'age' in newborn:
                    newborn['age'] = 0
                # Trigger mutations:
                newborn.mutate()
                # The parent and the child share reserves:
                newborn['energy reserve'] = newborn['energy reserve at birth'] 
                for reserve_substance in self['list of reserve substances']:
                    #print reserve_substance, newborn[reserve_substance]                    
                    self[reserve_substance] -= newborn[reserve_substance]
                    pass
                # Add the new organism to the ecosystem:
                self.parent_ecosystem.add_organism(newborn)
                self.subtract_outlays('procreate', self.parent_ecosystem.biotope.distance(self['location'], new_location))
                procreated = True
                if print_births:                
                    #print 'SELF:'
                    #print_dictionary(self)
                    #print "\nNEWBORN:"
                    #print_dictionary(newborn)
                    #a = raw_input('press any key...')
                    print "newborn!"
        return procreated

    def age(self):
        #print 'age'
        """ This method is completely unnecessary, because we can define it in ecosystem_settings:
        
        'organisms': {
            'category': 'Little pretty pets',
            'age': {
                'initial value': 0,
                'modifying': {'new value': {'+': ('age', 1)}}},
            'attack capacity': ....
            ...
            
            }
            
        Shall I remove it?
        """ 
        if 'age' in self:
            self['age'] += 1
    
    def die(self, cause = 'natural deth'):
        #print 'die'
        # self.parent_ecosystem.delete_organism(self) # parent_ecosystem tells biotope to erase organism from it
        if print_deths:        
            print 'dying', self.__str__(list_of_attributes = ('category', 'age', 'energy reserve')), cause        
        elif print_killed and cause == 'killed by a predator':
            print 'dying', self.__str__(list_of_attributes = ('category', 'age', 'energy reserve')), cause                    
        self.parent_ecosystem.new_deads.append(self)
