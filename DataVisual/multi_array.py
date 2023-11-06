#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass

import DataVisual.tables as Table
from MPSPlots.render2D import SceneList, Axis
from copy import deepcopy


@dataclass
class DataV(object):
    array: numpy.ndarray
    """ The multi-dimensional array which axis are represented by the given tables """
    x_table: Table.Xtable
    """ Table representing the x dimensions """
    y_parameter: object
    """ Parameter representing the y dimensions """

    @property
    def shape(self):
        return self.array.shape

    def mean(self, axis: str):
        """
        Method compute and the mean value of specified axis.
        The method then return a new DataV daughter object compressed in
        the said axis.

        :param      axis:  Axis for which to perform the operation.
        :type       axis:  str

        :returns:    New DataV instance containing the std value of axis.
        :rtype:      DataV
        """
        array = numpy.mean(self.array, axis=axis.position)

        x_table = [x for x in self.x_table if x != axis]

        x_table = Table.Xtable(x_table)

        new_data_set = DataV(
            array=array,
            x_table=x_table,
            y_parameter=self.y_parameter
        )

        return new_data_set

    def std(self, axis: str):
        """
        Method compute and the std value of specified axis.
        The method then return a new DataV daughter object compressed in
        the said axis.

        :param      axis:  Axis for which to perform the operation.
        :type       axis:  str

        :returns:    New DataV instance containing the std value of axis.
        :rtype:      DataV
        """
        array = numpy.std(self.array, axis=axis.position)

        x_table = [x for x in self.x_table if x != axis]

        x_table = Table.Xtable(x_table)

        new_data_set = DataV(
            array=array,
            x_table=x_table,
            y_parameter=self.y_parameter
        )

        return new_data_set

    def rsd(self, axis: str):
        """
        Method compute and the rsd value of specified axis.
        The method then return a new DataV daughter object compressed in
        the said axis.
        rsd is defined as std/mean.

        :param      axis:  Axis for which to perform the operation.
        :type       axis:  str

        :returns:    New DataV instance containing the std value of axis.
        :rtype:      DataV
        """
        array = numpy.std(self.array, axis=axis.position) \
                / numpy.mean(self.array, axis=axis.position)

        x_table = [x for x in self.x_table if x != axis]

        x_table = Table.Xtable(x_table)

        new_data_set = DataV(
            array=array,
            x_table=x_table,
            y_parameter=self.y_parameter
        )

        return new_data_set

    def plot(self,
            x: Table.Xparameter,
            normalize: bool = False,
            std: Table.Xparameter = None,
            add_box: bool = False,
            **kwargs) -> SceneList:
        """
        Plots the array according to the input parameters

        :param      x:          THe x-axis parameter
        :type       x:          Table.Xparameter
        :param      normalize:  The normalize
        :type       normalize:  bool
        :param      std:        The standard
        :type       std:        { type_description }
        :param      add_box:    Indicates if the box is added
        :type       add_box:    bool
        :param      kwargs:     The keywords arguments
        :type       kwargs:     dictionary

        :returns:   The scene list.
        :rtype:     SceneList
        """
        y_parameter = deepcopy(self.y_parameter)
        y_parameter.values = self.array
        x.is_base = True

        figure = SceneList(unit_size=(12, 5), tight_layout=True)

        if normalize:
            y_parameter.normalize()

        ax = figure.append_ax(
            x_label=x.long_label + x.unit,
            y_label=y_parameter.long_label + y_parameter.unit,
            show_legend=True,
            font_size=16,
            legend_font_size=15,
            **kwargs
        )

        if std is not None:
            self.add_std_line_to_ax(ax=ax, x=x, y=y_parameter, std=std)
        else:
            self.add_line_plot_to_ax(ax=ax, x=x, y=y_parameter)

        if add_box:
            self.add_box_info_to_ax(ax=ax)

        return figure

    def add_box_info_to_ax(self, ax: Axis, except_parameter: list = []) -> None:
        column_labels = []
        table_values = []

        for x_parameter in self.x_table:
            if x_parameter.is_base:
                continue

            if x_parameter.size == 1:
                column_labels.append(x_parameter.long_label)

                table_string = x_parameter.get_representation(index=0, short=True)

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

            label += f" // {repr_string}"

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
            dim for dim, size in enumerate(self.array.shape) if dim != x.position
        ]

        _, index = numpy.nested_iters(self.array, [[], dimensions], flags=["multi_index"])

        for _ in index:

            slicer = list(index.multi_index)

            slicer.insert(x.position, slice(None))

            label = self.get_diff_label(slicer=slicer)

            slicer = tuple(slicer)
            y_data = self.array[slicer]

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
            dim for dim, size in enumerate(self.array.shape) if dim not in [x.position, std.position]
        ]

        _, index = numpy.nested_iters(self.array, [[], dimensions], flags=["multi_index"])

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
                self.array,
                axis=std.position,
                keepdims=True
            )

            y_mean = numpy.mean(
                self.array,
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

# -
