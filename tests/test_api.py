#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch
import numpy
from DataVisual import DataV, Xparameter
import DataVisual.tables as Table


@patch("matplotlib.pyplot.show")
def test_plottings(patch):
    parameter_0 = Xparameter(
        values=numpy.linspace(0, 1, 4),
        name='parameter 0',
        format=".2e",
        unit="[A.U.]",
        long_label='Parameter: 0',
        short_label='Param: 0'
    )

    parameter_1 = Xparameter(
        values=numpy.linspace(0, 4, 100),
        name='parameter 1',
        format=".2e",
        unit="[A.U.]",
        long_label='Parameter: 1',
        short_label='Param: 1'
    )

    y_parameter = Xparameter(
        name='Measurement',
        format="<20s",
        unit="1",
        long_label='Arbitrary measure',
        short_label='Arbit. measure'
    )

    x_table = [parameter_0, parameter_1]

    y_parameter.values = 1 + 0.3 * numpy.random.rand(4, 100)

    data = DataV(
        array=y_parameter.values,
        x_table=Table.Xtable(x_table),
        y_parameter=y_parameter
    )

    figure = data.plot(x=parameter_1)

    figure.show()

# -
