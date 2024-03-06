from unittest.mock import patch
import numpy
from DataVisual import Array, Xparameter
import DataVisual.tables as Table

from DataVisual.future_table.tables import Length, Power, Area

parameter_1 = Length(
    long_label='Length 0',
    short_label='L0',
    values=numpy.linspace(0, 1, 100),
)

parameter_0 = Area(
    long_label='Area 1',
    short_label='A0',
    values=numpy.linspace(0, 1, 4),
)

y_parameter = Xparameter(
    name='Measurement',
    format_string="<20s",
    unit="1",
    long_label='Arbitrary measure',
    short_label='Arbit. measure'
)

y_parameter = Power(
    long_label='Power 1',
    short_label='P0',
    values=parameter_1.values**2 + 0.05 * numpy.random.rand(4, 100)
)

y_parameter.base_values

x_table = [parameter_0, parameter_1]

data = Array(
    x_table=Table.Xtable(x_table),
    y=y_parameter
)

figure = data.plot(x=parameter_1)

figure.show()
