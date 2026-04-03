import numpy as np


class QntzModel:
    def __init__(self):
        self.qntz_return_int_en = False

    def _scaled_floor(self, x, frac_bit):
        return np.floor(x * 2**frac_bit)

    def quantizer(self, input, frac_bit):
        if self.qntz_return_int_en:
            return int(self._scaled_floor(input, frac_bit))
        return self._scaled_floor(input, frac_bit) / 2**frac_bit

    def quantizer_arr(self, input_arr, frac_bit):
        if self.qntz_return_int_en:
            return self._scaled_floor(input_arr, frac_bit).astype(int)
        return self._scaled_floor(input_arr, frac_bit) / 2**frac_bit