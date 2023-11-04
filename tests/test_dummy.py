#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from DataVisual import DataV, Xparameter
import DataVisual.tables as Table

def test_plottings():

    parameter_0 = Xparameter(
        values=numpy.linspace(0, 1, 3),
        name='parameter 0',
        format=".2e",
        unit="m",
        long_label='parameter 0 long label',
        short_label='parameter 0 short label'
    )

    parameter_1 = Xparameter(
        values=numpy.linspace(0, 3, 100),
        name='parameter 1',
        format=".2e",
        unit="m",
        long_label='parameter 1 long label',
        short_label='parameter 1 short label'
    )

    y_parameter = Xparameter(
        name='Qsca',
        format="<20s",
        unit="1",
        long_label='Scattering efficiency',
        short_label='Qsca'
    )

    x_table = [parameter_0, parameter_1]

    y_parameter.values = 1 + 0.3 * numpy.random.rand(1, 3, 100)

    data = DataV(
        array=y_parameter.values,
        x_table=Table.Xtable(x_table),
        y_table=Table.Ytable([y_parameter])
    )

    data.plot(x=parameter_1, y=y_parameter).show()

# -
