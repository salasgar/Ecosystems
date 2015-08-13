# GEOLOGY EXAMPLE

from Geology_settings import altitude, water_depth

_sunlight = {
    'matrix size': (25, 25),
    'initial value #x #y': 0,
}

_temperature = {
    'matrix size': (20, 20),
    'initial value #x #y': 10.0,
    'value after updating #x #y': {
        'help':
        """
            Each cycle the temperature is increased by sunlight, but a
            percentage of the accumulated heat is lost in every cycle.
        """,
        '*': (
            # this is the proportion (85 per cent) of the heat that remains in
            # the biotope:
            0.85,
            {'+': (
                # the new value depends on the previous value:
                {'#biotope temperature': ('#x', '#y')},
                {'#biotope sunlight': ('#x', '#y')}
            )}
        )},
    # The values of the matrix of sunlight is updated every 1 cycle.
    'update once every': 1
}

ecosystem_settings = {
    'biotope': {
        'size': (200, 100),
        'biotope features': {
            'sunlight': _sunlight,
            'temperature': _temperature,
            'water depth': water_depth,
            'altitude': altitude
        }
    },
    'organisms': {
        'category name': {
            'initial number of organisms': 1,
            'genes': {
                'actions sequence': {
                    'initial value': []
                }
            }
        }
    }

}