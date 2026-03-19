import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots

class QntzFormat:
    def __init__(self, fix_en=False, int_bit=15, frac_bit=16):
        self.fix_en = fix_en
        self.int_bit = int_bit
        self.frac_bit = frac_bit

class QntzFormatSet:
    def __init__(self, input=QntzFormat(), coef=QntzFormat(), mult=QntzFormat(), add=QntzFormat()):
        self.input = input
        self.coef = coef
        self.mult = mult
        self.add = add

class FirFilter:
    def __init__(self, coef):
        assert len(coef) % 2 == 1
        self.coef = coef
        self.ramp_len = int((len(self.coef)-1) / 2)

    def apply(self, input, qntz_format_set=QntzFormatSet()):
        input_pad = np.concatenate([np.zeros(len(self.coef)-1), input, np.zeros(len(self.coef)-1)])
        if qntz_format_set.input.fix_en == True:
            input_pad = self.quantizer_arr(input_pad, qntz_format_set.input.frac_bit)
        output = []
        for i in range(len(input)+len(self.coef)-1):
            output.append(np.sum(input_pad[i:(i+len(self.coef))]*self.coef))
        return np.array(output)[self.ramp_len:-self.ramp_len]

    def apply_ref_model(self, input):
        return np.convolve(a=input, v=self.coef)[self.ramp_len:-self.ramp_len]

    def quantizer(self, input, frac_bit):
        return np.floor(input * 2**frac_bit) / 2**frac_bit
    
    def quantizer_arr(self, input_arr, frac_bit):
        output_array = []
        for input in input_arr:
            output_array.append(self.quantizer(input, frac_bit))
        return np.array(output_array)