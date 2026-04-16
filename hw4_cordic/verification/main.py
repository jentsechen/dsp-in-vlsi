from pathlib import Path
import numpy as np
from models.cordic import scaling_factors
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
        name="S(N)",
    )


if __name__ == "__main__":
    task_q1()