#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import itertools
from dataclasses import dataclass

import DataVisual.tables as Table
from MPSPlots.render2D import SceneList, Axis


@dataclass
class DataV(object):
    array: numpy.ndarray
    """ The multi-dimensional array which axis are represented by the given tables """
    x_table: Table.Xtable
    """ Table representing the x dimensions """
    y_table: Table.Ytable
    """ Table representing the y dimensions """

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
        array = numpy.std(self.array, axis=axis.position)

        new_data_set = DataV(
            array=array,
            x_table=[x for x in self.x_table if x != axis],
            y_table=self.y_table
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
        array = numpy.mean(self.array, axis=axis.position)

        new_data_set = DataV(
            array=array,
            x_table=[x for x in self.x_table if x != axis],
            y_table=self.y_table
        )

        return new_data_set

    def Rsd(self, axis: str):
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
        array = numpy.std(self.array, axis=self.x_table.nameTable[axis]) \
                / numpy.mean(self.array, axis=self.x_table.nameTable[axis])

        new_data_set = DataV(
            array=array,
            x_table=[x for x in self.x_table if x != axis],
            y_table=self.y_table
        )

        return new_data_set

    def plot(self,
            x: Table.Xparameter,
            y: Table.Xparameter,
            normalize: bool = False,
            std: Table.Xparameter = None,
            add_box: bool = True,
            **kwargs) -> SceneList:

        y.values = self.array

        figure = SceneList(unit_size=(12, 4))

        if normalize:
            y.normalize()

        ax = figure.append_ax(
            x_label=x.Label,
            y_label=y.Label,
            show_legend=True,
            font_size=16,
            legend_font_size=15,
            **kwargs
        )

        if std is not None:
            self._add_std_plot_on_ax_(ax=ax, x=x, y=y, std=std)
        else:
            self._add_normal_plot_on_ax_(ax=ax, x=x, y=y)

        if add_box:
            self.add_box_info_to_ax(ax=ax, x=x, y=y)

        return figure

    def _get_x_table_generator_(self, base_variable):
        generator = []
        for x in self.x_table:
            if x in base_variable:
                x.__base_variable__ = True
            else:
                x.__base_variable__ = False

            x.generator = x.iterate_through_values()
            generator.append(x.generator)

        return itertools.product(*generator)

    def add_box_info_to_ax(self, ax: Axis, x: Table.Xparameter, y: Table.Xparameter) -> None:
        for iteration in self._get_x_table_generator_(base_variable=[x]):
            label_in_box = ""

            for _, _, common, _ in iteration:
                label_in_box += common

        ax.add_text(
            text=label_in_box,
            add_box=True,
            localisation='lower left',
            font_size=12
        )

    def _add_normal_plot_on_ax_(self, ax: Axis, x: Table.Xparameter, y: Table.Xparameter) -> None:
        """
        Method plot the multi-dimensional array with the x key as abscissa.
        args and kwargs can be passed as standard input to matplotlib.pyplot.

        :param      x:    Key of the self dict which represent the abscissa.
        :type       x:    Table.Xparameter
        :param      y:    Key of the self dict which represent the ordinate.
        :type       y:    Table.Xparameter

        :returns:   All the artist to be plotted
        :rtype:     list
        """
        for iteration in self._get_x_table_generator_(base_variable=[x]):
            slicer = []
            label_in_figure = y.short_label

            for idx, _, _, diff in iteration:
                slicer += [idx]
                label_in_figure += diff

            slc = tuple([y.position, *slicer])

            data = y[slc]

            ax.add_line(
                x=x.values,
                y=data,
                label=label_in_figure
            )

    def _add_std_plot_on_ax_(self, ax: Axis, x: Table.Xparameter, y: Table.Xparameter, std: Table.Xparameter) -> None:
        """
        Method plot the multi-dimensional array with the x key as abscissa.
        args and kwargs can be passed as standard input to matplotlib.pyplot.

        :param      x:    Key of the self dict which represent the abscissa.
        :type       x:    Table.Xparameter
        :param      y:    Key of the self dict which represent the ordinate.
        :type       y:    Table.Xparameter

        :returns:   All the artist to be plotted
        :rtype:     list
        """
        for iteration in self._get_x_table_generator_(base_variable=[x, std]):
            label_in_figure = y.short_label
            slicer = []

            for idx, value, common, diff in iteration:
                slicer += [idx]
                label_in_figure += diff

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

            slc = tuple([y.position, *slicer])

            y_std = y_std[slc]
            y_mean = y_mean[slc]

            ax.add_std_line(
                x=x.values,
                y_mean=y_mean.squeeze(),
                y_std=y_std.squeeze(),
                label=label_in_figure
            )

# -
