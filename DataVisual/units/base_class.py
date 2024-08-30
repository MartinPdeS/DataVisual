import numpy
from typing import Iterable


class UnitMeta(type):
    """
    A metaclass for dynamically adding SI prefix properties to unit classes. Supports
    direct and inversely proportional unit conversions based on the provided power
    and whether the unit should use prefixes.

    Attributes:
        prefixes (dict): Maps SI prefix names to their corresponding multiplier values.
        prefix_to_string (dict): Maps SI prefix names to their string representations.
    """

    # Define multipliers for common SI prefixes
    prefixes = {
        "nano": 1e-9, "micro": 1e-6, "milli": 1e-3,
        "base": 1, "kilo": 1e3, "mega": 1e6,
        "giga": 1e9, "tera": 1e12,
    }

    # SI prefixes to their string representations
    prefix_to_string = {
        "nano": "n", "micro": r"$\mu$", "milli": "m",
        "base": "", "kilo": "k", "mega": "M",
        "giga": "G", "tera": "T"
    }

    # List of (magnitude, prefix) tuples
    magnitude_to_prefixes = [
        (-9, "nano"),
        (-6, "micro"),
        (-3, "milli"),
        (0, "base"),
        (3, "kilo"),
        (6, "mega"),
        (9, "giga"),
        (12, "tera")
    ]

    def __new__(cls, clsname, bases, attrs):
        # Initialize the class as usual
        new_class = super().__new__(cls, clsname, bases, attrs)

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
    """

    def __init__(
            self,
            long_label: str,
            short_label: str | None = None,
            string_format: str = '',
            base_values: numpy.ndarray | None = None,
            use_long_label_for_repr: bool = False,
            use_prefix: bool = None,
            value_representation: numpy.ndarray | None = None,
            normalized: bool = False,
            auto_scale: bool = True):

        self.long_label = long_label if long_label is not None else self.long_label
        self.short_label = short_label if short_label is not None else long_label.lower().replace(' ', '_')
        self.string_format = string_format if string_format is not None else self.string_format
        self.use_prefix = use_prefix if use_prefix is not None else self.use_prefix

        self.use_long_label_for_repr = use_long_label_for_repr

        self.value_representation = value_representation
        self.normalized = normalized
        self.is_base = False
        self.auto_scale = auto_scale
        self.set_base_values(base_values)

    def scale_values(self) -> None:
        if not self.use_prefix:
            self.long_prefix = ''
            self.short_prefix = ''
            self.values = self.base_values
            return

        if None in self.base_values or self.value_representation is not None:
            self.long_prefix = ''
            self.short_prefix = ''
            return

        if self.normalized:
            self.long_prefix = ''
            self.short_prefix = ''
            self.values = self.base_values / self.base_values.max()
            return

        long_prefix, short_prefix = self.get_closest_prefix_string()

        multiplier = UnitMeta.prefixes[long_prefix]

        self.long_prefix = long_prefix

        self.short_prefix = short_prefix

        self.values = self.base_values * (multiplier ** -self.power)

    def set_base_values(self, base_values: numpy.ndarray) -> numpy.ndarray:
        self.base_values = numpy.atleast_1d(base_values)

        self.scale_values()

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
        return numpy.size(self.base_values)

    @property
    def shape(self) -> tuple:
        """Returns the shape of the values."""
        return numpy.shape(self.values)

    @staticmethod
    def closest_prefix_order(order_of_magnitude: float) -> str:
        """
        Determines the closest SI prefix based on the order of magnitude of the values.

        Args:
            order_of_magnitude (float): The order of magnitude of the values.

        Returns:
            str: The closest SI prefix.
        """
        if order_of_magnitude < -9:
            return "nano"  # Below nano, remain at the lowest prefix
        elif order_of_magnitude < -6:
            return "nano"
        elif order_of_magnitude < -3:
            return "micro"
        elif order_of_magnitude < 0:
            return "milli"
        elif order_of_magnitude <= 3:
            return "base"
        elif order_of_magnitude < 6:
            return "kilo"
        elif order_of_magnitude < 9:
            return "mega"
        elif order_of_magnitude < 12:
            return "giga"
        else:
            return "tera"  # Above tera, remain at the highest prefix

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
            return self.values[index]

    def _get_unit_string(self, add_unit: bool, use_prefix: bool) -> str:
        """
        Constructs the unit string, including the appropriate SI prefix if required.

        Returns an empty string if add_unit is False.
        """
        if not add_unit:
            return ""

        unit = self.short_unit if self.unit else ""

        short_prefix = '' if self.short_prefix == 'base' else self.short_prefix

        return f"{short_prefix}{unit}"

# -
