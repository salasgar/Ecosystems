from math import sin, cos, exp
from random import random, randint

_geology_matrix_size = (100, 100)
_geology_updating_frequency = 1


class AltitudeCreator:

    def __init__(self, n_of_mountains):
        self.mountains_list = []
        for i in range(n_of_mountains):
            self.add_mountain()

    def add_mountain(self):
        # mountain = (center_x, center_y, altitude, pointedness)
        mountain = (random(), random(), random(), 10 * random())
        self.mountains_list.append(mountain)

    def get_value(self, x, y):
        result = 0
        for (center_x, center_y, altitude, pointedness) in self.mountains_list:
            result += altitude * exp(
                -(
                    (x-center_x)**2 +
                    (y-center_y)**2
                ) * pointedness
            )
        return result


_altitude_creator = AltitudeCreator(n_of_mountains=randint(3, 10))

"""
def _water_flow_auxiliar_function(
    coefficient,
    water_depth_0,
    altitude_0,
    water_depth_1,
    altitude_1
        ):
    print 'coefficient', coefficient  # ***
    return coefficient * max(
        - water_depth_0,
        min(
            water_depth_1,
            water_depth_1 + altitude_1 - water_depth_0 - altitude_0
        )
    )
"""


def _water_flow_auxiliar_function(*inputs):
    if len(inputs) == 5:
        (
            coefficient,
            water_depth_0,
            altitude_0,
            water_depth_1,
            altitude_1
        ) = inputs
    else:
        print inputs
        exit()
    return coefficient * max(
        - water_depth_0,
        min(
            water_depth_1,
            water_depth_1 + altitude_1 - water_depth_0 - altitude_0
        )
    )


altitude = {
    'matrix size': _geology_matrix_size,
    'initial value #x #y':
        lambda ecosystem, x, y: _altitude_creator.get_value(x, y),
    'value after updating #x #y': {'+': (
        {'#biotope altitude': ('#x', '#y')},
        # EROSION:
        {'function': (
            _water_flow_auxiliar_function,
            0.015,
            {'#biotope water depth': ('#x', '#y')},
            {'#biotope altitude': ('#x', '#y')},
            {'#biotope water depth': (
                {'+': ('#x', 'normalized abcissa unit')},
                '#y'
            )},
            {'#biotope altitude': (
                {'+': ('#x', 'normalized abcissa unit')},
                '#y'
            )}
        )},
        {'function': (
            _water_flow_auxiliar_function,
            0.015,
            {'#biotope water depth': ('#x', '#y')},
            {'#biotope altitude': ('#x', '#y')},
            {'#biotope water depth': (
                {'-': ('#x', 'normalized abcissa unit')},
                '#y'
            )},
            {'#biotope altitude': (
                {'-': ('#x', 'normalized abcissa unit')},
                '#y'
            )}
        )},
        {'function': (
            _water_flow_auxiliar_function,
            0.015,
            {'#biotope water depth': ('#x', '#y')},
            {'#biotope altitude': ('#x', '#y')},
            {'#biotope water depth': (
                '#x',
                {'+': ('#y', 'normalized ordinate unit')}
            )},
            {'#biotope altitude': (
                '#x',
                {'+': ('#y', 'normalized ordinate unit')}
            )}
        )},
        {'function': (
            _water_flow_auxiliar_function,
            0.015,
            {'#biotope water depth': ('#x', '#y')},
            {'#biotope altitude': ('#x', '#y')},
            {'#biotope water depth': (
                '#x',
                {'-': ('#y', 'normalized ordinate unit')}
            )},
            {'#biotope altitude': (
                '#x',
                {'-': ('#y', 'normalized ordinate unit')}
            )}
        )},
        {'function': (
            _water_flow_auxiliar_function,
            0.01,
            {'#biotope water depth': ('#x', '#y')},
            {'#biotope altitude': ('#x', '#y')},
            {'#biotope water depth': (
                {'+': ('#x', 'normalized abcissa unit')},
                {'+': ('#y', 'normalized ordinate unit')}
            )},
            {'#biotope altitude': (
                {'+': ('#x', 'normalized abcissa unit')},
                {'+': ('#y', 'normalized ordinate unit')}
            )}
        )},
        {'function': (
            _water_flow_auxiliar_function,
            0.01,
            {'#biotope water depth': ('#x', '#y')},
            {'#biotope altitude': ('#x', '#y')},
            {'#biotope water depth': (
                {'-': ('#x', 'normalized abcissa unit')},
                {'+': ('#y', 'normalized ordinate unit')}
            )},
            {'#biotope altitude': (
                {'-': ('#x', 'normalized abcissa unit')},
                {'+': ('#y', 'normalized ordinate unit')}
            )}
        )},
        {'function': (
            _water_flow_auxiliar_function,
            0.01,
            {'#biotope water depth': ('#x', '#y')},
            {'#biotope altitude': ('#x', '#y')},
            {'#biotope water depth': (
                {'+': ('#x', 'normalized abcissa unit')},
                {'-': ('#y', 'normalized ordinate unit')}
            )},
            {'#biotope altitude': (
                {'+': ('#x', 'normalized abcissa unit')},
                {'-': ('#y', 'normalized ordinate unit')}
            )}
        )},
        {'function': (
            _water_flow_auxiliar_function,
            0.01,
            {'#biotope water depth': ('#x', '#y')},
            {'#biotope altitude': ('#x', '#y')},
            {'#biotope water depth': (
                {'-': ('#x', 'normalized abcissa unit')},
                {'-': ('#y', 'normalized ordinate unit')}
            )},
            {'#biotope altitude': (
                {'-': ('#x', 'normalized abcissa unit')},
                {'-': ('#y', 'normalized ordinate unit')}
            )}
        )}
    )},
    'update once every': _geology_updating_frequency
}


