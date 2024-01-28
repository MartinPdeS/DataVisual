#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass

from DataVisual.utils import scale_unit


@dataclass
class Xparameter(object):
    name: str = None
    values: numpy.ndarray = None
    representation: str = None
    format: str = ""
    long_label: str = ""
    unit: str = ""
    short_label: str = ""
    position: int = None

    is_base: bool = False

    def __post_init__(self) -> None:
        self.values = numpy.atleast_1d(self.values)
        self.unit = f"{self.unit}"

        self.short_label = self.short_label if self.short_label != "" else self.name

    def get_value_representation(self, index: int) -> str:
        if self.representation is not None:
            return self.representation

        value = self.values[index]

        return f"{value:{self.format}}"

    def scale_unit(self, scale: str, inverse_proportional: bool = False) -> None:
        """
        Function that scales the unit an arrays of the parameter

        :param      scale:                 The scale
        :type       scale:                 str
        :param      inverse_proportional:  Reverse the factor relation if True
        :type       inverse_proportional:  bool

        :returns:   No return
        :rtype:     None
        """
        return scale_unit(
            parameter=self,
            inverse_proportional=inverse_proportional,
            scale=scale
        )

    def get_representation(
            self,
            index: int = None,
            value_only: bool = False,
            short: bool = True) -> str:
        """
        Gets the representation of a variable at certain index in the table.

        :param      index:       The index at which evaluate the values
        :type       index:       int
        :param      value_only:  Returns only the value
        :type       value_only:  bool
        :param      short:       Returns short or long representation string
        :type       short:       bool

        :returns:   The representation.
        :rtype:     str
        """
        values = self.representation if self.representation is not None else self.values

        label = self.short_label if short else self.long_label

        if index is None or len(label) == 0:
            return label

        return f"{label}: {values[index]:{self.format}}"

    @property
    def size(self) -> int:
        return self.values.shape[0]

    def normalize(self) -> None:
        self.unit = "A.U."
        self.values /= self.values.max()

    def __getitem__(self, idx: int) -> numpy.ndarray:
        return self.values[idx]

    def __repr__(self) -> str:
        return str(self.name)

    def get_size(self) -> int:
        return self.values.shape[0]

    def __eq__(self, other) -> bool:
        if other is None:
            return False

        return True if self.name == other.name else False


@dataclass
class Xtable(object):
    parameters: list

    def __post_init__(self):
        self.parameters = numpy.array(self.parameters)

        for idx, parameter in enumerate(self.parameters):
            parameter.position = idx

    def __getitem__(self, index):
        return self.parameters[index]

# -
