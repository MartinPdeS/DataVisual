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

    def __post_init__(self):
        self.values = numpy.atleast_1d(self.values)

        if self.representation is None:
            self.representation = self.values

        self.values = self.values

        self.Label = self.long_label + f" [{self.unit}]" if self.long_label != "" else self.name
        self.short_label = self.short_label if self.short_label != "" else self.name

        self.__base_variable__ = None

    def Setvalues(self, values):
        self.values = values

    @property
    def has_unique_value(self):
        if self.values.shape[0] == 1:
            return True
        else:
            return False

    def normalize(self):
        self.unit = "U.A."
        self.values /= self.values.max()

    def __getitem__(self, item):
        return self.values[item]

    def __repr__(self):
        return self.name

    def get_size(self):
        return self.values.shape[0]

    def __eq__(self, other):
        if other is None:
            return False

        return True if self.name == other.name else False

    def iterate_through_values(self):
        if self.__base_variable__ is True:
            yield slice(None), None, "", ""

        if self.__base_variable__ is False:
            for n, value in enumerate(self.representation):
                if self.has_unique_value:
                    label_in_figure = f" | {self.long_label} : {value}"
                    label_in_box = ""
                else:
                    label_in_figure = ""
                    label_in_box = f" | {self.long_label} : {value:{self.format}}"

                yield n, value, label_in_figure, label_in_box


@dataclass
class Xtable(object):
    X: numpy.ndarray

    def __post_init__(self):
        self.X = numpy.array(self.X)
        self.shape = [x.get_size() for x in self.X]
        self._name_to_idx_ = {x.name: order for order, x in enumerate(self.X)}

        self._common_parameter_ = []
        self._different_parameter_ = []

        for x in self:
            if x.values.size == 1:
                self._common_parameter_.append(x)
            else:
                self._different_parameter_.append(x)

    def get_value(self, Axis):
        return self[Axis].Value

    def get_position(self, Value):
        for order, x in enumerate(self.X):
            if x == Value:
                return order

    def __getitem__(self, value):
        if value is None:
            return None

        Idx = self._name_to_idx_[value] if isinstance(value, str) else value

        return self.X[Idx]


class Ytable(object):
    def __init__(self, Y):
        self.Y = Y
        self._name_to_idx_ = self.get_name_to_idx_()

        for n, y in enumerate(self.Y):
            y.position = n

    def get_shape(self):
        return [x.Size for x in self.Y] + [1]

    def get_name_to_idx_(self):
        return {x.name: order for order, x in enumerate(self.Y)}

    def __getitem__(self, Val):
        if isinstance(Val, str):
            idx = self._name_to_idx_[Val]
            return self.Y[idx]
        else:
            return self.Y[Val]

# -