def rain(x, y, time):
    # PRECONDITION:  0 <= x <= 1,  0 <= y <= 1
    return (1 + sin(float(time)/50))*(1+cos(x+y+x*y+(1+x-y)**2)+random()/4)


def _water_flow_auxiliar_function(
    coefficient,
    water_depth_0,
    altitude_0,
    water_depth_1,
    altitude_1
        ):
    return coefficient * max(
        - water_depth_0,
        min(
            water_depth_1,
            water_depth_1 + altitude_1 - water_depth_0 - altitude_0
        )
    )


water_depth = {
    'matrix size': _geology_matrix_size,
    'initial value #x #y': 0,
    'value after updating #x #y': {'max': (
        0,
        {'+': (
            # RAIN:
            {'function': (rain, '#x', '#y', 'time')},
            # EVAPORATION:
            {'*': (
                -0.01,
                {'#biotope temperature': ('#x', '#y')}
            )},
            # FLOW:
            {'function': (
                _water_flow_auxiliar_function,
                0.15,
                {'#biotope water depth': ('#x', '#y')},
                {'#biotope altitude': ('#x', '#y')},
                {'#biotope water depth': (
                    {'+': ('#x', 'normalized abcissa unit')},
                    '#y'
                )},
                {'#biotope altitude': (
                    {'+': ('#x', 'normalized abcissa unit')},
                    '#y'
                )}
            )},
            {'function': (
                _water_flow_auxiliar_function,
                0.15,
                {'#biotope water depth': ('#x', '#y')},
                {'#biotope altitude': ('#x', '#y')},
                {'#biotope water depth': (
                    {'-': ('#x', 'normalized abcissa unit')},
                    '#y'
                )},
                {'#biotope altitude': (
                    {'-': ('#x', 'normalized abcissa unit')},
                    '#y'
                )}
            )},
            {'function': (
                _water_flow_auxiliar_function,
                0.15,
                {'#biotope water depth': ('#x', '#y')},
                {'#biotope altitude': ('#x', '#y')},
                {'#biotope water depth': (
                    '#x',
                    {'+': ('#y', 'normalized ordinate unit')}
                )},
                {'#biotope altitude': (
                    '#x',
                    {'+': ('#y', 'normalized ordinate unit')}
                )}
            )},
            {'function': (
                _water_flow_auxiliar_function,
                0.15,
                {'#biotope water depth': ('#x', '#y')},
                {'#biotope altitude': ('#x', '#y')},
                {'#biotope water depth': (
                    '#x',
                    {'-': ('#y', 'normalized ordinate unit')}
                )},
                {'#biotope altitude': (
                    '#x',
                    {'-': ('#y', 'normalized ordinate unit')}
                )}
            )},
            {'function': (
                _water_flow_auxiliar_function,
                0.1,
                {'#biotope water depth': ('#x', '#y')},
                {'#biotope altitude': ('#x', '#y')},
                {'#biotope water depth': (
                    {'+': ('#x', 'normalized abcissa unit')},
                    {'+': ('#y', 'normalized ordinate unit')}
                )},
                {'#biotope altitude': (
                    {'+': ('#x', 'normalized abcissa unit')},
                    {'+': ('#y', 'normalized ordinate unit')}
                )}
            )},
            {'function': (
                _water_flow_auxiliar_function,
                0.1,
                {'#biotope water depth': ('#x', '#y')},
                {'#biotope altitude': ('#x', '#y')},
                {'#biotope water depth': (
                    {'-': ('#x', 'normalized abcissa unit')},
                    {'+': ('#y', 'normalized ordinate unit')}
                )},
                {'#biotope altitude': (
                    {'-': ('#x', 'normalized abcissa unit')},
                    {'+': ('#y', 'normalized ordinate unit')}
                )}
            )},
            {'function': (
                _water_flow_auxiliar_function,
                0.1,
                {'#biotope water depth': ('#x', '#y')},
                {'#biotope altitude': ('#x', '#y')},
                {'#biotope water depth': (
                    {'+': ('#x', 'normalized abcissa unit')},
                    {'-': ('#y', 'normalized ordinate unit')}
                )},
                {'#biotope altitude': (
                    {'+': ('#x', 'normalized abcissa unit')},
                    {'-': ('#y', 'normalized ordinate unit')}
                )}
            )},
            {'function': (
                _water_flow_auxiliar_function,
                0.1,
                {'#biotope water depth': ('#x', '#y')},
                {'#biotope altitude': ('#x', '#y')},
                {'#biotope water depth': (
                    {'-': ('#x', 'normalized abcissa unit')},
                    {'-': ('#y', 'normalized ordinate unit')}
                )},
                {'#biotope altitude': (
                    {'-': ('#x', 'normalized abcissa unit')},
                    {'-': ('#y', 'normalized ordinate unit')}
                )}
            )}
        )}
    )},
    'update once every': _geology_updating_frequency
}
