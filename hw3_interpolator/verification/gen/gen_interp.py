import os
import sys
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from models.bf16 import _encode, _decode, bf16_add, bf16_mul
from models.interpolator import Signal
from plotting.plotter import Plotter


def _half(bits: int) -> int:
    e = (bits >> 7) & 0xFF
    if e <= 1:
        return 0
    return (bits & 0x8000) | ((e - 1) << 7) | (bits & 0x7F)


def _negate(bits: int) -> int:
    e = (bits >> 7) & 0xFF
    if e == 0:
        return 0
    return bits ^ 0x8000


def _add(a: int, b: int) -> int:
    return _encode(bf16_add(_decode(a), _decode(b)))


def _mul(a: int, b: int) -> int:
    return _encode(bf16_mul(_decode(a), _decode(b)))


def _golden(
    x0_re: int, x0_im: int, x1_re: int, x1_im: int, x2_re: int, x2_im: int, mu: int
) -> tuple[int, int]:
    hx0_re = _half(x0_re)
    hx0_im = _half(x0_im)
    hx2_re = _half(x2_re)
    hx2_im = _half(x2_im)
    nx0_re = _negate(x0_re)
    nx0_im = _negate(x0_im)
    nx1_re = _negate(x1_re)
    nx1_im = _negate(x1_im)

    v2a_re = _add(hx0_re, nx1_re)
    v2a_im = _add(hx0_im, nx1_im)
    v2_re = _add(v2a_re, hx2_re)
    v2_im = _add(v2a_im, hx2_im)

    nv2_re = _negate(v2_re)
    nv2_im = _negate(v2_im)

    v1a_re = _add(x1_re, nx0_re)
    v1a_im = _add(x1_im, nx0_im)
    v1_re = _add(v1a_re, nv2_re)
    v1_im = _add(v1a_im, nv2_im)

    t2_re = _mul(mu, v2_re)
    t2_im = _mul(mu, v2_im)
    t1_re = _add(v1_re, t2_re)
    t1_im = _add(v1_im, t2_im)
    t3_re = _mul(mu, t1_re)
    t3_im = _mul(mu, t1_im)
    yc_re = _add(x0_re, t3_re)
    yc_im = _add(x0_im, t3_im)

    return yc_re, yc_im


def _cases() -> list[tuple[int, int, int, int, int, int, int]]:
    PHI = 1.0
    M_RANGE = range(10, 20)
    MU_VALUES = [k / 8 for k in range(8)]

    m_all = np.arange(0, 25)
    x1_samples = Signal.x1(m_all, phi=PHI)

    cases = []
    for m in M_RANGE:
        x0c = x1_samples[m]
        x1c = x1_samples[m + 1]
        x2c = x1_samples[m + 2]
        x0_re = _encode(float(x0c.real))
        x0_im = _encode(float(x0c.imag))
        x1_re = _encode(float(x1c.real))
        x1_im = _encode(float(x1c.imag))
        x2_re = _encode(float(x2c.real))
        x2_im = _encode(float(x2c.imag))
        for mu_f in MU_VALUES:
            mu = _encode(mu_f)
            cases.append((x0_re, x0_im, x1_re, x1_im, x2_re, x2_im, mu))

    return cases


def plot(out_dir: str) -> None:
    PHI = 1.0
    M_RANGE = range(10, 20)
    MU_VALUES = [k / 8 for k in range(8)]

    m_all = np.arange(0, 25)
    x1_samples = Signal.x1(m_all, phi=PHI)

    x_axis = np.array([m + mu for m in M_RANGE for mu in MU_VALUES])

    inputs = np.array([x1_samples[m] for m in M_RANGE for _ in MU_VALUES])

    cases = _cases()
    golden = np.array([
        _decode(yr) + 1j * _decode(yi)
        for c in cases
        for yr, yi in [_golden(*c)]
    ])

    os.makedirs(out_dir, exist_ok=True)
    plotter = Plotter()

    plotter.plot_two_complex_signals(
        inputs, "input x[m]",
        golden, "BF16 output y[m+μ]",
        path=os.path.join(out_dir, "interp_in_out.html"),
        png_path=os.path.join(out_dir, "interp_in_out.png"),
        x=x_axis,
        xaxis_title="m + μ",
    )

    true_vals = np.array([Signal.x1(m + mu, phi=PHI) for m in M_RANGE for mu in MU_VALUES])
    plotter.plot_interpolation_result(
        true_vals,
        [(golden, "BF16 poly2 interp.")],
        path=os.path.join(out_dir, "interp_error.html"),
        png_path=os.path.join(out_dir, "interp_error.png"),
        x=x_axis,
    )

    print(f"[gen_interp] plots → {out_dir}")


def run(out_dir: str) -> None:
    PHI = 1.0
    M_RANGE = range(10, 20)

    m_all = np.arange(0, 25)
    x1_samples = Signal.x1(m_all, phi=PHI)

    # interp_input.txt: one line per in_valid pulse, format "re_hex im_hex"
    # Needs x1[10]..x1[21]:
    #   x1[10], x1[11]          → shift register fill (no output)
    #   x1[12], ..., x1[21]     → one new sample per group, 8 outputs each
    input_indices = range(M_RANGE.start, M_RANGE.stop + 2)

    os.makedirs(out_dir, exist_ok=True)

    with open(os.path.join(out_dir, "interp_input.txt"), "w") as fin:
        for i in input_indices:
            s = x1_samples[i]
            re = _encode(float(s.real))
            im = _encode(float(s.imag))
            fin.write(f"{re:04x}{im:04x}\n")

    cases = _cases()
    with (
        open(os.path.join(out_dir, "interp_golden_y_re.txt"), "w") as fyr,
        open(os.path.join(out_dir, "interp_golden_y_im.txt"), "w") as fyi,
    ):
        for c in cases:
            yr, yi = _golden(*c)
            fyr.write(f"{yr:04x}\n")
            fyi.write(f"{yi:04x}\n")

    print(f"[gen_interp] {len(input_indices)} input samples, {len(cases)} golden outputs → {out_dir}")


if __name__ == "__main__":
    _root = os.path.join(
        os.path.dirname(__file__), "..", "..", "design", "01_RTL", "vectors"
    )
    run(os.path.normpath(_root))
    _diagram = os.path.join(os.path.dirname(__file__), "..", "..", "diagram", "Q6")
    plot(os.path.normpath(_diagram))
