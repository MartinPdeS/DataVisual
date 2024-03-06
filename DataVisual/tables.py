from dataclasses import dataclass
from typing import List, Union

from DataVisual.units import BaseUnit


@dataclass
class Table:
    """
    Represents a table of parameters (BaseUnits) for data visualization.

    Attributes:
    -----------
    parameters : list of BaseUnit
        The list of parameters contained in the table.
    """
    parameters: List[BaseUnit]

    def __post_init__(self) -> None:
        """Initializes the Xtable by assigning positions to each parameter."""
        for idx, parameter in enumerate(self.parameters):
            parameter.position = idx

    def __getitem__(self, index: Union[int, slice]) -> Union[BaseUnit, List[BaseUnit]]:
        """Allows indexing directly into the parameters list."""
        return self.parameters[index]

    def __repr__(self) -> str:
        return f"Xtable(size={len(self.parameters)})"
