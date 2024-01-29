#!/usr/bin/env python
# -*- coding: utf-8 -*-

def scale_to_factor(scale: str, inverse_proportional: bool) -> float:
    """
    Returns the scale factor associated to a certain scale value.
    Has to be in ['nano', 'micro', 'milli', 'none', 'kilo', 'mega', 'giga']

    :param      scale:  The scale value
    :type       scale:  str

    :returns:   The scale prefix
    :rtype:     str
    """
    match scale.lower():
        case 'nano':
            factor = 1e9
        case 'micro':
            factor = 1e6
        case 'milli':
            factor = 1e3
        case 'none':
            return 1
        case 'kilo':
            factor = 1e-3
        case 'mega':
            factor = 1e-6
        case 'giga':
            factor = 1e-9
        case _:
            raise ValueError('Scale value is not valid.')

    if inverse_proportional:
        return 1 / factor
    else:
        return factor


def scale_to_prefix(scale: str) -> str:
    """
    Returns the prefix associated to a certain scale value.
    Has to be in ['nano', 'micro', 'milli', 'none', 'kilo', 'mega', 'giga']

    :param      scale:  The scale value
    :type       scale:  str

    :returns:   The scale prefix
    :rtype:     str
    """
    match scale.lower():
        case 'nano':
            prefix = "n"
        case 'micro':
            prefix = r"$\mu$"
        case 'milli':
            prefix = "m"
        case 'none':
            return ""
        case 'kilo':
            prefix = "k"
        case 'mega':
            prefix = "M"
        case 'giga':
            prefix = "G"
        case _:
            raise ValueError('Scale value is not valid.')

    return prefix


def scale_unit(parameter: object, scale: str, inverse_proportional: bool = False) -> None:
    """
    Function that scales the unit an arrays of the parameter

    :param      scale:                 The scale
    :type       scale:                 str
    :param      inverse_proportional:  The inverse proportional
    :type       inverse_proportional:  bool

    :returns:   No return
    :rtype:     None
    """
    prefactor = scale_to_factor(
        scale=parameter.scale,
        inverse_proportional=not inverse_proportional
    )

    parameter.scale = scale

    factor = scale_to_factor(
        scale=scale,
        inverse_proportional=inverse_proportional
    )

    prefix = scale_to_prefix(scale=scale)

    parameter.unit = f'{prefix}{parameter.unit}'

    parameter.values *= factor * prefactor


# -
