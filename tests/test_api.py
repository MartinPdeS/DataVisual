#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import patch
import numpy as np
import pytest
from DataVisual import Array, Table
from DataVisual.units import Length, Power, Area


@pytest.fixture
def mock_x_table_2() -> Table:
    """
    Fixture to create a mock Table with two Length parameters.

    Returns:
        Table: A Table object containing two Length parameters.
    """
    parameter_0 = Length(
        base_values=np.linspace(0, 1, 10),
        long_label='Length: 0',
        short_label='L: 0'
    )

    parameter_1 = Length(
        base_values=np.linspace(0, 4, 10),
        long_label='Length: 1',
        short_label='L: 1'
    )

    return Table([parameter_0, parameter_1])


@pytest.fixture
def mock_x_table_3() -> Table:
    """
    Fixture to create a mock Table with two Length parameters and one Area parameter.

    Returns:
        Table: A Table object containing two Length parameters and one Area parameter.
    """
    parameter_0 = Length(
        base_values=np.linspace(0, 1, 10),
        long_label='Length: 0',
        short_label='L: 0'
    )

    parameter_1 = Length(
        base_values=np.linspace(0, 1, 10),
        long_label='Length: 1',
        short_label='L: 1'
    )

    parameter_2 = Area(
        base_values=np.linspace(0, 1, 10),
        long_label='Area: 1',
        short_label='A: 1'
    )

    return Table([parameter_0, parameter_1, parameter_2])


@pytest.fixture
def mock_measure_2() -> Power:
    """
    Fixture to create a mock Power measure with a 10x10 array of random values.

    Returns:
        Power: A Power object with random values.
    """
    return Power(
        long_label='Arbitrary measure',
        short_label='Arbit. measure',
        base_values=1 + 0.3 * np.random.rand(10, 10)
    )


@pytest.fixture
def mock_measure_3() -> Power:
    """
    Fixture to create a mock Power measure with a 10x10x10 array of random values.

    Returns:
        Power: A Power object with random values.
    """
    return Power(
        long_label='Arbitrary measure',
        short_label='Arbit. measure',
        base_values=1 + 0.3 * np.random.rand(10, 10, 10)
    )


@patch("matplotlib.pyplot.show")
def test_plot_line(mock_show, mock_x_table_2, mock_measure_2):
    """
    Test the basic line plot functionality of the Array class.

    Args:
        mock_show (MagicMock): Mocked version of plt.show to prevent actual plot display.
        mock_x_table_2 (Table): Fixture providing the x_table with two parameters.
        mock_measure_2 (Power): Fixture providing the y data as a Power object.
    """
    data = Array(x_table=mock_x_table_2, y=mock_measure_2)
    data.plot(x=mock_x_table_2[1])


@patch("matplotlib.pyplot.show")
def test_plot_std_line(mock_show, mock_x_table_3, mock_measure_3):
    """
    Test plotting with standard deviation shading in the Array class.

    Args:
        mock_show (MagicMock): Mocked version of plt.show to prevent actual plot display.
        mock_x_table_3 (Table): Fixture providing the x_table with three parameters.
        mock_measure_3 (Power): Fixture providing the y data as a Power object.
    """
    parameter_1, parameter_2 = mock_x_table_3[1], mock_x_table_3[2]
    data = Array(x_table=mock_x_table_3, y=mock_measure_3)
    data.plot(x=parameter_1, std=parameter_2)


@patch("matplotlib.pyplot.show")
def test_mean_plot_line(mock_show, mock_x_table_3, mock_measure_3):
    """
    Test plotting the mean of data along a specific axis in the Array class.

    Args:
        mock_show (MagicMock): Mocked version of plt.show to prevent actual plot display.
        mock_x_table_3 (Table): Fixture providing the x_table with three parameters.
        mock_measure_3 (Power): Fixture providing the y data as a Power object.
    """
    parameter_0, parameter_1 = mock_x_table_3[0], mock_x_table_3[1]
    data = Array(x_table=mock_x_table_3, y=mock_measure_3).mean(axis=parameter_0)
    data.plot(x=parameter_1)


@patch("matplotlib.pyplot.show")
def test_std_plot_line(mock_show, mock_x_table_3, mock_measure_3):
    """
    Test plotting the standard deviation of data along a specific axis in the Array class.

    Args:
        mock_show (MagicMock): Mocked version of plt.show to prevent actual plot display.
        mock_x_table_3 (Table): Fixture providing the x_table with three parameters.
        mock_measure_3 (Power): Fixture providing the y data as a Power object.
    """
    parameter_0, parameter_1 = mock_x_table_3[0], mock_x_table_3[1]
    data = Array(x_table=mock_x_table_3, y=mock_measure_3).std(axis=parameter_0)
    data.plot(x=parameter_1)


@patch("matplotlib.pyplot.show")
def test_rsd_plot_line(mock_show, mock_x_table_3, mock_measure_3):
    """
    Test plotting the relative standard deviation (RSD) of data along a specific axis in the Array class.

    Args:
        mock_show (MagicMock): Mocked version of plt.show to prevent actual plot display.
        mock_x_table_3 (Table): Fixture providing the x_table with three parameters.
        mock_measure_3 (Power): Fixture providing the y data as a Power object.
    """
    parameter_0, parameter_1 = mock_x_table_3[0], mock_x_table_3[1]
    data = Array(x_table=mock_x_table_3, y=mock_measure_3).rsd(axis=parameter_0)
    data.plot(x=parameter_1)


if __name__ == "__main__":
    pytest.main([__file__])


# -
