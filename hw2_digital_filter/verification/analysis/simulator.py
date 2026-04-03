import numpy as np
from models.filter_coef import FilterCoef
from models.fir_filter import FirFilter
from models.qntz_format import QntzFormatSet


class Simulator:
    def __init__(self, print_int_bit_en=False):
        self.coef = FilterCoef().v
        self.input = self._gen_input()
        self.filter = FirFilter(self.coef)
        self.ref_output = self.filter.apply_ref_model(input=self.input)
        self.output = self.filter.apply(
            input=self.input, qntz_format_set=QntzFormatSet(), det_int_bit_en=True
        )
        if print_int_bit_en:
            self.filter.max_val_set.get_int_bit_set()

    def run(self, qntz_format_set: QntzFormatSet) -> np.ndarray:
        return self.filter.apply(input=self.input, qntz_format_set=qntz_format_set)

    def run_reference(self) -> np.ndarray:
        return self.filter.apply_ref_model(input=self.input)

    def calc_rmse(self, a: np.ndarray, b: np.ndarray) -> float:
        assert len(a) == len(b)
        return np.sqrt(np.sum((a - b) ** 2) / len(b))

    def _gen_input(self) -> np.ndarray:
        n = np.arange(0, 144)
        return np.cos(-2 * np.pi / 128 * n) - np.cos(2 * np.pi * n / 4)