import numpy as np
import plotly.graph_objs as go
import plotly.offline as pof
from plotly.subplots import make_subplots
from scipy import signal
from filter_coef import FilterCoef
from fir_filter import FirFilter, QntzFormatSet, Mode
from qntz_model import QntzModel, QntzFormat
from fir_filter import Mode


class FixedPointSetting(QntzModel):
    def __init__(self, input, coef, qntz_format_set: QntzFormatSet):
        super().__init__()
        self.input = input
        self.coef = coef
        self.qntz_format_set = qntz_format_set
        self.qntz_return_int_en = True

    def save_data(self, mode: Mode):
        if mode == Mode.INPUT:
            data_vec = self.quantizer_arr(
                input_arr=self.input, frac_bit=self.qntz_format_set.input.frac_bit
            )
            file_name = "input"
        else:  #  mode == Mode.COEF
            data_vec = self.quantizer_arr(
                input_arr=self.coef, frac_bit=self.qntz_format_set.coef.frac_bit
            )
            file_name = "coef"
        wrt_str = ""
        with open(
            f"..\\design\\digital_filter\\digital_filter.sim\\sim_1\\behav\\xsim\\{file_name}.txt",
            "w",
        ) as file:
            for data in data_vec:
                wrt_str += f"{data}\n"
            file.write(wrt_str)

    def print_coef_lut(self):
        data_vec = self.quantizer_arr(
            input_arr=self.coef, frac_bit=self.qntz_format_set.coef.frac_bit
        )
        for i, data in enumerate(data_vec):
            sign = "-" if data < 0 else ""
            lut_str = f"        {sign}{self.qntz_format_set.coef.total_bit_width()}'sd{abs(data)}"
            if i != len(data_vec) - 1:
                lut_str += ","
            print(lut_str)
