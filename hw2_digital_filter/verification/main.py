from pathlib import Path
import numpy as np
from models.filter_coef import FilterCoef
from models.qntz_format import QntzFormat, QntzFormatSet
from analysis.simulator import Simulator
from analysis.verification import FuncVerification, VeriConfig
from plotting.plotter import Plotter

DIAGRAM = Path(__file__).parent.parent / "diagram"


def task_q1():
    out = DIAGRAM / "Q1"
    out.mkdir(parents=True, exist_ok=True)
    coef = FilterCoef().v
    plotter = Plotter()
    plotter.plot_signal(coef, out / "imp_resp.html", png_path=out / "imp_resp.png")
    plotter.plot_filter_freq_resp(coef, out / "freq_resp.html", png_path=out / "freq_resp.png")


def task_q2():
    out = DIAGRAM / "Q2"
    out.mkdir(parents=True, exist_ok=True)
    sim = Simulator()
    plotter = Plotter()
    plotter.plot_signal(sim.input, out / "input.html", png_path=out / "input.png")
    plotter.plot_signal(sim.output, out / "output.html", png_path=out / "output.png")


def task_q3():
    out = DIAGRAM / "Q3"
    out.mkdir(parents=True, exist_ok=True)

    INPUT_FRAC_BIT = 13
    COEF_FRAC_BIT = 15
    MULT_FRAC_BIT = 18
    FRAC_BIT_RANGE = np.arange(9, 21)

    sim = Simulator()
    plotter = Plotter()
    output_ft = sim.run(QntzFormatSet())

    configs = [
        (
            "input",
            QntzFormatSet(
                input=QntzFormat(fix_en=True),
            ),
        ),
        (
            "coef",
            QntzFormatSet(
                input=QntzFormat(fix_en=True, frac_bit=INPUT_FRAC_BIT),
                coef=QntzFormat(fix_en=True),
            ),
        ),
        (
            "mult",
            QntzFormatSet(
                input=QntzFormat(fix_en=True, frac_bit=INPUT_FRAC_BIT),
                coef=QntzFormat(fix_en=True, frac_bit=COEF_FRAC_BIT),
                mult=QntzFormat(fix_en=True),
            ),
        ),
        (
            "add",
            QntzFormatSet(
                input=QntzFormat(fix_en=True, frac_bit=INPUT_FRAC_BIT),
                coef=QntzFormat(fix_en=True, frac_bit=COEF_FRAC_BIT),
                mult=QntzFormat(fix_en=True, frac_bit=MULT_FRAC_BIT),
                add=QntzFormat(fix_en=True),
            ),
        ),
    ]

    for name, qntz_format_set in configs:
        errors = []
        for f in FRAC_BIT_RANGE:
            getattr(qntz_format_set, name).frac_bit = f
            errors.append(sim.calc_rmse(sim.run(qntz_format_set), output_ft))
        plotter.plot_rmse_vs_frac_bit(
            FRAC_BIT_RANGE,
            errors,
            out / f"qntz_{name}.html",
            out / f"qntz_{name}.png",
        )


def task_q4():
    out = DIAGRAM / "Q4"
    out.mkdir(parents=True, exist_ok=True)

    COEF_FRAC_BIT = 15
    qntz_format_set = QntzFormatSet(
        input=QntzFormat(fix_en=True, frac_bit=13),
        coef=QntzFormat(fix_en=True, frac_bit=COEF_FRAC_BIT),
        mult=QntzFormat(fix_en=True, frac_bit=18),
        add=QntzFormat(fix_en=True, frac_bit=18),
    )

    sim     = Simulator()
    plotter = Plotter()
    output_ft = sim.run(QntzFormatSet())
    output_fx = sim.run(qntz_format_set)

    plotter.plot_verification(
        golden=output_ft, result=output_fx, sim_name="fixed-point",
        path=out / "output_in_time.html",
        error=output_fx - output_ft,
        error_path=out / "output_error_in_time.html",
        png_path=out / "output_in_time.png",
        error_png_path=out / "output_error_in_time.png",
    )

    coef_fx = sim.filter.quantizer_arr(sim.coef, COEF_FRAC_BIT)
    plotter.plot_freq_response(
        coef_ft=sim.coef, coef_fx=coef_fx,
        path=out / "filter_in_freq.html",
        error_path=out / "filter_error_in_freq.html",
        png_path=out / "filter_in_freq.png",
        error_png_path=out / "filter_error_in_freq.png",
    )


VERI_DATA = Path(__file__).parent / "func_verification"


def task_q5():
    veri = FuncVerification(data_dir=VERI_DATA, diagram_dir=DIAGRAM)
    veri.run(VeriConfig("rtl_sim_paral_1", "RTL sim., 1-paral", "Q5"))


def task_q6():
    veri = FuncVerification(data_dir=VERI_DATA, diagram_dir=DIAGRAM)
    veri.run(VeriConfig("gl_sim_paral_1", "post syn. sim., 1-paral", "Q6", latency=7))


def task_q8():
    veri = FuncVerification(data_dir=VERI_DATA, diagram_dir=DIAGRAM)
    veri.run(VeriConfig("gl_sim_paral_2", "post syn. sim., 2-paral", "Q8", latency=14, multi_col=True))


if __name__ == "__main__":
    task_q1()
    task_q2()
    task_q3()
    task_q4()
    task_q5()
    task_q6()
    task_q8()
