#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass


@dataclass
class Xparameter(object):
    name: str = None
    values: str = None
    representation: str = None
    format: str = ""
    long_label: str = ""
    unit: str = ""
    short_label: str = ""
    position: int = None

    is_base: bool = False

    def __post_init__(self):
        self.values = numpy.atleast_1d(self.values)
        self.unit = f" [{self.unit}]"

        self.short_label = self.short_label if self.short_label != "" else self.name

    def set_values(self, values: numpy.ndarray) -> None:
        self.values = values

    def get_value_representation(self, index: int) -> str:
        if self.representation is not None:
            return self.representation

        return f"{self.values[index]:{self.format}}"

    def get_representation(self, index: int = None, value_only: bool = False, short: bool = False) -> str:
        if self.representation is not None:
            return self.representation
        else:
            label = self.short_label if short else self.long_label

        if index is None or len(label) == 0:
            return label

        return f"{label}: {self.values[index]:{self.format}}"

    @property
    def size(self) -> int:
        return self.values.shape[0]

    def normalize(self):
        self.unit = " [A.U.]"
        self.values /= self.values.max()

    def __getitem__(self, item):
        return self.values[item]

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
