import numpy as np
from fixed_point_sim import FixedPointSim, Mode
from fir_filter import FirFilter, QntzFormat, QntzFormatSet
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from scipy import signal
from fixed_point_setting import FixedPointSetting


def qntz_anal():
    simulator = FixedPointSim()
    simulator.plot_qntz_anal(
        mode=Mode.INPUT, qntz_format_set=QntzFormatSet(input=QntzFormat(fix_en=True))
    )
    input_frac_bit = 13
    simulator.plot_qntz_anal(
        mode=Mode.COEF,
        qntz_format_set=QntzFormatSet(
            input=QntzFormat(fix_en=True, frac_bit=input_frac_bit),
            coef=QntzFormat(fix_en=True),
        ),
    )
    coef_frac_bit = 15
    simulator.plot_qntz_anal(
        mode=Mode.MULT,
        qntz_format_set=QntzFormatSet(
            input=QntzFormat(fix_en=True, frac_bit=input_frac_bit),
            coef=QntzFormat(fix_en=True, frac_bit=coef_frac_bit),
            mult=QntzFormat(fix_en=True),
        ),
    )
    mult_frac_bit = 18
    simulator.plot_qntz_anal(
        mode=Mode.ADD,
        qntz_format_set=QntzFormatSet(
            input=QntzFormat(fix_en=True, frac_bit=input_frac_bit),
            coef=QntzFormat(fix_en=True, frac_bit=coef_frac_bit),
            mult=QntzFormat(fix_en=True, frac_bit=mult_frac_bit),
            add=QntzFormat(fix_en=True),
        ),
    )
    # add_frac_bit = 18


if __name__ == "__main__":
    # qntz_anal()
    # simulator = FixedPointSim(print_int_bit_en=True)
    # simulator.plot_qntz_output_in_time(
    # qntz_format_set=QntzFormatSet(
    #     input=QntzFormat(fix_en=True, frac_bit=13),
    #     coef=QntzFormat(fix_en=True, frac_bit=15),
    #     mult=QntzFormat(fix_en=True, frac_bit=18),
    #     add=QntzFormat(fix_en=True, frac_bit=18),
    # )
    # )
    # simulator.plot_qntz_filter_in_freq(frac_bit=15)

    qntz_format_set = QntzFormatSet(
        input=QntzFormat(fix_en=True, int_bit=1, frac_bit=13),
        coef=QntzFormat(fix_en=True, int_bit=1, frac_bit=15),
        mult=QntzFormat(fix_en=True, int_bit=1, frac_bit=18),
        add=QntzFormat(fix_en=True, int_bit=3, frac_bit=18),
    )

    simulator = FixedPointSim()
    setting = FixedPointSetting(
        input=simulator.input,
        coef=simulator.filter_coef,
        qntz_format_set=qntz_format_set,
    )
    setting.save_data(mode=Mode.INPUT)
    # setting.save_data(mode=Mode.COEF)
    # setting.print_coef_lut()

    # simulator.filter.qntz_return_int_en = True
    output = simulator.filter.apply(
        input=simulator.input, qntz_format_set=qntz_format_set
    )
    for i in range(20):
        print(int(output[i]*2**18))
