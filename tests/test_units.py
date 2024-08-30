#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import pytest
import numpy as np
from DataVisual.units import components

@pytest.mark.parametrize("unit_string", components.__all__, ids=components.__all__)
def test_units(unit_string: str):
    """
    Test the initialization and basic functionality of unit classes in the components module.

    This test dynamically creates instances of all unit classes defined in the `components` module.
    It initializes each unit with a linspace of values and checks if the unit can be instantiated and
    printed without errors.

    Args:
        unit_string (str): The name of the unit class to test, provided by pytest's parameterization.
    """
    # Retrieve the unit class from the components module using the unit_string
    unit_class = getattr(components, unit_string)

    # Initialize the unit with sample data
    unit = unit_class(
        base_values=np.linspace(0, 1, 10),
        long_label='Unit',
        short_label='U0'
    )

    # Print the unit to ensure it's been created successfully (primarily for debugging)
    print(unit)


if __name__ == "__main__":
    pytest.main([__file__])


# -
