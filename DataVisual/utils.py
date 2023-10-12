import numpy as np


def norm(Scalar):
    return np.sqrt(np.sum(np.abs(Scalar)**2))


def normalize(Scalar):
    return Scalar / norm(Scalar)

# -
