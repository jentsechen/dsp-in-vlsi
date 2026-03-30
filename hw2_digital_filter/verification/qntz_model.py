import numpy as np


class QntzFormat:
    def __init__(self, fix_en=False, int_bit=15, frac_bit=16):
        self.fix_en = fix_en
        self.int_bit = int_bit
        self.frac_bit = frac_bit

    def total_bit_width(self):
        return 1 + self.int_bit + self.frac_bit


class QntzModel:
    def __init__(self):
        self.qntz_return_int_en = False

    def quantizer(self, input, frac_bit):
        if self.qntz_return_int_en:
            return int(np.floor(input * 2**frac_bit))
        return np.floor(input * 2**frac_bit) / 2**frac_bit

    def quantizer_arr(self, input_arr, frac_bit):
        output_array = []
        for input in input_arr:
            output_array.append(self.quantizer(input, frac_bit))
        return np.array(output_array)
