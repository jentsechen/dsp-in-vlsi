from pathlib import Path
import numpy as np
from models.cordic import avg_phase_error_fixedxy, avg_phase_error_fixed, scaling_factors, scaling_factor, avg_magnitude_error_fixed, csd_of_scaling_factor, float_to_fixed
from plotting.plotter import Plotter

DIAGRAM = Path(__file__).parent.parent / "diagram"
DOCUMENT = Path(__file__).parent.parent / "document"


def test_inputs():
    m = np.arange(10)
    alpha = (4 * m + 2) / 20.0 * np.pi
    return np.cos(alpha), np.sin(alpha)


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

    X, Y = test_inputs()

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
    X, Y = test_inputs()

    N_values = np.arange(1, 16)
    frac_bits_xy = 12
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
    X, Y = test_inputs()

    N = 10
    frac_bits_xy = 12
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


def task_q4():
    out = DIAGRAM / "Q4"
    out.mkdir(parents=True, exist_ok=True)

    X, Y = test_inputs()

    frac_bits_xy = 12
    N_values = np.arange(1, 16)
    errors = np.array([avg_magnitude_error_fixed(X, Y, N, frac_bits_xy) for N in N_values])

    plotter = Plotter()
    plotter.plot_signal(
        errors,
        out / "error_vs_N_magnitude.html",
        png_path=out / "error_vs_N_magnitude.png",
        x=N_values,
        xaxis_title="number of micro-rotations",
        yaxis_title="avg. rel. magnitude error",
        hlines=[{"y": 1e-3, "color": "red", "dash": "dash", "annotation_text": "0.1%"}],
    )


def task_q5_1():
    out = DIAGRAM / "Q5"
    out.mkdir(parents=True, exist_ok=True)

    X, Y = test_inputs()
    frac_bits_xy = 12

    N = 10

    frac_bits_range = np.arange(5, 16)
    errors = np.array([
        avg_magnitude_error_fixed(X, Y, N, frac_bits_xy, csd_of_scaling_factor(N, b), b)
        for b in frac_bits_range
    ])

    plotter = Plotter()
    plotter.plot_signal(
        errors,
        out / "error_vs_csd_frac_bits.html",
        png_path=out / "error_vs_csd_frac_bits.png",
        x=frac_bits_range,
        xaxis_title="fractional bits of CSD scaling factor",
        yaxis_title="avg. rel. magnitude error",
        hlines=[{"y": 1e-3, "color": "red", "dash": "dash", "annotation_text": "0.1%"}],
    )


def task_q5_2():
    X, Y = test_inputs()
    frac_bits_xy = 12
    N = 10

    frac_bits = next(
        b for b in range(5, 21)
        if avg_magnitude_error_fixed(X, Y, N, frac_bits_xy, csd_of_scaling_factor(N, b), b) < 1e-3
    )

    s_float = scaling_factor(N)
    s_int = float_to_fixed(s_float, frac_bits)
    bin_str = format(s_int, f"0{frac_bits}b")
    csd = csd_of_scaling_factor(N, frac_bits)
    csd_terms = " ".join(
        f"{'−' if d < 0 else '+'}2^{p}" for p, d in sorted(csd.items())
    )

    print(f"S({N}) = {s_float:.10f}")
    print(f"Fractional bits: {frac_bits}")
    print(f"Fixed-point integer: {s_int} = 0b{bin_str}")
    print(f"Binary fixed-point: 0.{bin_str}")
    print(f"CSD: {csd_terms}  (over 2^{frac_bits})")


def task_q5():
    task_q5_1()
    task_q5_2()


if __name__ == "__main__":
    task_q1()
    task_q2()
    task_q3()
    task_q4()
    task_q5()