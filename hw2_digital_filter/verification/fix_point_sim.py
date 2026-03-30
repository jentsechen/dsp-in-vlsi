import numpy as np
from fixed_point_sim import FixedPointSim, Mode
from fir_filter import FirFilter, QntzFormat, QntzFormatSet

if __name__ == "__main__":
    simulator = FixedPointSim()
    simulator.plot_qntz(mode=Mode.INPUT,
                        qntz_format_set=QntzFormatSet(input=QntzFormat(fix_en=True, int_bit=1)))
    input_frac_bit = 13
    simulator.plot_qntz(mode=Mode.COEF,
                        qntz_format_set=QntzFormatSet(input=QntzFormat(fix_en=True, int_bit=1, frac_bit=input_frac_bit),
                                                      coef=QntzFormat(fix_en=True, int_bit=1)))
    coef_frac_bit = 15
    simulator.plot_qntz(mode=Mode.MULT,
                        qntz_format_set=QntzFormatSet(input=QntzFormat(fix_en=True, int_bit=1, frac_bit=input_frac_bit),
                                                      coef=QntzFormat(fix_en=True, int_bit=1, frac_bit=coef_frac_bit),
                                                      mult=QntzFormat(fix_en=True, int_bit=1)))
    mult_frac_bit = 18
    simulator.plot_qntz(mode=Mode.ADD,
                        qntz_format_set=QntzFormatSet(input=QntzFormat(fix_en=True, int_bit=1, frac_bit=input_frac_bit),
                                                      coef=QntzFormat(fix_en=True, int_bit=1, frac_bit=coef_frac_bit),
                                                      mult=QntzFormat(fix_en=True, int_bit=1, frac_bit=mult_frac_bit),
                                                      add=QntzFormat(fix_en=True, int_bit=1)))
    add_frac_bit = 18