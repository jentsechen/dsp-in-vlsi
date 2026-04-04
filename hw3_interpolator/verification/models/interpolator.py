import numpy as np
from enum import Enum, auto


class InterpMethod(Enum):
    Linear, Poly2, PwisePar = auto(), auto(), auto()


class Signal:
    @staticmethod
    def x1(m, phi: float = 1.0):
        theta = 2 * np.pi * (m / 10 + phi / 2)
        return np.cos(theta) + 1j * np.sin(theta)

    @staticmethod
    def x2(m, phi: float = 1.0):
        theta = 2 * np.pi * (m / 4 + phi / 3)
        return 2**-20 * (np.cos(theta) + 1j * np.sin(theta))


class InterpolatorModel:
    def __init__(self, signal):
        arr = np.asarray(signal)
        self.signal = arr if arr.dtype == object else arr.astype(complex)

    def linear(self, m: int, mu: float) -> complex:
        return mu * self.signal[m + 1] + (1 - mu) * self.signal[m]

    def poly2(self, m: int, mu: float) -> complex:
        c0 = (1 - mu) * (2 - mu) / 2
        cm1 = mu * (2 - mu)
        cm2 = -mu * (1 - mu) / 2
        return c0 * self.signal[m] + cm1 * self.signal[m + 1] + cm2 * self.signal[m + 2]

    def piecewise_parabolic(self, m: int, mu: float, alpha: float = 0.5) -> complex:
        c1 = -alpha * mu + alpha * mu**2
        c0 = 1 + (alpha - 1) * mu - alpha * mu**2
        cm1 = (alpha + 1) * mu - alpha * mu**2
        cm2 = -alpha * mu + alpha * mu**2
        return (
            c1 * self.signal[m - 1]
            + c0 * self.signal[m]
            + cm1 * self.signal[m + 1]
            + cm2 * self.signal[m + 2]
        )

    def interpolate_range(
        self,
        method: InterpMethod,
        m_range,
        mu_values,
        **kwargs,
    ) -> np.ndarray:
        _methods = {
            InterpMethod.Linear: self.linear,
            InterpMethod.Poly2: self.poly2,
            InterpMethod.PwisePar: self.piecewise_parabolic,
        }
        fn = _methods[method]
        m_list = list(m_range)
        mu_list = list(mu_values)
        return np.array(
            [[fn(m, mu, **kwargs) for mu in mu_list] for m in m_list],
            dtype=complex,
        )
