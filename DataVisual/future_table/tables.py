from DataVisual.future_table.base_class import BaseClass, UnitMeta


class Length(BaseClass, metaclass=UnitMeta):
    unit: str = 'meter'
    short_unit: str = 'm'
    is_inverse: bool = False
    string_format: str = '.2f'
    power: int = 1

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class Area(BaseClass, metaclass=UnitMeta):
    unit: str = 'area'
    short_unit: str = 'm^2'
    is_inverse: bool = False
    string_format: str = '.2f'
    power: int = 2

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
