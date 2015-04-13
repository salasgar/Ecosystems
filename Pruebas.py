Speed = 0
Attack_capacity = 1
Defense_capacity = 2
Do_photosynthesis = 3
Energy = 4
Age = 5
Coordinates = 6

NUM_PARAMETERS = 7

class Organism:
    Parameters = []
    Parameter_location = []
    
    def __init__(self, Data):
        self.Parameters = [None]
        self.Parameter_location = [0 for i in range(NUM_PARAMETERS)]
        location = 1
        for (parameter, value) in Data:
            self.Parameter_location[parameter] = location
            self.Parameters += [value]
            location += 1
    
    def __getitem__(self, parameter):
        return self.Parameters[self.Parameter_location[parameter]]
        
    def __setitem__(self, parameter, value):
        self.Parameters[self.Parameter_location[parameter]] = value
        
Data1 = [(Attack_capacity, 7.3), (Energy, 50.0), (Coordinates, (23, 54)), (Age, 10)]

Data2 = [(Defense_capacity, 49), (Speed, 5.0), (Do_photosynthesis, False), (Coordinates, (3, 4)), (Age, 20)]

Organism1 = Organism(Data1)

Organism2 = Organism(Data2)

# Mira lo sencillo que es de usar:

print Organism1[Attack_capacity]

print "Le cambiamos el valor a un gen:"

Organism1[Attack_capacity] = 2.4

print Organism1[Attack_capacity]

print "intentamos acceder a un gen que no posee:"

print Organism1[Speed]

print "Estos son los valores almacenados:"

print Organism1.Parameters

print Organism1.Parameter_location


print "Ahora las coordenadas:"

SIZE_X, SIZE_Y = 200, 100

print "Coordenadas en formato lista:"
    
X = 0
Y = 1

coords = [7, 3]

print coords

coords[X] = coords[Y] + 1

print coords

print "Coordenadas en formato clase:"

class Coordenadas:
    Valores = [0, 0]
    
    def __init__(self, V):
        self.Valores = list(V)
        
    def __init__(self, x, y):
        self.Valores = [x, y]
        
    def __getitem__(self, c):
        return self.Valores[c]
        
    def __setitem__(self, c, value):
        self.Valores[c] = value % (SIZE_X, SIZE_Y)[c]
        
    def __str__(self):
        return str(tuple(self.Valores))
        
coords = Coordenadas(7, 3)

print coords

coords[X] = coords[Y] + 1

print coords

coords[X], coords[Y] = (504, 504)  # se asignan los valores modulo SIZE_X y SIZE_Y

print coords, "  <--- Nota que 504 modulo 200 no es igual que 504 modulo 100\n"

print "Ahora el biotopo:"

class Biotope:
    Array = []
    
    def __init__(self):
        self.Array = [[None for i in range(SIZE_Y)] for j in range(SIZE_X)]
        
    def __getitem__(self, coords):
        return self.Array[coords[0] % SIZE_X][coords[1] % SIZE_Y]
        
    def __setitem__(self, coords, value):
        self.Array[coords[0] % SIZE_X][coords[1] % SIZE_Y] = value

Biotopo = Biotope()

Biotopo[5, 6] = 'Organismo Pepito'
Biotopo[1007, 1008] = 'Organisma Antonieta'

print Biotopo[205, 206], "   <--- Nota que (205, 206) es igual a (5, 6) modulo (SIZE_X, SIZE_Y)"
print Biotopo[7, 8], "   <--- Nota que (7, 8) es igual a (1007, 1008) modulo (SIZE_X, SIZE_Y)"




