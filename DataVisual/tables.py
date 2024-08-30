#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import List, Union
from DataVisual.units import BaseUnit

@dataclass
class Table:
    """
    Represents a table of parameters (BaseUnits) for data visualization.

    This class provides functionality to store, access, and manage a list of parameters
    used in data visualization, typically for x-axis or other multidimensional data.

    Attributes:
    -----------
    parameters : List[BaseUnit]
        A list of BaseUnit objects representing the parameters contained in the table.
    """

    parameters: List[BaseUnit]

    def __post_init__(self) -> None:
        """
        Post-initialization to assign positional indices to each parameter.

        This method assigns the index of each parameter in the list as its `position` attribute,
        enabling easy reference to the order of parameters within the table.
        """
        for idx, parameter in enumerate(self.parameters):
            parameter.position = idx

    def __getitem__(self, index: Union[int, slice]) -> Union[BaseUnit, List[BaseUnit]]:
        """
        Enables direct indexing into the parameters list.

        Args:
            index (Union[int, slice]): The index or slice to retrieve from the parameters list.

        Returns:
            Union[BaseUnit, List[BaseUnit]]: The parameter(s) at the specified index or slice.
        """
        return self.parameters[index]

    def __repr__(self) -> str:
        """
        Returns a string representation of the Table.

        This is useful for debugging and provides a clear view of the parameters contained in the table.

        Returns:
            str: A string representation of the parameters list.
        """
        return str(self.parameters)
