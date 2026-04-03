from pathlib import Path
import numpy as np
from models.interpolator import Signal, InterpolatorModel, InterpMethod
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


if __name__ == "__main__":
    task_q1()
    task_q2()
