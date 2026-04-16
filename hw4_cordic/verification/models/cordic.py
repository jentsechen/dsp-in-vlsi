import numpy as np


def scaling_factor(N: int) -> float:
    product = 1.0
    for i in range(N):
        product *= np.sqrt(1 + 2 ** (-2 * i))
    return 1.0 / product


def scaling_factors(n_range) -> np.ndarray:
    return np.array([scaling_factor(N) for N in n_range])