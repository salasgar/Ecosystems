# SUBSTANCES


"""
	All substances are a subclass of this one:
"""

class Substance:
	def __init__(self, parent_biotope):
		self.biotope = parent_biotope
		self.cycle_n = 0
	def reset(self):
		pass
	def get_amount_at_location(self, location):
		return 0.0
	def add(self, location, amount):
		pass
	def subtract(self, location, amount):
		pass
	def evolve(self):
		pass


def gauss_bell(x, mean, variance):
	return = (variance * sqrt(2.0 * pi() * exp(((x - mean)/variance)**2))**(-1)

# EXAMPLE OF SUBSTANCES:


class Rain(Substance):
	def __init__(self, parent_biotope, average_intensity, width):
		self = Substance(parent_biotope)
		self.center = parent_biotope.get_random_location()
		self.average_intensity = average_intensity
		self.width = width
		self.intensity = gauss(mean = self.average_intensity, variance = average_intensity)
		self.wind_speed = (gauss(0, 5), gauss(0, 5))
	def get_amount_at_location(self, location):
		(x, y) = location
		(x0, y0) = self.center
		gauss_x = gauss_bell(x, mean = x0, variance = self.width)
		gauss_y = gauss_bell(y, mean = y0, variance = self.width)
		return  gauss_x * gauss_y * max(intensity, 0)
	def evolve(self):
		self.cycle_n += 1
		self.intensity = 0.8 * self.intensity + 0.2 * gauss(self.average_intensity, average_intensity)
			0.8 * self.wind_speed[0] + 0.2 * gauss(0, 5),
			0.8 * self.wind_speed[1] + 0.2 * gauss(0, 5))
		self.center = (
			roundint(self.center[0] + self.wind_speed[0]),
			roundint(self.center[1] + self.wind_speed[1]))

class Biotope_water(Substance):
	def __init__(self, parent_biotope, rain_average_intensity):
		self = Substance(parent_biotope)
		self.size_x, self.size_y = self.parent_biotope.size
		rain_area_width = min(self.size_x, self.size_y)/4.0
		self.rain = Rain(parent_biotope, rain_average_intensity, rain_area_width)
		self.matrix = Matrix(*self.size_x, self.size_y, value = 0)
	def evaporation_ratio(self, x, y):
		return uniform(0, 0.5 * y/self.size_y)
	def get_amount_at_location(self, location):
		return self.matrix[location]
	def add(self, location, amount):
		self.matrix[location] += amount
	def subtract(self, location, amount):
		self.matrix[location] -= amount
	def evolve(self):
		axuliary_matrix = self.matrix.deep_copy()
		for x in range(self.size_x):
			for y in range(self.size_y):
				for i in range(-4, 4):
					for j in range(-4, 4):
						
				auxiliary_matrix[x, y] += self.rain.get_amount_at_location([x, y])
				auxiliary_matrix[x, y] -= auxiliary_matrix[x, y] * self.evaporation_ratio(x, y)
				








