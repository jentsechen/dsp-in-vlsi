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

    def apply(self, input, qntz_format_set: QntzFormatSet):
        input_pad = np.concatenate([np.zeros(len(self.coef)-1), input, np.zeros(len(self.coef)-1)])
        if qntz_format_set.input.fix_en:
            input_pad = self.quantizer_arr(input_pad, qntz_format_set.input.frac_bit)

        if qntz_format_set.coef.fix_en:
            coef = self.quantizer_arr(input_arr=self.coef, frac_bit=qntz_format_set.coef.frac_bit)
        else: 
            coef = self.coef

        output = []
        for i in range(len(input)+len(self.coef)-1):
            mult_out = input_pad[i:(i+len(self.coef))]*coef
            if qntz_format_set.mult.fix_en:
                mult_out = self.quantizer_arr(input_arr=mult_out, frac_bit=qntz_format_set.mult.frac_bit)
            if qntz_format_set.add.fix_en:
                add_out = 0
                for m in mult_out:
                    add_out = self.quantizer(input=add_out+m, frac_bit=qntz_format_set.add.frac_bit)
            else:
                add_out = np.sum(mult_out)
            output.append(add_out)
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