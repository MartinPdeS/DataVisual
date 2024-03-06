from DataVisual.units.base_class import BaseUnit, UnitMeta

__all__ = [
    'Length',
    'Area',
    'Mass',
    'Power',
    'Energy',
    'Index',
    'Radian',
    'Degree',
    'Amplitude',
    'Efficiency',
    'Custom',
]


class Length(BaseUnit, metaclass=UnitMeta):
    unit: str = 'meter'
    short_unit: str = 'm'
    is_inverse: bool = False
    string_format: str = '.0f'
    power: int = 1

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class Area(BaseUnit, metaclass=UnitMeta):
    unit: str = 'area'
    short_unit: str = r'm$^2$'
    is_inverse: bool = False
    string_format: str = '.0f'
    power: int = 2

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class Mass(BaseUnit, metaclass=UnitMeta):
    unit: str = 'gram'
    short_unit: str = 'g'
    is_inverse: bool = False
    string_format: str = '.0f'
    power: int = 1

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class Power(BaseUnit, metaclass=UnitMeta):
    unit: str = 'watt'
    short_unit: str = 'Watt'
    is_inverse: bool = False
    string_format: str = '.0f'
    power: int = 1

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class Energy(BaseUnit, metaclass=UnitMeta):
    unit: str = 'joule'
    short_unit: str = 'J'
    is_inverse: bool = False
    string_format: str = '.0f'
    power: int = 1

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class Index(BaseUnit, metaclass=UnitMeta):
    unit: str = ''
    short_unit: str = ''
    is_inverse: bool = False
    string_format: str = '.2f'
    power: int = 1

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class Radian(BaseUnit, metaclass=UnitMeta):
    unit: str = 'radian'
    short_unit: str = 'rad'
    is_inverse: bool = False
    string_format: str = '.1f'
    power: int = 1

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class Degree(BaseUnit, metaclass=UnitMeta):
    unit: str = 'degree'
    short_unit: str = 'deg'
    is_inverse: bool = False
    string_format: str = '.1f'
    power: int = 1

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class Amplitude(BaseUnit, metaclass=UnitMeta):
    unit: str = 'amplitude'
    short_unit: str = 'amp.'
    is_inverse: bool = False
    string_format: str = '.1f'
    power: int = 1

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class Efficiency(BaseUnit, metaclass=UnitMeta):
    unit: str = ''
    short_unit: str = ''
    is_inverse: bool = False
    string_format: str = '.1f'
    power: int = 1

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class Custom(BaseUnit, metaclass=UnitMeta):
    unit: str = ''
    short_unit: str = ''
    is_inverse: bool = False
    string_format: str = '.1f'
    power: int = 1

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

# -
