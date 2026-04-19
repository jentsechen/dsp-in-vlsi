from pathlib import Path
import numpy as np
from models.cordic import avg_phase_error_fixedxy, scaling_factors
from plotting.plotter import Plotter

DIAGRAM = Path(__file__).parent.parent / "diagram"


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


if __name__ == "__main__":
    task_q1()
    task_q2()