
#-- Substance codes ---------------------
# Substances spread in the biotope:
NO_SUBSTANCE = 0
WATER = 1
CARBON_DIOXIDE = 2
OXIGEN = 3
NITRATE = 4
PHOSPHATE = 5
POISON = 10
POISON1 = 11
POISON2 = 12
FOOD = 13
FOOD1 = 14
FOOD2 = 15

TEMPERATURE = 101  
SUNLIGHT = 102  # Is there an equivalence between ENERGY and SUNLIGHT  ???
RAIN = 103 # The presence of RAIN increases the amount of WATER in the soil, and in the end, if there is enought humidity, it become DEPTH
ALTITUDE = 104
DEPTH = 105  # Depth of a sea, a lake or a river

# Substances inside organisms:
WATER_RESERVE = 201
NITRATE_RESERVE = 204
PHOSPHATE_RESERVE = 205

class Substance(Tools.Matrix):
    
    def __init__(self, substance_metadata):
        self.substance_metadata = substance_metadata
        (self.size_x, self.size_y) = self.substance_metadata['dimensions']
        self.block_size = self.substance_metadata['block_size']
        super(substance, self).__init__(size_x // block_size,
                                        size_y // block_size,
                                        value = 0)

    def set_value(self, coordinates, value):
        (i, j) = (int(coordinates[0] // self.block_size), 
                  int(coordinates[1] // self.block_size))
        self[i, j] = value
        
    def get_value(self, coordinates):
        (i, j) = (int(coordinates[0] // self.block_size),
                  int(coordinates[1] // self.block_size))
        return self[i, j]

    def get_concentration(self, coordinates):
        """ 
            It returns the amount of substance divided by the block_area.
        """
        block_area = self.block_size ** 2
        return self.get_value(location) / block_area
        
    def variate_value(self, coordinates, variation):
        (i, j) = (int(coordinates[0] // self.block_size),
                  int(coordinates[1] // self.block_size))
        self[i, j] += value
        
    def evolve(self):
        aux_matrix = Tools.Matrix(self.size_x, self.size_y)
        spread_speed = self.substance_metadata['spread_speed']
        for i in range(self.size_x):
            for j in range(self.size_y):
                aux_matrix[i, j] = spread_speed * \
                    math.fsum(self[i+k, j+m] for k in (-1, 0, 1)\
                    for m in (-1, 0, 1)) / 9 + (1-spread_speed)*self[i,j]
        # TODO: Simplify this operation
        self.data = aux_matrix.data

    def set_random_values(self, lowerBond = 0, higherBond = 100):
        for i in range(self.size_x):
            for j in range(self.size_y):
                self[i,j] = lowerBond + random() * (higherBond - lowerBond)