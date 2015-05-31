from GUI import GUI
from Tools import *
from Biotope import Biotope
from Settings import *
from Organism import *
from time import *

# from time import sleep  # To remove
# import Biotope
# import Organism

things_to_see = {
    "https://www.coursera.org/course/ml",
    ""
}

DEFAULT_SETTINGS = {}

    
class Ecosystem(object):
    """ Attributes:
    self.biotope
    self.organisms_list
    self.newborns    
    self.outlays
    self.constraints
    """

    def __init__(self, ecosystem_settings, default_settings = DEFAULT_SETTINGS):
        self.load_settings(ecosystem_settings, default_settings)
        self.initialize_biotope()
        self.initialize_outlays()
        self.initialize_constraints()
        self.newborns = []
        self.new_deads = []
        self.initialize_organisms()
        self.storage_capacities_dictionary = {
            'energy reserve': 'energy storage capacity',
            'water reserve': 'water storage capacity'
            # to do: add more thigs
            }
        self.initialize_statistics()
        
    def load_settings(self, ecosystem_settings, default_settings):
        print 'load_settings'
        if 'ecosystem' in default_settings:            
            merge_dictionaries(
                dictionary_to_be_completed = ecosystem_settings,
                dictionary_to_complete_with = default_settings['ecosystem'])
        if is_dictionary(ecosystem_settings['organisms']):
            ecosystem_settings['organisms'] = [ecosystem_settings['organisms']]
        for category in ecosystem_settings['organisms']:
            if not 'number of organisms' in category:
                category['number of organisms'] = 1
            if not 'genes' in category:
                category['genes'] = {}
          
            category['genes'] = unpack_genes(category['genes'])

            if not 'list of reserve substances' in category['genes']:
                if 'energy reserve' in category['genes']:
                    category['genes']['list of reserve substances'] = {'value, not function': ['energy reserve']}
                else:
                    category['genes']['list of reserve substances'] = {'value, not function': []}                    
            if not 'actions sequence' in category['genes']:
                category['genes']['actions sequence'] = []
                actions_sequence = category['genes']['actions sequence']
                organisms_genes_list = extract_genes_names(category['genes'])
                if 'speed' in organisms_genes_list:
                    actions_sequence.append('move')                 
                if ('attack capacity' in organisms_genes_list) or ('hunt radius' in organisms_genes_list):
                    actions_sequence.append('hunt')                   
                if 'list of reserve substances' in organisms_genes_list:
                    actions_sequence.append('interchange substances with the biotope')
                    actions_sequence.append('interchange substances with other organisms')                    
                if 'sex' in organisms_genes_list:
                    actions_sequence.append('fertilize other organisms')                 
                if 1 + 1 == 2:
                    actions_sequence.append('procreate')
                    actions_sequence.append('stay alive')   
                category['genes']['actions sequence'] = actions_sequence
            if ('hunt' in category['genes']['actions sequence']) and not ('hunt radius' in extract_genes_names(category['genes'])):
                category['genes']['hunt radius'] = 1.5
        self.settings = ecosystem_settings  
        #print_dictionary( self.settings     )         

    def initialize_biotope(self):
        print 'initialize_biotope'
        self.biotope = Biotope(settings = self.settings['biotope'], parent_ecosystem = self)
                
    def initialize_outlays(self):
        print 'initialize_outlays'
        self.outlays = {}
        for action in self.settings['outlays']:
            self.outlays[action] = {}
            for reserve_substance in self.settings['outlays'][action]:
                self.outlays[action][reserve_substance] = make_function(self.settings['outlays'][action][reserve_substance])
    
    def initialize_constraints(self):
        print 'initialize_constraints'
        self.constraints = {}
        for action in self.settings['constraints']:
            self.constraints[action] = make_function(self.settings['constraints'][action])        
    
    def initialize_statistics(self):
        print 'initialize_statistics'
        self.statistics = {
            'number of natural deths': 0,
            'number of killed by a predator': 0,
            'number of births': 0}
        for category in self.settings['organisms']:
            if 'category' in category:
                self.statistics['number of births of ' + category['category']] = 0
                self.statistics['number of natural deths of ' + category['category']] = 0
                self.statistics['number of ' + category['category'] + ' killed by a predator'] = 0
            if 'list of reserve substances' in category['genes']:
                for reserve_substance in category['genes']['list of reserve substances']:
                    self.statistics['total amount of ' + reserve_substance] = 0
                    self.statistics['average amount of ' + reserve_substance] = 0
                    if 'category' in category:                    
                        self.statistics['total amount of ' + reserve_substance + ' in ' + category['category']] = 0
                        self.statistics['average amount of ' + reserve_substance + ' in ' + category['category']] = 0             
            for gene in extract_genes_names(category['genes']):
                self.statistics['average ' + gene] = 0
        
    def add_organism(self, organism):
        #print 'add organism'
        self.biotope.add_organism(organism)
        self.newborns.append(organism)  
        
    def delete_organism(self, organism):
        #print 'delete organism'
        self.biotope.delete_organism(organism['location'])
        if organism in self.newborns:
            del self.newborns[self.newborns.index(organism)]
        if organism in self.organisms_list:
            del self.organisms_list[self.organisms_list.index(organism)]
            # warning: list.index() can be very slow. We should use a double chain list            
        
    def size_x(self):
        return self.biotope['size'][0]

    def size_y(self):
        return self.biotope['size'][1]

    
    def initialize_organisms(self):
        print 'initialize_organisms'
        """ 
        PRE-CONDITIONS:
            This initialization must be called AFTER self.initialize_biotope, 
            because we use here Biotope.seek_free_location
        """
        for category in self.settings['organisms']:  # in Ecosystem.load_settings we make sure that self.settings['organisms'] is a list of (one or more) categories
            genes_settings = category['genes']
            all_genes = genes_settings.keys()
            for _ in range(category['number of organisms']):                
                new_organism = Organism(self, {'mutating genes': {}, 'variable genes': {}, 'list of reserve substances': []})
                # Load genes:
                for gene in genes_settings:
                    new_organism.add_gene(gene, genes_settings[gene], all_genes)
                # Load decisions:
                if 'decisions' in category:
                    for decision in category['decisions']:
                        new_organism.add_decision(decision, category['decisions'][decision])
                self.add_organism(new_organism) # This adds new_organism to self.newborns and to self.biotope in a random location
        self.organisms_list = self.newborns
        self.newborns = []

    def evolve(self):
        #print 'evolve'
        # Biotope actions:
        self.biotope.evolve()
        # Organisms actions:
        i = 0        
        while i < len(self.organisms_list):
            self.organisms_list[i].act()
            i += 1
            for dead_organism in self.new_deads:
                # the organism may be in self.organisms_list or in self.newborns:
                if dead_organism in self.organisms_list and self.organisms_list.index(dead_organism) < i:
                    i -= 1
                self.delete_organism(dead_organism) # this erases the organism from the biotope too
                #print "number of organisms", len(self.organisms_list)
            self.new_deads = []
        self.organisms_list += self.newborns
        self.newborns = []
        
        # print 'Num of organisms + newborns: %d' % len(self.organisms)

    def count(self, item, value):
        N = 0
        for organism in self.organisms_list:
            if item in organism and organism[item] == value:
                N += 1
        return N

