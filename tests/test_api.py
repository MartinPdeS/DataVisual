#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch
import numpy
import pytest
from DataVisual import Array
from DataVisual import Table
from DataVisual.units import Length, Power, Area


@pytest.fixture
def mock_x_table_2() -> list:
    parameter_0 = Length(
        values=numpy.linspace(0, 1, 10),
        long_label='Length: 0',
        short_label='L: 0'
    )

    parameter_1 = Length(
        values=numpy.linspace(0, 4, 10),
        long_label='Length: 1',
        short_label='L: 1'
    )

    x_table = [parameter_0, parameter_1]

    return Table(x_table)


@pytest.fixture
def mock_x_table_3() -> list:
    parameter_0 = Length(
        values=numpy.linspace(0, 1, 10),
        long_label='Length: 0',
        short_label='L: 0'
    )

    parameter_1 = Length(
        values=numpy.linspace(0, 1, 10),
        long_label='Length: 1',
        short_label='L: 1'
    )

    parameter_2 = Area(
        values=numpy.linspace(0, 1, 10),
        long_label='Area: 1',
        short_label='A: 1'
    )

    x_table = [parameter_0, parameter_1, parameter_2]

    return Table(x_table)


@pytest.fixture
def mock_measure_2() -> list:
    measure = Power(
        long_label='Arbitrary measure',
        short_label='Arbit. measure',
        values=1 + 0.3 * numpy.random.rand(10, 10)
    )

    return measure


@pytest.fixture
def mock_measure_3() -> list:
    measure = Power(
        long_label='Arbitrary measure',
        short_label='Arbit. measure',
        values=1 + 0.3 * numpy.random.rand(10, 10, 10)
    )

    return measure


@patch("matplotlib.pyplot.show")
def test_plot_line(patch, mock_x_table_2, mock_measure_2):
    data = Array(
        x_table=mock_x_table_2,
        y=mock_measure_2
    )

    figure = data.plot(x=mock_x_table_2[1])

    figure.show()


@patch("matplotlib.pyplot.show")
def test_plot_std_line(patch, mock_x_table_3, mock_measure_3):
    parameter_0, parameter_1, parameter_2 = mock_x_table_3

    data = Array(
        x_table=mock_x_table_3,
        y=mock_measure_3,
    )

    figure = data.plot(x=parameter_1, std=parameter_2)

    figure.show()


@patch("matplotlib.pyplot.show")
def test_mean_plot_line(patch, mock_x_table_3, mock_measure_3):
    parameter_0, parameter_1, parameter_2 = mock_x_table_3

    data = Array(
        x_table=mock_x_table_3,
        y=mock_measure_3
    )

    data = data.mean(axis=parameter_0)

    figure = data.plot(x=parameter_1)

    figure.show()


@patch("matplotlib.pyplot.show")
def test_std_plot_line(patch, mock_x_table_3, mock_measure_3):
    parameter_0, parameter_1, parameter_2 = mock_x_table_3

    data = Array(
        x_table=mock_x_table_3,
        y=mock_measure_3
    )

    data = data.std(axis=parameter_0)

    figure = data.plot(x=parameter_1)

    figure.show()


@patch("matplotlib.pyplot.show")
def test_rsd_plot_line(patch, mock_x_table_3, mock_measure_3):
    parameter_0, parameter_1, parameter_2 = mock_x_table_3

    data = Array(
        x_table=mock_x_table_3,
        y=mock_measure_3
    )

    data = data.rsd(axis=parameter_0)

    figure = data.plot(x=parameter_1)

    figure.show()


# -
