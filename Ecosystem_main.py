from GUI import GUI
# from time import sleep  # To remove
#import Biotope
#import Organism

def complete_with_default_values(experiment):
    if !('biotope' in experiment.keys()):
        experiment['biotope']= {
            'size': (100, 200),
        	'featuremaps': None }
    # TO DO More things    

def generate_functions(dictionary):
    
    """
    Este método lo que hace es recorrer todo el diccionario de Experiment e ir sustituyendo donde pone:
    
    {'type': 'random function', 
     'name': 'gaussian',
     'mean': 0,
     'variance': 1}
     
    por una función de verdad, que devuelve valores aleatorios.

    """
    if 'type' in dictionary:
        if dictionary['type'] == 'random function':
            return Tools.random_function_maker(dictionary)
        elif dictionary['type'] == 'outlay function':
            return Tools.outlay_function_maker(dictionary)
        elif dictionary['type'] == 'interpreted function':
            return Tools.interpreted_function_maker(dictionary)
    else:
        """
            Si dictionary no es la descripción de una función, entonces llamamos recursivamente a generate_function, 
            para seguir profundizando dentro del diccionario, en busca de funciones para sustituirlas:
        """
        for x in dictionary:
            if type(dictionary[x]) == dict:
                dictionary[x] = generate_functions(dictionary[x])
            else:
                """                
                   Si uno de los valores del diccionario es una lista, la recorremos: 
                """
                if hasattr(dictionary[x], __iter__):
                    for i in dictionary[x]:
                        """
                        Y si encontramos un diccionario, llamamos recursivamente a generate_functions:
                        """
                        if type(dictionary[x][i]) == dict:
                            dictionary[x][i] = generate_functions(dictionary[x][i]) 
                else:
                    """
                    Y si lo que nos encontramos es un número, entonces lo sustituimos por una función que devuelve ese número.
                    ¿Por qué? Porque así se simplifica la función initialize_organisms, ya que no se tiene que preocupar de si
                    'initial values' es un número o una función. Simplemente, como sabe que todos los valores son funciones,
                    llama a:
                    
                        set_of_organisms['genes'][gene]['initial values']()
                        
                    o a:
                    
                        set_of_organisms['status'][status]['initial values']()
                        
                    que le devuelven o bien un valor fijo, o bien un valor aleatorio
                    
                    Falta arreglarlo para cuando el valor fijo es un array
                    """
                    if (type(dictionary[x])== int) or (type(dictionary[x]]) == float):
                        dictionary[x] = lambda: dictionary[x]
    return dictionary

class Ecosystem(object):

    def __init__(self, experiment):
        """
            Esta función modifica experiment, añadiendole aquellos valores de los que experiment no dice nada porque se sobreentienden
            o porque se la suda:
        """
        complete_with_default_values(experiment)
        """
            Esta función modifica experiment, sustituyendo las descripciones de funciones por funciones de verdad:
        """
        generate_functions(experiment)
        self.experiment = experiment
        """
            Creamos el biotopo antes que los organismos, porque si no no tenemos dónde meterlos cuando los creamos, ni podemos asignarles
            un location ni nada:
        """
        self.initialize_biotope(self.experiment['biotope'])
        self.initialize_organisms(self.experiment['organisms'])
        # self.initialize_featuremaps(experiment['featuremaps'])  """ This is included in self.initialize_biotope

    def initialize_biotope(self, experiment_biotope_data):
        pass  # TODO

    def initialize_organisms(self, experiment_organisms_data):
        for set_of_organisms in experiment_organisms_data:
            for N in range(experiment_organisms_data['number of organisms']):
                """
                    Creamos un organismo de momento solo con un atributo:
                """
                organism = {'location': self.biotope.seek_free_location()}
                """
                    Le vamos añadiendo genes, llamando a las funciones que generan los valores iniciales
                    (que pueden ser aleatorios o fijos):
                """
                for gene in set_of_organisms['genes']:
                    organism[gene] = set_of_organisms['genes'][gene]['initial values']()
                for status in set_of_organisms['status']:
                    organism[status] = set_of_organisms['status'][status]['initial values']()
                """
                    Y metemos el organismo en el ecosistema:                    
                """
                self.add_organism(organism)
                

    def evolve(self):
        # Biotope actions
        self.biotope.evolve()
    
        # Organisms actions
        # TODO: Adaptar a nuevos métodos
    
        for organism in self.organisms:
            # Actions
            organism.move(self)

            # Procreation and death of organism:
            organism.procreate(self)
            org_status = organism.age(self)
            if org_status == 'Dead':
                self.organisms.remove(organism)

        self.organisms += self.newborns
        self.newborns = []
        """
        # print 'Num of organisms + newborns: %d' % len(self.organisms)


def main():
    # create Ecosystem
    experiment = None
    ecosystem = Ecosystem(experiment)
    # Add initial organisms to the ecosystem:
    ecosystem.create_organisms(initial_settings.initial_organisms)

    gui = GUI(ecosystem)
    # Loop
    time = 0
    while (len(ecosystem.organisms) > 0) and (time < 300):
        # TODO: Define correct condition
        ecosystem.evolve()
        gui.handle_events()
        gui.draw_ecosystem()
        # sleep(0.1)  # To remove
        time += 1
        if time % 10 == 0:
            print ("time =", time, "Num of organisms =",
                   len(ecosystem.organisms))
    gui.delete()

if __name__ == '__main__':
    main()
