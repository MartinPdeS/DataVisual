#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass
from typing import Any, Optional, Callable

import DataVisual.tables as Table
from DataVisual.utils import scale_unit
from MPSPlots.render2D import SceneList, Axis
from copy import deepcopy


@dataclass
class DataVisual:
    """
    A class for visualizing and manipulating data associated with X and Y dimensions.

    Attributes:
    -----------
    x_table : Xtable
        A table representing the X dimensions.
    y : object
        An object representing the Y dimensions, expected to have a `values` attribute.
    scale : str, optional
        The scale type for the visualization, defaults to 'none'.
    """

    x_table: Table.Xtable
    y: Any
    scale: str = 'none'

    def __post_init__(self):
        self._validate_attributes()

    def _validate_attributes(self):
        """Ensures that the 'y' attribute has a 'values' attribute."""
        if not hasattr(self.y, 'values'):
            raise ValueError("The 'y' attribute must have a 'values' attribute.")

    @property
    def shape(self) -> tuple:
        """Returns the shape of the y values."""
        return self.y.values.shape

    def generate_y_copy(operation: Callable):
        """Decorator to generate a y copy for operations like mean, std, and rsd."""
        def wrapper(self, axis):
            new_y = deepcopy(self.y)

            x_table = [x for x in self.x_table if x != axis]

            x_table = Table.Xtable(x_table)

            new_values = operation(self, axis=axis)

            new_y.values = new_values

            return DataVisual(x_table=x_table, y=new_y)

        return wrapper

    @generate_y_copy
    def mean(self, axis: str):
        """
        Method compute and the mean value of specified axis.
        The method then return a new DataVisual daughter object compressed in
        the said axis.

        :param      axis:  Axis for which to perform the operation.
        :type       axis:  str

        :returns:    New DataVisual instance containing the std value of axis.
        :rtype:      DataVisual
        """

        return numpy.mean(self.y.values, axis=axis.position)

    @generate_y_copy
    def std(self, axis: str):
        """
        Method compute and the std value of specified axis.
        The method then return a new DataVisual daughter object compressed in
        the said axis.

        :param      axis:  Axis for which to perform the operation.
        :type       axis:  str

        :returns:    New DataVisual instance containing the std value of axis.
        :rtype:      DataVisual
        """
        return numpy.std(self.y.values, axis=axis.position)

    @generate_y_copy
    def rsd(self, axis: str):
        """
        Method compute and the rsd value of specified axis.
        The method then return a new DataVisual daughter object compressed in
        the said axis.
        rsd is defined as std/mean.

        :param      axis:  Axis for which to perform the operation.
        :type       axis:  str

        :returns:    New DataVisual instance containing the std value of axis.
        :rtype:      DataVisual
        """
        std = numpy.std(self.y.values, axis=axis.position)
        mean = numpy.mean(self.y.values, axis=axis.position)

        return std / mean

    def _normalize(self, values: numpy.ndarray) -> numpy.ndarray:
        """Normalizes the y values."""
        return (values - numpy.mean(values)) / numpy.std(values)

    def plot(
            self,
            x: Table.Xparameter,
            normalize: bool = False,
            std: Table.Xparameter = None,
            add_box: bool = False,
            **kwargs) -> SceneList:
        """
        Generates a plot of the data.

        Parameters:
        -----------
        x : Xparameter
            The parameter for the x-axis.
        normalize : bool, optional
            If True, normalize the y data, by default False.
        std : Xparameter, optional
            The parameter for standard deviation, by default None.
        add_box : bool, optional
            If True, adds a box with additional information to the plot, by default False.
        **kwargs : dict
            Additional keyword arguments for plotting.

        Returns:
        --------
        SceneList
            A SceneList object containing the plot.
        """
        y = deepcopy(self.y)

        x.is_base = True

        figure = SceneList(unit_size=(12, 5), tight_layout=True)

        if normalize:
            y.normalize()

        y_label = f" {y.long_label} [{y.unit}]"

        x_label = f" {x.long_label} [{x.unit}]"

        ax = figure.append_ax(
            x_label=x_label,
            y_label=y_label,
            show_legend=True,
            font_size=22,
            legend_font_size=18,
            tick_size=20,
            **kwargs
        )

        if std is not None:
            self.add_std_line_to_ax(ax=ax, x=x, y=y, std=std)
        else:
            self.add_line_plot_to_ax(ax=ax, x=x, y=y)

        if add_box:
            self.add_box_info_to_ax(ax=ax)

        return figure

    def add_box_info_to_ax(self, ax: Axis, except_parameter: list = []) -> None:
        """Adds a box with additional information to the axis."""
        column_labels, table_values = [], []

        for x_parameter in self.x_table:
            if x_parameter.is_base:
                continue

            if x_parameter.size == 1:
                column_labels.append(x_parameter.long_label)

                table_string = x_parameter.get_value_representation(index=0)

                table_values.append(table_string)

        ax.add_table(
            table_values=[table_values],
            column_labels=column_labels,
            row_labels=[''],
            position='top'
        )

    def get_diff_label(self, slicer: tuple) -> str:
        """
        Gets the label corresponding to the different parameter for each plots
        taking account for the slicer value.

        :param      slicer:  The slicer
        :type       slicer:  tuple

        :returns:   The difference label.
        :rtype:     str
        """
        label = ''
        for i, x_parameter in zip(slicer, self.x_table):
            if x_parameter.size == 1:
                continue

            if i == slice(None):
                continue

            repr_string = x_parameter.get_representation(index=i, short=False)

            label += f" :: {repr_string}"

        return label

    def add_line_plot_to_ax(self, ax: Axis, x: Table.Xparameter, y: Table.Xparameter, **kwargs) -> None:
        """
        Method plot the multi-dimensional array with the x key as abscissa.
        kwargs can be passed as standard input to the artist Line from MPSPLots.

        :param      x:    Key of the self dict which represent the abscissa.
        :type       x:    Table.Xparameter
        :param      y:    Key of the self dict which represent the ordinate.
        :type       y:    Table.Xparameter

        :returns:   No returns
        :rtype:     None
        """
        dimensions = [
            dim for dim, size in enumerate(self.y.values.shape) if dim != x.position
        ]

        _, index = numpy.nested_iters(self.y.values, [[], dimensions], flags=["multi_index"])

        for _ in index:

            slicer = list(index.multi_index)

            slicer.insert(x.position, slice(None))

            label = self.get_diff_label(slicer=slicer)

            slicer = tuple(slicer)
            y_data = self.y.values[slicer]

            ax.add_line(
                x=x.values,
                y=y_data.squeeze(),
                label=label,
                line_width=2,
                **kwargs
            )

    def add_std_line_to_ax(self, ax: Axis, x: Table.Xparameter, y: Table.Xparameter, std: Table.Xparameter) -> None:
        """
        Method plot the multi-dimensional array with the x key as abscissa.
        kwargs can be passed as standard input to the artist STDLine from MPSPLots.

        :param      x:    Key of the self dict which represent the abscissa.
        :type       x:    Table.Xparameter
        :param      y:    Key of the self dict which represent the ordinate.
        :type       y:    Table.Xparameter

        :returns:   No returns
        :rtype:     None
        """
        std.is_base = True
        dimensions = [
            dim for dim, size in enumerate(self.y.values.shape) if dim not in [x.position, std.position]
        ]

        _, index = numpy.nested_iters(self.y.values, [[], dimensions], flags=["multi_index"])

        for _ in index:
            slicer = list(index.multi_index)

            if x.position < std.position:
                slicer.insert(x.position, slice(None))
                slicer.insert(std.position, slice(None))
            else:
                slicer.insert(std.position, slice(None))
                slicer.insert(x.position, slice(None))

            label = self.get_diff_label(slicer)

            slicer = tuple(slicer)

            y_std = numpy.std(
                self.y.values,
                axis=std.position,
                keepdims=True
            )

            y_mean = numpy.mean(
                self.y.values,
                axis=std.position,
                keepdims=True
            )

            y_std = y_std[slicer]
            y_mean = y_mean[slicer]

            ax.add_std_line(
                x=x.values,
                y_mean=y_mean.squeeze(),
                y_std=y_std.squeeze(),
                label=label
            )

    def scale_unit(self, scale: str, inverse_proportional: bool = False) -> None:
        """
        Scales the unit of the y parameter based on the given scale.

        Parameters:
        -----------
        scale : str
            The scale type (e.g., 'micro', 'nano').
        inverse_proportional : bool, optional
            Whether the scaling is inverse proportional, by default False.
        """
        return scale_unit(
            parameter=self.y,
            inverse_proportional=inverse_proportional,
            scale=scale
        )

# -
