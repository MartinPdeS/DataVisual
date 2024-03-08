#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-

import pytest
import numpy
from DataVisual.units import components


@pytest.mark.parametrize("unit_string", components.__all__, ids=components.__all__)
def test_units(unit_string: str):
    unit_class = getattr(components, unit_string)
    unit = unit_class(
        base_values=numpy.linspace(0, 1, 10),
        long_label='Unit',
        short_label='U0'
    )

    print(unit)

# -
