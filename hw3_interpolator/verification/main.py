from pathlib import Path
import numpy as np
from models.interpolator import Signal, InterpolatorModel, InterpMethod
from models.bf16 import bf16_add, bf16_mul, bf16_from_bits, bf16_to_bin, to_bf16c_array
from plotting.plotter import Plotter

DIAGRAM = Path(__file__).parent.parent / "diagram"


def task_q1():
    out = DIAGRAM / "Q1"
    out.mkdir(parents=True, exist_ok=True)

    PHI = 1.0
    start_point, end_point = 10, 20
    M_RANGE = range(start_point, end_point)
    MU_VALUES = [k / 8 for k in range(8)]

    m_samples = np.arange(0, 25)
    x1_samples = Signal.x1(m_samples, phi=PHI)
    model = InterpolatorModel(x1_samples)

    x_axis = np.append(
        np.array([[m + mu for mu in MU_VALUES] for m in M_RANGE]).flatten(),
        float(end_point),
    )
    golden = np.append(
        np.array(
            [[Signal.x1(m + mu, phi=PHI) for mu in MU_VALUES] for m in M_RANGE]
        ).flatten(),
        Signal.x1(20.0, phi=PHI),
    )
    linear = np.append(
        model.interpolate_range(InterpMethod.Linear, M_RANGE, MU_VALUES).flatten(),
        x1_samples[end_point],
    )
    poly2 = np.append(
        model.interpolate_range(InterpMethod.Poly2, M_RANGE, MU_VALUES).flatten(),
        x1_samples[end_point],
    )

    plotter = Plotter()
    plotter.plot_interpolation_result(
        golden,
        [(linear, "linear interp."), (poly2, "2nd poly. interp.")],
        out / "x1_interp.html",
        png_path=out / "x1_interp.png",
        x=x_axis,
    )


def task_q2():
    out = DIAGRAM / "Q2"
    out.mkdir(parents=True, exist_ok=True)

    PHI = 1.0
    start_point, end_point = 4, 8
    M_RANGE = range(start_point, end_point)
    MU_VALUES = [k / 8 for k in range(8)]

    m_samples = np.arange(0, 15)
    x2_samples = Signal.x2(m_samples, phi=PHI)
    model = InterpolatorModel(x2_samples)

    x_axis = np.append(
        np.array([[m + mu for mu in MU_VALUES] for m in M_RANGE]).flatten(),
        float(end_point),
    )
    golden = np.append(
        np.array(
            [[Signal.x2(m + mu, phi=PHI) for mu in MU_VALUES] for m in M_RANGE]
        ).flatten(),
        Signal.x2(float(end_point), phi=PHI),
    )
    linear = np.append(
        model.interpolate_range(InterpMethod.Linear, M_RANGE, MU_VALUES).flatten(),
        x2_samples[end_point],
    )
    pwise = np.append(
        model.interpolate_range(InterpMethod.PwisePar, M_RANGE, MU_VALUES).flatten(),
        x2_samples[end_point],
    )

    plotter = Plotter()
    plotter.plot_interpolation_result(
        golden,
        [(linear, "linear interp."), (pwise, "pwise. par. interp.")],
        out / "x2_interp.html",
        png_path=out / "x2_interp.png",
        x=x_axis,
    )


def task_q3():
    OUT = Path(__file__).parent.parent / "document" / "q3_results.tex"

    operands = [
        ("a", "add",  (1, "1000_0011", "0000_000"), (0, "1000_1011", "0000_011")),
        ("b", "add",  (1, "0000_0001", "0000_011"), (0, "0000_0001", "1111_010")),
        ("c", "mul",  (1, "0000_0010", "1100_000"), (0, "0111_1100", "0000_110")),
        ("d", "mul",  (0, "0110_0011", "1011_110"), (0, "1001_0011", "0101_000")),
    ]

    def _fmt_decimal(v: float) -> str:
        s = f"{v:.17g}"
        if "e" in s:
            mantissa, exp = s.split("e")
            return f"${mantissa}\\cdot10^{{{int(exp)}}}$"
        return f"${s}$"

    lines = []
    for label, op, (s1, e1, f1), (s2, e2, f2) in operands:
        a = bf16_from_bits(s1, e1, f1)
        b = bf16_from_bits(s2, e2, f2)
        result = bf16_add(a, b) if op == "add" else bf16_mul(a, b)
        sr, er, fr = bf16_to_bin(result)
        e_tex = er[:4] + r"\_" + er[4:]
        f_tex = fr[:4] + r"\_" + fr[4:]
        lines.append(f"\\newcommand{{\\q{label}S}}{{{sr}}}")
        lines.append(f"\\newcommand{{\\q{label}E}}{{{e_tex}}}")
        lines.append(f"\\newcommand{{\\q{label}F}}{{{f_tex}}}")
        lines.append(f"\\newcommand{{\\q{label}Decim}}{{{_fmt_decimal(result)}}}")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def task_q4():
    out = DIAGRAM / "Q4"
    out.mkdir(parents=True, exist_ok=True)

    PHI = 1.0
    start_point, end_point = 10, 20
    M_RANGE = range(start_point, end_point)
    MU_VALUES = [k / 8 for k in range(8)]

    m_samples = np.arange(0, 25)
    x1_samples = Signal.x1(m_samples, phi=PHI)
    x1_samples_bf16 = to_bf16c_array(x1_samples)

    model_double = InterpolatorModel(x1_samples)
    model_bf16 = InterpolatorModel(x1_samples_bf16)

    x_axis = np.append(
        np.array([[m + mu for mu in MU_VALUES] for m in M_RANGE]).flatten(),
        float(end_point),
    )
    poly2_double = np.append(
        model_double.interpolate_range(InterpMethod.Poly2, M_RANGE, MU_VALUES).flatten(),
        x1_samples[end_point],
    )
    poly2_bf16_raw = np.append(
        model_bf16.interpolate_range(InterpMethod.Poly2, M_RANGE, MU_VALUES).flatten(),
        x1_samples_bf16[end_point],
    )
    poly2_bf16 = np.array([complex(v) for v in poly2_bf16_raw])

    plotter = Plotter()
    plotter.plot_interpolation_result(
        poly2_double,
        [(poly2_double, "double"), (poly2_bf16, "BF16")],
        out / "x1_poly2_bf16_diff.html",
        png_path=out / "x1_poly2_bf16_diff.png",
        x=x_axis,
        golden_err=poly2_double,
        results_err=[(poly2_bf16, "BF16")],
        x_err=x_axis,
    )


if __name__ == "__main__":
    task_q1()
    task_q2()
    task_q3()
    task_q4()
