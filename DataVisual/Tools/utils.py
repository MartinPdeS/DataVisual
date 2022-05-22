import itertools
import numpy           as np
from scipy.interpolate import griddata
from scipy             import ndimage
import re



def Norm(Scalar):
    return np.sqrt(np.sum(np.abs(Scalar)**2))


def Normalize(Scalar):
    return Scalar / Norm(Scalar)

def IO(text):
    txt = '\n' + '-' * 100 + '\n'
    txt += text
    txt += '\n' + '-' * 100
    return txt


UlistLike = (list, np.ndarray, tuple)

def _ToList(arg):

    if isinstance(arg, list):
        return np.asarray(arg)

    if not isinstance(arg, UlistLike):
        return np.asarray([arg])

    else:
        return arg


def ToList(*args):
    out = []
    for arg in args:
        if not isinstance(arg, UlistLike):
            out.append( [arg] )
        else:
            out.append(arg)

    if len(out) == 1: return out[0]

    return np.asarray(out)


def FormatStr(function):
    def wrapped(*args, **kwargs):
        args = (re.sub(r"\s+", "", arg.lower() ) if isinstance(arg, str) else arg for arg in args)

        kwargs = {k: re.sub(r"\s+", "", v.lower() ) if isinstance(v, str) else v for k, v in kwargs.items()}

        return function(*args, **kwargs)
    return wrapped


def FormatString(string):
    return re.sub(r"\s+", "", string.lower() )

# -
