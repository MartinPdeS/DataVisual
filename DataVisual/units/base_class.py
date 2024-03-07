import numpy
from dataclasses import dataclass
from typing import Iterable


class UnitMeta(type):
    """
    A metaclass for creating classes that represent quantities with units, automatically
    adding properties for SI prefixes like nano, kilo, mega, etc., with support for inversely
    proportional conversions.
    """
    prefixes = {
        "nano": 1e-9,
        "micro": 1e-6,
        "milli": 1e-3,
        "centi": 1e-2,
        "deci": 1e-1,
        "base": 1,
        "deca": 1e1,
        'hecto': 1e2,
        "kilo": 1e3,
        "mega": 1e6,
        "giga": 1e9,
        "tera": 1e12,
    }

    prefix_orders = [-9, -6, -3, -2, -1, 0, 1, 2, 3, 6, 9, 12]

    # List of (magnitude, prefix) tuples
    magnitude_to_prefixes = [
        (-9, "nano"),
        (-6, "micro"),
        (-3, "milli"),
        (-2, "centi"),
        (-1, "deci"),
        (0, "base"),
        (1, "deca"),
        (2, "hecto"),
        (3, "kilo"),
        (6, "mega"),
        (9, "giga"),
        (12, "tera")
    ]

    prefix_to_string = {
        "nano": "n",
        "micro": r"$\mu$",
        "milli": "m",
        "centi": "c",
        "deci": "d",
        "base": "",
        "deca": "da",
        "hecto": "h",
        "kilo": "k",
        "mega": "M",
        "giga": "G",
        "tera": "T"
    }

    def __new__(cls, clsname, bases, attrs):
        new_class = super().__new__(cls, clsname, bases, attrs)
        is_inverse = attrs.get('is_inverse', False)
        use_prefix = attrs.get('use_prefix', True)

        power = attrs.get('power', 1)  # Default power is 1

        if not use_prefix:
            return new_class

        def make_property(prefix, multiplier, is_inverse, power):

            if not is_inverse:
                def getter(self):
                    return getattr(self, 'base_values') / (multiplier ** power)
                def setter(self, value):
                    setattr(self, 'base_values', value * (multiplier ** power))
            else:
                def getter(self):
                    return getattr(self, 'base_values') * (multiplier ** power)
                def setter(self, value):
                    setattr(self, 'base_values', value / (multiplier ** power))

            return property(getter, setter)

        for prefix, multiplier in cls.prefixes.items():
            property_name = f"{prefix}_{attrs['unit'].lower()}"
            setattr(new_class, property_name, make_property(prefix, multiplier, is_inverse, power))

        return new_class


