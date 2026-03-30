import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from enum import Enum, auto


class Mode(Enum):
    INPUT, COEF, MULT, ADD = auto(), auto(), auto(), auto()


class QntzFormat:
    def __init__(self, fix_en=False, int_bit=15, frac_bit=16):
        self.fix_en = fix_en
        self.int_bit = int_bit
        self.frac_bit = frac_bit


class QntzFormatSet:
    def __init__(
        self, input=QntzFormat(), coef=QntzFormat(), mult=QntzFormat(), add=QntzFormat()
    ):
        self.input = input
        self.coef = coef
        self.mult = mult
        self.add = add


class MaxValSet:
    def __init__(self):
        self.input = 0
        self.coef = 0
        self.mult = 0
        self.add = 0

    def apply(self, data_vec, mode: Mode):
        if mode == Mode.INPUT:
            self.input = self.iq_abs_max_ceil(data_vec=data_vec, local_max=self.input)
        elif mode == Mode.COEF:
            self.coef = self.iq_abs_max_ceil(data_vec=data_vec, local_max=self.coef)
        elif mode == Mode.MULT:
            self.mult = self.iq_abs_max_ceil(data_vec=data_vec, local_max=self.mult)
        else:  # mode == Mode.ADD
            self.add = self.iq_abs_max_ceil(data_vec=data_vec, local_max=self.add)

    def iq_abs_max_ceil(self, data_vec, local_max):
        max_val = np.max(
            np.array(
                [
                    np.max(np.abs(data_vec.real)),
                    np.max(np.abs(data_vec.imag)),
                    local_max,
                ]
            )
        )
        return np.ceil(max_val)

    def find_int_bit(self, data):
        if data < 1:
            return 0
        else:
            return int(np.ceil(np.log2(data)))

    def get_int_bit_set(self):
        print(f"int bit of input: {self.find_int_bit(self.input)}")
        print(f"int bit of coef: {self.find_int_bit(self.coef)}")
        print(f"int bit of mult: {self.find_int_bit(self.mult)}")
        print(f"int bit of add: {self.find_int_bit(self.add)}")


class FirFilter:
    def __init__(self, coef):
        assert len(coef) % 2 == 1
        self.coef = coef
        self.ramp_len = int((len(self.coef) - 1) / 2)
        self.max_val_sel = MaxValSet()

    def apply(self, input, qntz_format_set: QntzFormatSet, det_int_bit_en=False):
        if det_int_bit_en:
            self.max_val_sel.apply(data_vec=input, mode=Mode.INPUT)
        input_pad = np.concatenate(
            [np.zeros(len(self.coef) - 1), input, np.zeros(len(self.coef) - 1)]
        )
        if qntz_format_set.input.fix_en:
            input_pad = self.quantizer_arr(input_pad, qntz_format_set.input.frac_bit)

        if det_int_bit_en:
            self.max_val_sel.apply(data_vec=self.coef, mode=Mode.COEF)
        if qntz_format_set.coef.fix_en:
            coef = self.quantizer_arr(
                input_arr=self.coef, frac_bit=qntz_format_set.coef.frac_bit
            )
        else:
            coef = self.coef

        output = []
        for i in range(len(input) + len(self.coef) - 1):
            mult_out = input_pad[i : (i + len(self.coef))] * coef
            if det_int_bit_en:
                self.max_val_sel.apply(data_vec=mult_out, mode=Mode.MULT)
            if qntz_format_set.mult.fix_en:
                mult_out = self.quantizer_arr(
                    input_arr=mult_out, frac_bit=qntz_format_set.mult.frac_bit
                )

            if det_int_bit_en:
                add_out = 0
                add_out_vec = []
                for m in mult_out:
                    add_out = self.quantizer(
                        input=add_out + m, frac_bit=qntz_format_set.add.frac_bit
                    )
                    add_out_vec.append(add_out)
                self.max_val_sel.apply(data_vec=np.array(add_out_vec), mode=Mode.ADD)
            if qntz_format_set.add.fix_en:
                add_out = 0
                for m in mult_out:
                    add_out = self.quantizer(
                        input=add_out + m, frac_bit=qntz_format_set.add.frac_bit
                    )
            else:
                add_out = np.sum(mult_out)
            output.append(add_out)
        return np.array(output)[self.ramp_len : -self.ramp_len]

    def apply_ref_model(self, input):
        return np.convolve(a=input, v=self.coef)[self.ramp_len : -self.ramp_len]

    def quantizer(self, input, frac_bit):
        return np.floor(input * 2**frac_bit) / 2**frac_bit

    def quantizer_arr(self, input_arr, frac_bit):
        output_array = []
        for input in input_arr:
            output_array.append(self.quantizer(input, frac_bit))
        return np.array(output_array)