def main():
    print " *"*30, "\nWe start NOW!"
    # create Ecosystem
    ecosystem = Ecosystem(ecosystem_settings2)
    
    """
    f = make_function({'and': (
                    {'>': ('energy reserve', 'energy reserve procreating threshold')}, 
                    {'randbool': 'procreating frequency'})})
    for organism in ecosystem.organisms_list:
        p = organism['procreate?'](organism)
        if p:
            print organism['energy reserve']
            print organism['energy reserve procreating threshold']
            print f(organism)
            print organism['procreate?'](organism)
            print p
        
    #return 0
    
    """
    
    enable_graphics = True
    time_lapse = 1
    make_pauses = False #not enable_graphics
    make_sleeps = False
    Total_time = 2000000
    
    """
    for i in range(Total_time):
        for organism in ecosystem.organisms_list:
            print "*"*10
            print "age {0}, energy reserve {1}, location {2}".format(organism['age'], organism['energy reserve'], organism['location'])
            for action in organism['actions sequence']:
                decision = action + '?'
                if decision in organism:
                    print decision, 
                    if organism[decision](organism):
                        print True, actions_dictionary[action](organism)
                    else:
                        print False
                else:
                    print action, actions_dictionary[action](organism)
            if ecosystem.constraints['die?'](organism):
                print 'die'
                print 'energy reserve', organism['energy reserve']
            else:
                print "doesn't die", organism['energy reserve']
            if raw_input('Exit? ').upper() == 'Y':
                break
        ecosystem.organisms_list += ecosystem.newborns
        ecosystem.newborns = []
        for organism in ecosystem.organisms_list:
            print organism['age'],
        print "\nnumber of organisms: {0}, newborns: {1}, new_deads: {2}".format(len(ecosystem.organisms_list), len(ecosystem.newborns), len(ecosystem.new_deads))
        if raw_input('Exit? ').upper() == 'Y':
            break
        
        
    return 0
    
    """
    
    
    if enable_graphics:
        gui = GUI(ecosystem)
    # Loop
    time = 0
    user_input = 'N'
    while (len(ecosystem.organisms_list) > 0) and (time < Total_time) and (user_input != 'Y') and (user_input != 'y'):
        if time % time_lapse == 0:
            print ("time =", time, "Num of organisms =",
                   len(ecosystem.organisms_list))
            if print_ages:
                print [organism['age'] for organism in ecosystem.organisms_list]
            if print_organisms:
                for organism in ecosystem.organisms_list:  
                    #print organism['age'], round(organism['energy reserve'], 2), organism['color'](organism)
                    print organism.__str__(list_of_attributes = ('age', 'energy reserve', 'color'))
                    #if organism['age'] > 100:
                    #    print ecosystem.constraints['die?'](organism)
            #print ecosystem.count('category', 'plant'), 'plants and', ecosystem.count('category', 'animal'), 'animals'
            if make_pauses:
                user_input = raw_input('exit? [Y/N]: ')                    
        if (user_input != 'y') and (user_input != 'Y'):
            ecosystem.evolve()
        if enable_graphics:
            gui.handle_events()
            gui.draw_ecosystem()
        if make_sleeps:
            sleep(1.0)  # To remove
        time += 1
    if enable_graphics:
        gui.delete()
                    
if __name__ == '__main__':
    main()