class BaseUnit:
    """
    A base class for representing measurement units with features for normalization,
    SI prefix adjustment, and formatted string representation.

    Attributes:
        long_label (str): Descriptive name of the unit.
        short_label (str): Abbreviated label of the unit.
        string_format (str): Python format specifier for converting numerical values to strings.
        values (float | np.ndarray): The numerical values associated with this unit.
        use_long_label_for_repr (bool): Flag indicating whether the long label should be used in the __repr__ output.
        use_prefix (bool): Determines whether SI prefixes are automatically used when representing values.
        value_representation (float | np.ndarray): Custom representation of the values, if any.

    Methods:
        __repr__: Returns a string representation of the unit instance.
        get_unit: Returns the unit string, considering normalization.
        size: Returns the number of values.
        shape: Returns the shape of the values array.
        values: Property that returns the measurement values, normalized if applicable.
        get_closest_prefix_string: Identifies the closest SI prefix based on the values' magnitude.
        get_representation: Generates a formatted string representation for the unit and its values.
        get_prefix: Determines the appropriate SI prefix for representation.
        get_array: Retrieves the measurement values, optionally scaled by the closest SI prefix.
    """

    def __init__(
            self,
            long_label: str,
            short_label: str | None = None,
            string_format: str = '',
            values: numpy.ndarray | None = None,
            use_long_label_for_repr: bool = False,
            use_prefix: bool = True,
            value_representation: numpy.ndarray | None = None,
            normalized: bool = False):
        self.long_label = long_label
        self.short_label = short_label if short_label is not None else long_label.lower().replace(' ', '_')
        self.string_format = string_format if string_format is not None else ".2f"
        self.base_values = values
        self.use_long_label_for_repr = use_long_label_for_repr
        self.use_prefix = use_prefix if use_prefix is not None else True
        self.value_representation = value_representation
        self.normalized = normalized
        self.is_base = False
        self.string_format = ''

    def __repr__(self) -> str:
        """Returns a string representation of the BaseUnit instance."""
        unit_representation = self.get_unit()

        if unit_representation == '':
            return f"{self.long_label}"

        return f"{self.long_label} [{unit_representation}]"

    def get_unit(self) -> str:
        """Returns the unit, considering if it's normalized."""
        return "A.U." if self.normalized else self.unit

    @property
    def size(self) -> int:
        """Returns the number of values."""
        return numpy.size(self.values)

    @property
    def shape(self) -> tuple:
        """Returns the shape of the values."""
        return numpy.shape(self.values)

    @classmethod
    def closest_prefix_order(cls, order_of_magnitude: float) -> str:
        """
        Determines the closest SI prefix based on the order of magnitude of the values.

        Args:
            order_of_magnitude (float): The order of magnitude of the values.

        Returns:
            str: The closest SI prefix.
        """
        # Find the prefix with the highest magnitude that is less than or equal to the order_of_magnitude
        for magnitude, prefix in reversed(cls.magnitude_to_prefixes):
            if order_of_magnitude >= magnitude:
                return prefix
        # Fallback to the smallest prefix if none match
        return cls.magnitude_to_prefixes[0][1]

    @property
    def values(self) -> numpy.ndarray:
        if self.normalized:
            return self.base_values / self.base_values.max()
        return self.base_values

    def get_closest_prefix_string(self) -> tuple[str, str]:
        """
        Determines the closest SI prefix string for the current values.

        Returns:
            tuple[str, str]: A tuple containing the long and short forms of the closest SI prefix.
        """
        base_value = numpy.max(self.base_values) if isinstance(self.base_values, Iterable) else self.base_values
        magnitude = numpy.log10(abs(base_value)) / self.power

        prefix = self.closest_prefix_order(magnitude)

        # Return the string representation of the closest prefix
        return prefix, UnitMeta.prefix_to_string.get(prefix, "")

    def get_representation(
            self,
            index: int = None,
            add_unit: bool = False,
            use_short_repr: bool = False,
            use_prefix: bool = True) -> str:
        """
        Generates a formatted string representation of the unit, optionally including its value,
        label, and unit prefix.

        Args:
            index (int, optional): The index of the value to format. Relevant for array-like values.
            add_unit (bool, optional): Flag to include the unit in the representation.
            use_short_repr (bool, optional): Flag to use the short label instead of the long label.
            use_prefix (bool, optional): Flag to use SI prefixes in the value representation.

        Returns:
            str: The formatted string representation of the unit.
        """
        label = self._choose_label(use_short_repr)
        value = self._get_value_with_prefix(index, use_prefix)
        unit = self._get_unit_string(add_unit, use_prefix)

        # Construct the final representation based on provided options
        representation = f"{label}"
        if value is not None:
            representation += f": {value:{self.string_format}}"
        if add_unit and unit not in ['', 'base']:
            representation += f" [{unit}]"

        return representation

    def _choose_label(self, use_short_repr: bool) -> str:
        """Selects the appropriate label based on user preference."""
        label = self.short_label if use_short_repr else self.long_label
        return label.replace('_', ' ')

    def _get_value_with_prefix(self, index: int, use_prefix: bool):
        """Retrieves the value at the given index, considering SI prefix adjustments."""
        if self.value_representation is not None:
            return self.value_representation if index is None else self.value_representation[index]

        if index is not None:
            if use_prefix and self.use_prefix:
                long_prefix, _ = self.get_prefix(use_prefix=use_prefix)
                # Assuming there's logic to handle attribute retrieval by prefix
                return getattr(self, f"{long_prefix}_{self.unit}")[index]
            else:
                return self.base_values if index is None else self.base_values[index]

    def _get_unit_string(self, add_unit: bool, use_prefix: bool) -> str:
        """
        Constructs the unit string, including the appropriate SI prefix if required.

        Returns an empty string if add_unit is False.
        """
        if not add_unit:
            return ""

        # Fetch the appropriate prefix based on whether SI prefixes are used.
        _, short_prefix = self.get_prefix(use_prefix=use_prefix)
        unit = self.short_unit if self.unit else ""
        return f"{short_prefix}{unit}"

    def get_prefix(self, use_prefix: bool) -> tuple[str, str]:
        """
        Determines the appropriate SI prefix for representation based on the class's values.

        This method needs to be implemented or adjusted based on the specific logic for determining
        the prefix, likely involving `closest_prefix_order` or similar logic.

        Returns:
            tuple[str, str]: A tuple containing the long form and short form of the SI prefix.
        """
        if use_prefix and self.use_prefix:
            long_prefix, short_prefix = self.get_closest_prefix_string()
        else:
            long_prefix, short_prefix = 'base', 'base'

        return long_prefix, short_prefix

    def get_array(self, scaled: bool = False) -> numpy.ndarray:
        """
        Returns the measurement values, optionally scaled according to the closest SI prefix.

        Args:
            scaled (bool, optional): Whether to scale the values according to the closest SI prefix. Defaults to False.

        Returns:
            np.ndarray: The measurement values, scaled if requested.
        """
        if not scaled or not self.use_prefix:
            return self.base_values
        else:
            return self.get_scaled_array()

    def get_scaled_array(self) -> numpy.ndarray:
        """Returns a formatted string representation for the value at the given index."""
        long_prefix, short_prefix = self.get_closest_prefix_string()
        return getattr(self, f'{long_prefix}_{self.get_unit()}')

# -
