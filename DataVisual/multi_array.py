#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy

import numpy
from dataclasses import dataclass
from typing import Any, Callable, NoReturn
import matplotlib.pyplot as plt
import MPSPlots

from DataVisual.tables import Table
from DataVisual.units import BaseUnit


@dataclass
class Array:
    """
    A class for visualizing and manipulating data associated with X and Y dimensions.

    Attributes:
    -----------
    x_table : Table
        A table representing the X dimensions.
    y : Any
        An object representing the Y dimensions, expected to have a `values` attribute.
    """

    x_table: Table
    y: Any

    def __post_init__(self):
        """Post-initialization to validate the attributes."""
        self._validate_attributes()

    def _validate_attributes(self):
        """Ensures that the 'y' attribute has a 'values' attribute."""
        if not hasattr(self.y, 'values'):
            raise ValueError("The 'y' attribute must have a 'values' attribute.")

    @property
    def shape(self) -> tuple:
        """Returns the shape of the y values."""
        return self.y.values.shape

    @staticmethod
    def generate_y_copy(operation: Callable) -> Callable:
        """
        Decorator to generate a modified copy of 'y' for operations like mean, std, and rsd.

        Args:
            operation (Callable): The operation to perform on 'y'.

        Returns:
            Callable: A wrapper function that applies the operation and returns a new Array instance.
        """

        def wrapper(self, axis):
            new_y = deepcopy(self.y)

            x_table = [x for x in self.x_table if x != axis]
            x_table = Table(x_table)

            new_values = operation(self, axis=axis)

            new_y.values = new_values

            return Array(x_table=x_table, y=new_y)

        return wrapper

    @generate_y_copy
    def mean(self, axis: str) -> numpy.ndarray:
        """
        Computes the mean along the specified axis and returns a new Array instance.

        Args:
            axis (str): The axis along which to compute the mean.

        Returns:
            Array: A new Array instance containing the mean values along the specified axis.
        """
        return numpy.mean(self.y.values, axis=axis.position)

    @generate_y_copy
    def std(self, axis: str) -> numpy.ndarray:
        """
        Computes the standard deviation along the specified axis and returns a new Array instance.

        Args:
            axis (str): The axis along which to compute the standard deviation.

        Returns:
            Array: A new Array instance containing the standard deviation values along the specified axis.
        """
        return numpy.std(self.y.values, axis=axis.position)

    @generate_y_copy
    def rsd(self, axis: str) -> numpy.ndarray:
        """
        Computes the relative standard deviation (RSD) along the specified axis.

        RSD is defined as the standard deviation divided by the mean.

        Args:
            axis (str): The axis along which to compute the RSD.

        Returns:
            Array: A new Array instance containing the RSD values along the specified axis.
        """
        std = numpy.std(self.y.values, axis=axis.position)
        mean = numpy.mean(self.y.values, axis=axis.position)

        return std / mean

    def _normalize(self, values: numpy.ndarray) -> numpy.ndarray:
        """
        Normalizes the provided values.

        Args:
            values (np.ndarray): The values to normalize.

        Returns:
            np.ndarray: The normalized values.
        """
        return (values - numpy.mean(values)) / numpy.std(values)

    def plot(
            self,
            x: BaseUnit,
            normalize: bool = False,
            std: BaseUnit = None,
            add_box: bool = False,
            **kwargs) -> NoReturn:
        """
        Generates a plot of the data with options for normalization, adding standard deviation, and more.

        This method creates a plot using the provided x-axis data, and optionally normalizes the y data,
        adds standard deviation shading, and includes additional information in a box.

        Args:
            x (BaseUnit): The parameter for the x-axis.
            normalize (bool, optional): If True, normalizes the y data. Default is False.
            std (BaseUnit, optional): The parameter for standard deviation. Default is None.
            add_box (bool, optional): If True, adds a box with additional information to the plot. Default is False.
            **kwargs: Additional keyword arguments passed to the plotting functions.

        Returns:
            NoReturn: This method modifies the plot in place and displays it, but does not return a value.
        """
        with plt.style.context(MPSPlots.styles.mps):
            # Deep copy the y data to avoid modifying the original
            y = deepcopy(self.y)
            x.is_base = True

            # Create a figure and axis for plotting
            figure, ax = plt.subplots()

            # Normalize the y data if specified
            if normalize:
                y.normalized = True

            # Generate x and y axis labels
            y_label = y.get_representation(use_prefix=True, add_unit=True)
            x_label = x.get_representation(use_prefix=True, add_unit=True)

            # Set axis labels
            ax.set(xlabel=x_label, ylabel=y_label)

            # Plot the data with or without standard deviation
            if std is not None:
                self.add_std_line_to_ax(ax=ax, x=x, y=y, std=std)
            else:
                self.add_line_plot_to_ax(ax=ax, x=x, y=y)

            # Optionally add a legend
            ax.legend()

            # Adjust layout for better spacing
            plt.tight_layout()

            # Display the plot
            plt.show()

    def get_diff_label(self, slicer: tuple) -> str:
        """
        Generates a label for a plot based on the parameters and their values,
        taking into account the slicing information provided.

        This method constructs a label string by iterating through the slicer and
        the corresponding x_table parameters. It skips parameters with a single value
        or when the slicer is set to select all elements (`slice(None)`).

        Args:
            slicer (tuple): A tuple representing the indices or slices used to select
                            specific data in a multi-dimensional array.

        Returns:
            str: A string label that represents the selected parameters and their values.
        """
        label = ''
        for index, x_parameter in zip(slicer, self.x_table):
            # Skip parameters with only one value or when the entire dimension is selected
            if x_parameter.size == 1 or index == slice(None):
                continue

            # Generate a representation of the parameter's value
            repr_string = x_parameter.get_representation(
                index=index,
                use_short_repr=True,
                use_prefix=True,
                add_unit=True
            )

            # Append the representation to the label string
            label += f"/ {repr_string}"

        return label.strip()  # Remove any leading/trailing whitespace or slashes

    def add_line_plot_to_ax(self, ax: plt.Axes, x: BaseUnit, y: BaseUnit, **kwargs) -> NoReturn:
        """
        Adds a line plot to the given axis using the provided x and y data.

        This method handles multi-dimensional arrays by iterating over all non-x dimensions.
        Each slice of the y array along these dimensions will be plotted against the x values.

        Args:
            ax (Axes): The matplotlib axis where the line plot will be added.
            x (Any): The x-axis data, represented as a BaseUnit object.
            y (Any): The y-axis data, represented as a BaseUnit object.
            **kwargs: Additional keyword arguments passed to the plot method.

        Returns:
            NoReturn: This method modifies the ax in place and does not return any value.
        """
        # Identify non-x dimensions to iterate over
        dimensions = [dim for dim, size in enumerate(y.values.shape) if dim != x.position]

        # Iterate over multi-dimensional y array
        _, index = numpy.nested_iters(y.values, [[], dimensions], flags=["multi_index"])

        for _ in index:
            slicer = list(index.multi_index)
            slicer.insert(x.position, slice(None))  # Insert full slice for x dimension

            label = self.get_diff_label(slicer=tuple(slicer))

            y_data = y.values[tuple(slicer)].squeeze()
            x_data = x.values

            # Plot the data
            ax.plot(x_data, y_data, label=label, linewidth=2, **kwargs)

    def add_std_line_to_ax(self, ax: plt.Axes, x: BaseUnit, y: BaseUnit, std: BaseUnit) -> NoReturn:
        """
        Adds a line plot with standard deviation shading to the given axis.

        This method plots the mean of the y data with shaded areas representing
        the standard deviation. It handles multi-dimensional arrays by iterating
        over all non-x and non-std dimensions.

        Args:
            ax (Axes): The matplotlib axis where the line plot will be added.
            x (Any): The x-axis data, represented as a BaseUnit object.
            y (Any): The y-axis data, represented as a BaseUnit object.
            std (Any): The standard deviation data, represented as a BaseUnit object.

        Returns:
            NoReturn: This method modifies the ax in place and does not return any value.
        """
        std.is_base = True
        # Identify non-x and non-std dimensions to iterate over
        dimensions = [dim for dim, size in enumerate(y.values.shape) if dim not in [x.position, std.position]]

        # Iterate over multi-dimensional y array
        _, index = numpy.nested_iters(y.values, [[], dimensions], flags=["multi_index"])

        for _ in index:
            slicer = list(index.multi_index)

            if x.position < std.position:
                slicer.insert(x.position, slice(None))
                slicer.insert(std.position, slice(None))
            else:
                slicer.insert(std.position, slice(None))
                slicer.insert(x.position, slice(None))

            label = self.get_diff_label(slicer=tuple(slicer))

            # Compute mean and standard deviation
            y_mean = numpy.mean(y.values, axis=std.position, keepdims=True)
            y_std = numpy.std(y.values, axis=std.position, keepdims=True)

            y_mean = y_mean[tuple(slicer)].squeeze()
            y_std = y_std[tuple(slicer)].squeeze()

            # Compute upper and lower bounds for shading
            y1 = y_mean - y_std / 2
            y2 = y_mean + y_std / 2

            # Plot the shaded area and mean line
            ax.fill_between(x.values, y1=y1, y2=y2, label=label, alpha=0.5, edgecolor='black')
            ax.plot(x.values, y_mean, linewidth=1)

# -
