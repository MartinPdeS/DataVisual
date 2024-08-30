#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .multi_array import Array  # noqa: F403 F401
from .tables import Table  # noqa: F403 F401
from .units import *  # noqa: F403 F401

try:
    from ._version import version as __version__  # noqa: F401

except ImportError:
    __version__ = "0.0.0"

# -