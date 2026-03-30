import numpy as np
from fixed_point_sim import FixedPointSim, Mode
from fir_filter import FirFilter, QntzFormat, QntzFormatSet


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
    simulator = FixedPointSim()
    simulator.plot_qntz_result(
        qntz_format_set=QntzFormatSet(
            input=QntzFormat(fix_en=True, frac_bit=13),
            coef=QntzFormat(fix_en=True, frac_bit=15),
            mult=QntzFormat(fix_en=True, frac_bit=18),
            add=QntzFormat(fix_en=True, frac_bit=18),
        )
    )
