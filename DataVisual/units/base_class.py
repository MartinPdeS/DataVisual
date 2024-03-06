import numpy


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
        use_prefix = attrs.get('use_prefix', False)

        power = attrs.get('power', 1)  # Default power is 1

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


class BaseUnit():
    position: int = None
    is_base: bool = False
    normalized: bool = False
    use_long_label_for_repr: bool = False
    use_prefix: bool = True

    def __init__(
            self,
            long_label: str,
            short_label: str | None = None,
            string_format: str | None = None,
            values: float | numpy.ndarray | None = None,
            use_long_label_for_repr: bool = False,
            use_prefix: bool = None,
            value_representation: float | numpy.ndarray | None = None):

        if string_format is not None:
            self.string_format = string_format

        if use_prefix is not None:
            self.use_prefix = use_prefix

        self.long_label = long_label

        self.short_label = long_label.lower().replace(' ', '_') if short_label is None else short_label

        self.value_representation = value_representation
        self.base_values = values
        self.use_long_label_for_repr = use_long_label_for_repr

    def __repr__(self) -> str:
        return f"{self.long_label} [{self.get_unit()}]"

    def get_unit(self):
        if self.normalized:
            return "A.U."
        else:
            return self.unit

    @property
    def size(self) -> int:
        """Returns the number of values."""
        return numpy.size(self.base_values)

    @property
    def shape(self) -> tuple:
        """Returns the shape of values."""
        return numpy.shape(self.base_values)

    @staticmethod
    def closest_prefix_order(order_of_magnitude: float) -> str:
        # Mapping order of magnitude to prefix
        # This time we ensure the selected prefix will result in a value >= 1 and < 1000
        if order_of_magnitude < -9:
            return "nano"  # Below nano, remain at the lowest prefix
        elif -9 <= order_of_magnitude < -6:
            return "nano"
        elif -6 <= order_of_magnitude < -3:
            return "micro"
        elif -3 <= order_of_magnitude < -2:
            return "milli"
        elif -2 <= order_of_magnitude < -1:
            return "centi"
        elif -1 <= order_of_magnitude < 0:
            return "deci"
        elif 0 <= order_of_magnitude < 1:
            return "base"
        elif 1 <= order_of_magnitude < 2:
            return "deca"
        elif 2 <= order_of_magnitude < 3:
            return "hecto"
        elif 3 <= order_of_magnitude < 6:
            return "kilo"
        elif 6 <= order_of_magnitude < 9:
            return "mega"
        elif 9 <= order_of_magnitude < 12:
            return "giga"
        else:
            return "tera"  # Above tera, remain at the highest prefix

    @property
    def values(self):
        if self.normalized:
            return self.base_values / self.base_values.max()
        return self.base_values

    def get_closest_prefix_string(self):
        """
        Retrieves the SI prefix string that represents the closest magnitude to unity
        for the current base_values.
        """
        base_value = numpy.max(self.base_values) if hasattr(self.base_values, "__iter__") else self.base_values
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
        """Returns a formatted string representation for the value at the given index."""
        label = self.short_label if use_short_repr else self.long_label

        label = label.replace('_', ' ')

        if self.value_representation is not None:
            value = self.value_representation[index]
            label += f" {value}"
            return label

        if self.use_long_label_for_repr:
            return label

        unit = self.short_unit if add_unit else ""

        if use_prefix and self.use_prefix:
            long_prefix, short_prefix = self.get_closest_prefix_string()
        else:
            long_prefix, short_prefix = 'base', 'base'

        if self.use_long_label_for_repr:
            return self.long_label

        if index is not None:
            value = getattr(self, long_prefix + '_' + self.unit)[index]
            label += f"={value:{self.string_format}}"

        if add_unit and (self.unit != ''):
            label += f" [{short_prefix}{unit}]"

        return label

    def get_values(self, index: int, use_prefix: bool = True):
        if use_prefix and self.use_prefix:
            long_prefix, short_prefix = self.get_closest_prefix_string()
        else:
            long_prefix, _ = 'base', 'base'

        if self.value_representation is not None:
            return self.value_representation[index]

        else:

            return getattr(self, long_prefix + '_' + self.unit)[index]

    def get_array(self, scaled: bool = False):
        if not scaled or not self.use_prefix:
            return self.base_values
        else:
            return self.get_scaled_array()

    def get_scaled_array(self) -> str:
        """Returns a formatted string representation for the value at the given index."""
        long_prefix, short_prefix = self.get_closest_prefix_string()
        return getattr(self, f'{long_prefix}_{self.get_unit()}')

# -
