import numpy as np
from enum import Enum, auto
from models.qntz_model import QntzModel
from models.qntz_format import QntzFormat, QntzFormatSet


class Mode(Enum):
    INPUT, COEF, MULT, ADD = auto(), auto(), auto(), auto()


class MaxValSet:
    def __init__(self):
        self.input = 0
        self.coef = 0
        self.mult = 0
        self.add = 0

    _attr = {Mode.INPUT: "input", Mode.COEF: "coef", Mode.MULT: "mult", Mode.ADD: "add"}

    def apply(self, data_vec, mode: Mode):
        attr = self._attr[mode]
        setattr(self, attr, self._iq_abs_max_ceil(data_vec, getattr(self, attr)))

    def _iq_abs_max_ceil(self, data_vec, local_max):
        return np.ceil(
            np.max([np.max(np.abs(data_vec.real)), np.max(np.abs(data_vec.imag)), local_max])
        )

    def _find_int_bit(self, data):
        if data < 1:
            return 0
        elif data == 1:
            return 1
        else:
            return int(np.ceil(np.log2(data)))

    def get_int_bit_set(self):
        for attr in self._attr.values():
            print(f"int bit of {attr}: {self._find_int_bit(getattr(self, attr))}")


class FirFilter(QntzModel):
    def __init__(self, coef):
        super().__init__()
        assert len(coef) % 2 == 1
        self.coef = coef
        self.ramp_len = int((len(self.coef) - 1) / 2)
        self.max_val_set = MaxValSet()

    def apply(self, input, qntz_format_set: QntzFormatSet, det_int_bit_en=False):
        if det_int_bit_en:
            self.max_val_set.apply(data_vec=input, mode=Mode.INPUT)
        input_pad = np.concatenate(
            [np.zeros(len(self.coef) - 1), input, np.zeros(len(self.coef) - 1)]
        )
        if qntz_format_set.input.fix_en:
            input_pad = self.quantizer_arr(input_pad, qntz_format_set.input.frac_bit)

        if det_int_bit_en:
            self.max_val_set.apply(data_vec=self.coef, mode=Mode.COEF)
        coef = (
            self.quantizer_arr(self.coef, qntz_format_set.coef.frac_bit)
            if qntz_format_set.coef.fix_en
            else self.coef
        )

        output = []
        for i in range(len(input) + len(self.coef) - 1):
            mult_out = input_pad[i : i + len(self.coef)] * coef
            if det_int_bit_en:
                self.max_val_set.apply(data_vec=mult_out, mode=Mode.MULT)
            if qntz_format_set.mult.fix_en:
                mult_out = self.quantizer_arr(mult_out, qntz_format_set.mult.frac_bit)

            if det_int_bit_en:
                add_out, add_out_vec = 0, []
                for m in mult_out:
                    add_out = self.quantizer(add_out + m, qntz_format_set.add.frac_bit)
                    add_out_vec.append(add_out)
                self.max_val_set.apply(data_vec=np.array(add_out_vec), mode=Mode.ADD)
            if qntz_format_set.add.fix_en:
                add_out = 0
                for m in mult_out:
                    add_out = self.quantizer(add_out + m, qntz_format_set.add.frac_bit)
            else:
                add_out = np.sum(mult_out)
            output.append(add_out)
        return np.array(output)[self.ramp_len : -self.ramp_len]

    def apply_ref_model(self, input):
        return np.convolve(a=input, v=self.coef)[self.ramp_len : -self.ramp_len]