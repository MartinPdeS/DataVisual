import numpy as np


def norm(Scalar):
    return np.sqrt(np.sum(np.abs(Scalar)**2))


def normalize(Scalar):
    return Scalar / norm(Scalar)


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
    match scale.lower():
        case 'milli':
            prefix = "m"
            factor = 1e3
        case 'micro':
            prefix = r"$\mu$"
            factor = 1e6
        case 'kilo':
            prefix = r"k"
            factor = 1e-3
        case 'mega':
            prefix = r"M"
            factor = 1e-6
        case 'giga':
            prefix = r"G"
            factor = 1e-9
        case _:
            raise ValueError('Scale value is not valid.')

    parameter.unit = f'{prefix}{parameter.unit}'

    if inverse_proportional:
        parameter.values /= factor
    else:
        parameter.values *= factor

# -
