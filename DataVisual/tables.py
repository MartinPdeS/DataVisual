import numpy
from dataclasses import dataclass, field
from typing import List, Union

from DataVisual.utils import scale_unit


@dataclass
class Xparameter:
    """
    Represents a single parameter in a data visualization context, including its metadata and values.

    Attributes:
    -----------
    name : str
        The name of the parameter.
    values : numpy.ndarray
        The numeric values associated with the parameter.
    representation : str, optional
        Custom representation of the parameter's values, if any.
    format_string : str, optional
        String format for displaying the parameter's values.
    long_label : str, optional
        A longer, descriptive label for the parameter.
    unit : str, optional
        The unit of the parameter's values.
    short_label : str, optional
        A shorter label for the parameter, defaults to `name` if not provided.
    position : int, optional
        The position of the parameter in a larger context, such as a table.
    is_base : bool, optional
        Indicates whether the parameter is a base parameter.
    scale : str, optional
        The scale associated with the parameter, defaults to 'none'.
    """
    name: str
    values: numpy.ndarray = field(default_factory=lambda: numpy.array([]))
    representation: str = ""
    format_string: str = ""
    long_label: str = ""
    unit: str = ""
    short_label: str = ""
    position: int = None
    is_base: bool = False
    scale: str = 'none'

    def __post_init__(self) -> None:
        self.values = numpy.atleast_1d(self.values)
        self.short_label = self.short_label if self.short_label else self.name

    def get_value_representation(self, index: int) -> str:
        """Returns a formatted string representation for the value at the given index."""
        value = self.values[index]
        return f"{value:{self.format_string}}" if self.format_string else str(value)

    def scale_unit(self, scale: str, inverse_proportional: bool = False) -> None:
        """Scales the unit of the parameter's values according to the given scale."""
        scale_unit(self, inverse_proportional=inverse_proportional, scale=scale)

    def get_representation(self, index: int = None, value_only: bool = False, short: bool = True) -> str:
        """
        Returns the representation of the parameter, optionally including the value at a given index.

        Parameters:
        -----------
        index : int, optional
            The index of the value to include in the representation.
        value_only : bool, optional
            If True, returns only the value without the label.
        short : bool, optional
            If True, uses the short label, otherwise the long label.
        """
        label = self.short_label if short else self.long_label
        if index is not None and not value_only:
            value = self.get_value_representation(index)
            return f"{label}: {value}"
        elif index is not None:
            return self.get_value_representation(index)
        return label

    @property
    def size(self) -> int:
        """Returns the number of values."""
        return len(self.values)

    def normalize(self) -> None:
        """Normalizes the parameter's values to a range [0, 1] and updates the unit to arbitrary units (A.U.)."""
        self.values = self.values / numpy.max(self.values)
        self.unit = "A.U."

    def __getitem__(self, idx: Union[int, slice]) -> numpy.ndarray:
        """Allows indexing directly into the parameter's values."""
        return self.values[idx]

    def __repr__(self) -> str:
        return f"Xparameter(name={self.name}, size={self.size})"

    def __eq__(self, other) -> bool:
        """Checks equality based on the parameter's name."""
        return isinstance(other, Xparameter) and self.name == other.name


@dataclass
class Xtable:
    """
    Represents a table of parameters (Xparameters) for data visualization.

    Attributes:
    -----------
    parameters : list of Xparameter
        The list of parameters contained in the table.
    """
    parameters: List[Xparameter]

    def __post_init__(self) -> None:
        """Initializes the Xtable by assigning positions to each parameter."""
        for idx, parameter in enumerate(self.parameters):
            parameter.position = idx

    def __getitem__(self, index: Union[int, slice]) -> Union[Xparameter, List[Xparameter]]:
        """Allows indexing directly into the parameters list."""
        return self.parameters[index]

    def __repr__(self) -> str:
        return f"Xtable(size={len(self.parameters)})"
