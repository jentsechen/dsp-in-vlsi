import numpy as np


class FilterCoef:
    def __init__(self, n_taps=25, boundary=2, norm_en=False):
        self.v = self._gen(n_taps=n_taps, boundary=boundary, norm_en=norm_en)

    def _gen(self, n_taps, boundary, norm_en):
        t = np.linspace(-boundary, boundary, n_taps)
        sinc_out = np.sinc(t)
        if norm_en:
            return sinc_out / sum(sinc_out)
        return sinc_out