from pathlib import Path
import numpy as np
from models.cordic import avg_phase_error_fixedxy, avg_phase_error_fixed, scaling_factors
from plotting.plotter import Plotter

DIAGRAM = Path(__file__).parent.parent / "diagram"
DOCUMENT = Path(__file__).parent.parent / "document"


def task_q1():
    out = DIAGRAM / "Q1"
    out.mkdir(parents=True, exist_ok=True)

    N_values = np.arange(1, 31)
    S = scaling_factors(N_values)

    plotter = Plotter()
    plotter.plot_signal(
        S,
        out / "scaling_factor.html",
        png_path=out / "scaling_factor.png",
        x=N_values,
        xaxis_title="N",
        yaxis_title="S(N)",
    )


def task_q2():
    out = DIAGRAM / "Q2"
    out.mkdir(parents=True, exist_ok=True)

    m = np.arange(10)
    alpha = (4 * m + 2) / 20.0 * np.pi
    X, Y = np.cos(alpha), np.sin(alpha)

    N = 30
    frac_bits_range = np.arange(5, 16)
    errors = np.array([
        avg_phase_error_fixedxy(X, Y, N, b)
        for b in frac_bits_range
    ])

    plotter = Plotter()
    plotter.plot_signal(
        errors,
        out / "phase_error_vs_wordlength.html",
        png_path=out / "phase_error_vs_wordlength.png",
        x=frac_bits_range,
        xaxis_title="wordlength of the fractional part (bits)",
        yaxis_title="avg. abs. phase error (rad)",
        hlines=[{"y": 2**-9, "color": "red", "dash": "dash", "annotation_text": "2⁻⁹"}],
    )


def task_q3_1(out):
    m = np.arange(10)
    alpha = (4 * m + 2) / 20.0 * np.pi
    X, Y = np.cos(alpha), np.sin(alpha)

    N_values = np.arange(1, 31)
    frac_bits_xy = 9
    errors = np.array([
        avg_phase_error_fixedxy(X, Y, N, frac_bits_xy)
        for N in N_values
    ])

    plotter = Plotter()
    plotter.plot_signal(
        errors,
        out / "phase_error_vs_micro_rotation.html",
        png_path=out / "phase_error_vs_micro_rotation.png",
        x=N_values,
        xaxis_title="number of micro-rotations",
        yaxis_title="avg. abs. phase error (rad)",
        hlines=[{"y": 2**-9, "color": "red", "dash": "dash", "annotation_text": "2⁻⁹"}],
    )


def task_q3_2(out):
    m = np.arange(10)
    alpha = (4 * m + 2) / 20.0 * np.pi
    X, Y = np.cos(alpha), np.sin(alpha)

    N = 10
    frac_bits_xy = 9
    frac_bits_theta_range = np.arange(5, 16)
    errors = np.array([
        avg_phase_error_fixed(X, Y, N, frac_bits_xy, b)
        for b in frac_bits_theta_range
    ])

    plotter = Plotter()
    plotter.plot_signal(
        errors,
        out / "phase_error_vs_theta_wordlength.html",
        png_path=out / "phase_error_vs_theta_wordlength.png",
        x=frac_bits_theta_range,
        xaxis_title="wordlength of the fractional part of elementary angles (bits)",
        yaxis_title="avg. abs. phase error (rad)",
        hlines=[{"y": 2**-9, "color": "red", "dash": "dash", "annotation_text": "2⁻⁹"}],
    )


def task_q3_3(out, N=10, frac_bits_theta=10):
    angles_float = [np.arctan(2.0**(-i)) for i in range(N)]
    angles_fixed = [int(np.round(a * 2**frac_bits_theta)) for a in angles_float]

    rows = []
    for i, (af, ai) in enumerate(zip(angles_float, angles_fixed)):
        bin_str = format(ai, f"0{frac_bits_theta}b")
        rows.append(f"        {i} & {af:.10f} & \\texttt{{0.{bin_str}}} \\\\")

    lines = [
        r"\begin{table}[htbp]",
        r"    \centering",
        r"    \begin{tabular}{ccc}",
        r"    \toprule",
        f"    $i$ & $\\theta_e(i) = \\arctan(2^{{-i}})$ (rad) & Binary fixed-point ({frac_bits_theta} frac.~bits) \\\\",
        r"    \midrule",
        *rows,
        r"    \bottomrule",
        r"    \end{tabular}",
        f"    \\caption{{Elementary angles $\\theta_e(i)$ in floating-point and {frac_bits_theta}-bit fixed-point binary representation}}",
        r"    \label{tab:elementary_angles}",
        r"\end{table}",
    ]

    (out / "elementary_angles_table.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")


def task_q3():
    out = DIAGRAM / "Q3"
    out.mkdir(parents=True, exist_ok=True)
    task_q3_1(out)
    task_q3_2(out)
    task_q3_3(DOCUMENT)


if __name__ == "__main__":
    # task_q1()
    # task_q2()
    task_q3()