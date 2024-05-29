#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass
from typing import Any, Callable

from MPSPlots.render2D import SceneList, Axis
from copy import deepcopy

from DataVisual.tables import Table
from DataVisual.units import BaseUnit


@dataclass
class Array:
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

    x_table: Table
    y: Any
    scale: str = 'none'

    def __post_init__(self):
        self._validate_attributes()

    def _validate_attributes(self):
        """Ensures that the 'y' attribute has a 'values' attribute."""
        if not hasattr(self.y, 'base_values'):
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

            x_table = Table(x_table)

            new_values = operation(self, axis=axis)

            new_y.base_values = new_values

            return Array(x_table=x_table, y=new_y)

        return wrapper

    @generate_y_copy
    def mean(self, axis: str):
        """
        Method compute and the mean value of specified axis.
        The method then return a new Array daughter object compressed in
        the said axis.

        :param      axis:  Axis for which to perform the operation.
        :type       axis:  str

        :returns:    New Array instance containing the std value of axis.
        :rtype:      Array
        """

        return numpy.mean(self.y.values, axis=axis.position)

    @generate_y_copy
    def std(self, axis: str):
        """
        Method compute and the std value of specified axis.
        The method then return a new Array daughter object compressed in
        the said axis.

        :param      axis:  Axis for which to perform the operation.
        :type       axis:  str

        :returns:    New Array instance containing the std value of axis.
        :rtype:      Array
        """
        return numpy.std(self.y.values, axis=axis.position)

    @generate_y_copy
    def rsd(self, axis: str):
        """
        Method compute and the rsd value of specified axis.
        The method then return a new Array daughter object compressed in
        the said axis.
        rsd is defined as std/mean.

        :param      axis:  Axis for which to perform the operation.
        :type       axis:  str

        :returns:    New Array instance containing the std value of axis.
        :rtype:      Array
        """
        std = numpy.std(self.y.values, axis=axis.position)
        mean = numpy.mean(self.y.values, axis=axis.position)

        return std / mean

    def _normalize(self, values: numpy.ndarray) -> numpy.ndarray:
        """Normalizes the y values."""
        return (values - numpy.mean(values)) / numpy.std(values)

    def plot(
            self,
            x: BaseUnit,
            normalize: bool = False,
            std: BaseUnit = None,
            add_box: bool = False,
            **kwargs) -> SceneList:
        """
        Generates a plot of the data.

        Parameters:
        -----------
        x : BaseUnit
            The parameter for the x-axis.
        normalize : bool, optional
            If True, normalize the y data, by default False.
        std : BaseUnit, optional
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
            y.normalized = True

        y_label = y.get_representation(
            use_prefix=True,
            add_unit=True,
        )

        x_label = x.get_representation(
            use_prefix=True,
            add_unit=True,
        )

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

                table_string = x_parameter.get_representation(index=0, use_short_repr=True)

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

            repr_string = x_parameter.get_representation(
                index=i,
                use_short_repr=True,
                use_prefix=True,
                add_unit=True
            )

            label += "/ " + f"{repr_string}"

        return label

    def add_line_plot_to_ax(self, ax: Axis, x: BaseUnit, y: BaseUnit, **kwargs) -> None:
        """
        Method plot the multi-dimensional array with the x key as abscissa.
        kwargs can be passed as standard input to the artist Line from MPSPLots.

        :param      x:    Key of the self dict which represent the abscissa.
        :type       x:    BaseUnit
        :param      y:    Key of the self dict which represent the ordinate.
        :type       y:    BaseUnit

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
            y_data = self.y.values[slicer].squeeze()
            x_data = x.values

            ax.add_line(
                x=x_data,
                y=y_data,
                label=label,
                line_width=2,
                **kwargs
            )

    def add_std_line_to_ax(self, ax: Axis, x: BaseUnit, y: BaseUnit, std: BaseUnit) -> None:
        """
        Method plot the multi-dimensional array with the x key as abscissa.
        kwargs can be passed as standard input to the artist STDLine from MPSPLots.

        :param      x:    Key of the self dict which represent the abscissa.
        :type       x:    BaseUnit
        :param      y:    Key of the self dict which represent the ordinate.
        :type       y:    BaseUnit

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

            ax.add_std_line(
                x=x.values,
                y_mean=y_mean[slicer].squeeze(),
                y_std=y_std[slicer].squeeze(),
                label=label
            )

# -
