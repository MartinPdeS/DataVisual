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
        "micro": "μ",
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


class BaseClass():
    position: int = None
    is_base: bool = False

    def __init__(self, long_label: str, short_label: str, values: float | numpy.ndarray):
        self.long_label = long_label
        self.short_label = short_label
        self.base_values = values

    def __repr__(self) -> str:
        return f"{self.long_label} [{self.unit}]"

    def get_value_representation_without_unit(self, index: int = None) -> str:
        """Returns a formatted string representation for the value at the given index."""
        if numpy.isscalar(self.base_values) or (index is None):
            value = self.base_values
        else:
            value = self.base_values[index]
        return f"{value:{self.string_format}}"

    def get_value_representation_with_unit(self, index: int = None) -> str:
        """Returns a formatted string representation for the value at the given index."""
        if numpy.isscalar(self.base_values) or (index is None):
            value = self.base_values
        else:
            value = self.base_values[index]
        return f"{value:{self.string_format}} {self.short_unit}"

    @property
    def size(self) -> int:
        """Returns the number of values."""
        return numpy.size(self.base_values)

    @staticmethod
    def closest_prefix_order(order_of_magnitude: float) -> str:
        prefix_orders = [-9, -6, -3, -2, -1, 0, 1, 2, 3, 6, 9, 12]
        prefixes = ["nano", "micro", "milli", "centi", "deci", "base", "deca", "hecto", "kilo", "mega", "giga", "tera"]
        closest = min(prefix_orders, key=lambda x: abs(x - order_of_magnitude))
        return prefixes[prefix_orders.index(closest)]

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

    def get_value_representation(self, index: int = None) -> str:
        """Returns a formatted string representation for the value at the given index."""
        long_prefix, short_prefix = self.get_closest_prefix_string()
        if numpy.isscalar(self.base_values) or (index is None):
            value = getattr(self, f'{long_prefix}_{self.unit}')
        else:
            value = getattr(self, f'{long_prefix}_{self.unit}')[index]
        return f"{value:{self.string_format}} {short_prefix}{self.short_unit}"
