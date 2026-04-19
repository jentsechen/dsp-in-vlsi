import numpy as np
from typing import Optional


# ── Scaling factor ────────────────────────────────────────────────────────────


def scaling_factor(N: int) -> float:
    product = 1.0
    for i in range(N):
        product *= np.sqrt(1 + 2 ** (-2 * i))
    return 1.0 / product


def scaling_factors(n_range) -> np.ndarray:
    return np.array([scaling_factor(N) for N in n_range])


# ── Fixed-point helpers ───────────────────────────────────────────────────────


def float_to_fixed(x: float, frac_bits: int) -> int:
    """Round float to nearest fixed-point integer (round half away from zero)."""
    return int(np.round(x * (2**frac_bits)))


def fixed_to_float(x_int: int, frac_bits: int) -> float:
    return x_int / (2**frac_bits)


def arith_right_shift(x: int, shift: int) -> int:
    """Arithmetic right shift — Python >> already sign-extends negative integers."""
    return x >> shift


# ── Elementary angles ─────────────────────────────────────────────────────────


def elementary_angles_float(N: int) -> np.ndarray:
    """theta_e(i) = arctan(2^{-i}), i = 0 .. N-1."""
    return np.array([np.arctan(2.0 ** (-i)) for i in range(N)])


def elementary_angles_fixed(N: int, frac_bits: int) -> list:
    """Quantised elementary angles as fixed-point integers."""
    return [float_to_fixed(np.arctan(2.0 ** (-i)), frac_bits) for i in range(N)]


# ── CSD / NAF representation ─────────────────────────────────────────────────


def to_naf(n: int) -> dict:
    """Convert non-negative integer n to Non-Adjacent Form (NAF == CSD).

    Returns {bit_position: digit} where digit in {+1, -1}.
    Bit position 0 is the LSB.
    """
    digits = {}
    pos = 0
    while n != 0:
        if n & 1:
            # digit is +1 if n mod 4 == 1, -1 if n mod 4 == 3
            digit = 2 - (n % 4)
            n -= digit
            digits[pos] = digit
        n >>= 1
        pos += 1
    return digits


def csd_of_scaling_factor(N: int, frac_bits: int) -> dict:
    """CSD representation of S(N) quantised to frac_bits fractional bits."""
    s_int = float_to_fixed(scaling_factor(N), frac_bits)
    return to_naf(s_int)


def apply_csd(x_int: int, csd: dict) -> int:
    """Multiply x_int by a CSD number using shift-and-add.

    csd maps bit_position -> digit where the CSD number equals
    sum(digit * 2^bit_position).  All bit_positions must be >= 0
    (the CSD number is a non-negative integer).

    Returns x_int * CSD_value as an integer.
    """
    result = 0
    for bit_pos, digit in csd.items():
        result += digit * (x_int << bit_pos)
    return result


def csd_nonzero_count(csd: dict) -> int:
    return len(csd)


# ── Floating-point reference CORDIC ──────────────────────────────────────────


def cordic_phase_float(X: float, Y: float, N: int) -> float:
    """Floating-point CORDIC arctangent: atan2(Y, X) using N micro-rotations."""
    theta_offset = 0.0
    if X < 0:
        # Check original Y sign before flipping
        theta_offset = np.pi if Y >= 0 else -np.pi
        X, Y = -X, -Y

    theta = 0.0
    for i in range(N):
        mu = -1 if Y >= 0 else 1
        theta_e = np.arctan(2.0 ** (-i))
        X_new = X - mu * Y * (2.0 ** (-i))
        Y_new = Y + mu * X * (2.0 ** (-i))
        X, Y = X_new, Y_new
        theta -= mu * theta_e

    return theta + theta_offset


def cordic_magnitude_float(X: float, Y: float, N: int) -> float:
    """Floating-point CORDIC magnitude: sqrt(X^2 + Y^2) using N micro-rotations."""
    if X < 0:
        X, Y = -X, -Y

    for i in range(N):
        mu = -1 if Y >= 0 else 1
        X_new = X - mu * Y * (2.0 ** (-i))
        Y_new = Y + mu * X * (2.0 ** (-i))
        X, Y = X_new, Y_new

    return scaling_factor(N) * X


# ── Bit-true fixed-point CORDIC ───────────────────────────────────────────────


def cordic_phase_fixed(
    X: float,
    Y: float,
    N: int,
    frac_bits_xy: int,
    frac_bits_theta: int,
) -> float:
    """Bit-true fixed-point CORDIC for phase (arctangent).

    Data formats (2's complement integers throughout):
      X, Y            : 1 sign + 1 integer + frac_bits_xy fractional  (frac_bits_xy+2 bits)
      theta (iter.)   : 1 sign + 1 integer + frac_bits_theta fractional
                        (CORDIC sum stays within ±sum(θ_e) ≈ ±1.74 rad < 2)
      theta (output)  : 1 sign + 2 integer + frac_bits_theta fractional
                        (after adding ±π offset; π ≈ 3.14 > 2, so one extra integer
                        bit is needed only at the final output adder)

    Micro-rotation (shift-and-add, no multiply):
      X[i+1] = X[i] - mu * (Y[i] >> i)
      Y[i+1] = Y[i] + mu * (X[i] >> i)

    Phase accumulation:
      theta[i+1] = theta[i] - mu * theta_e[i]     (theta_e from ROM)

    Initial stage maps X < 0 inputs to the first/fourth quadrant and adds
    a ±pi offset to the final phase.

    Args:
        X, Y            : floating-point inputs (quantised internally)
        N               : number of micro-rotations
        frac_bits_xy    : fractional bits for X/Y datapaths (word = frac_bits_xy+2)
        frac_bits_theta : fractional bits for phase accumulator and angle LUT

    Returns:
        phase estimate in radians (float)
    """
    theta_e_lut = elementary_angles_fixed(N, frac_bits_theta)

    # Initial stage: quadrant mapping so that X > 0
    theta_offset_int = 0
    if X < 0:
        # Check original Y sign before flipping
        theta_offset_int = (
            float_to_fixed(np.pi, frac_bits_theta)
            if Y >= 0
            else -float_to_fixed(np.pi, frac_bits_theta)
        )
        X, Y = -X, -Y

    X_int = float_to_fixed(X, frac_bits_xy)
    Y_int = float_to_fixed(Y, frac_bits_xy)
    theta_int = 0

    for i in range(N):
        mu = -1 if Y_int >= 0 else 1

        # Shift-and-add micro-rotation (exact integer arithmetic)
        X_int_new = X_int - mu * arith_right_shift(Y_int, i)
        Y_int_new = Y_int + mu * arith_right_shift(X_int, i)

        X_int = X_int_new
        Y_int = Y_int_new
        theta_int -= mu * theta_e_lut[i]

    theta_int += theta_offset_int
    return fixed_to_float(theta_int, frac_bits_theta)


def cordic_magnitude_fixed(
    X: float,
    Y: float,
    N: int,
    frac_bits_xy: int,
    csd: Optional[dict] = None,
    frac_bits_scale: int = 0,
) -> float:
    """Bit-true fixed-point CORDIC for magnitude.

    After N micro-rotations, X_int represents X(N) with frac_bits_xy fractional
    bits.  Magnitude = S(N) * X(N) where S(N) is applied via CSD shift-and-add.

    If csd is None the exact floating-point S(N) is used (useful as a reference).

    Args:
        X, Y            : floating-point inputs (quantised internally)
        N               : number of micro-rotations
        frac_bits_xy    : fractional bits for X/Y datapaths
        csd             : CSD digits of S(N) from csd_of_scaling_factor(); None
                          to use exact float scaling
        frac_bits_scale : fractional bits used when building csd (must match
                          the frac_bits argument passed to csd_of_scaling_factor)

    Returns:
        magnitude estimate (float)
    """
    if X < 0:
        X, Y = -X, -Y

    X_int = float_to_fixed(X, frac_bits_xy)
    Y_int = float_to_fixed(Y, frac_bits_xy)

    for i in range(N):
        mu = -1 if Y_int >= 0 else 1

        X_int_new = X_int - mu * arith_right_shift(Y_int, i)
        Y_int_new = Y_int + mu * arith_right_shift(X_int, i)

        X_int = X_int_new
        Y_int = Y_int_new

    if csd is not None:
        # Shift-and-add: result has (frac_bits_xy + frac_bits_scale) fractional bits
        result_int = apply_csd(X_int, csd)
        return fixed_to_float(result_int, frac_bits_xy + frac_bits_scale)
    else:
        return scaling_factor(N) * fixed_to_float(X_int, frac_bits_xy)


# ── Fixed X/Y only, float theta CORDIC ───────────────────────────────────────


def cordic_phase_fixedxy(X: float, Y: float, N: int, frac_bits_xy: int) -> float:
    theta_offset = 0.0
    if X < 0:
        theta_offset = np.pi if Y >= 0 else -np.pi
        X, Y = -X, -Y

    X_int = float_to_fixed(X, frac_bits_xy)
    Y_int = float_to_fixed(Y, frac_bits_xy)
    theta = 0.0

    for i in range(N):
        mu = -1 if Y_int >= 0 else 1
        X_int_new = X_int - mu * arith_right_shift(Y_int, i)
        Y_int_new = Y_int + mu * arith_right_shift(X_int, i)
        X_int = X_int_new
        Y_int = Y_int_new
        theta -= mu * np.arctan(2.0 ** (-i))

    return theta + theta_offset


def avg_phase_error_fixedxy(
    X_arr: np.ndarray,
    Y_arr: np.ndarray,
    N: int,
    frac_bits_xy: int,
) -> float:
    estimated = np.array([
        cordic_phase_fixedxy(x, y, N, frac_bits_xy)
        for x, y in zip(X_arr, Y_arr)
    ])
    reference = np.arctan2(Y_arr, X_arr)
    return float(np.mean(np.abs(estimated - reference)))


# ── Batch helpers (operate on arrays) ────────────────────────────────────────


def batch_phase_fixed(
    X_arr: np.ndarray,
    Y_arr: np.ndarray,
    N: int,
    frac_bits_xy: int,
    frac_bits_theta: int,
) -> np.ndarray:
    """Apply cordic_phase_fixed element-wise."""
    return np.array(
        [
            cordic_phase_fixed(x, y, N, frac_bits_xy, frac_bits_theta)
            for x, y in zip(X_arr, Y_arr)
        ]
    )


def batch_magnitude_fixed(
    X_arr: np.ndarray,
    Y_arr: np.ndarray,
    N: int,
    frac_bits_xy: int,
    csd: Optional[dict] = None,
    frac_bits_scale: int = 0,
) -> np.ndarray:
    """Apply cordic_magnitude_fixed element-wise."""
    return np.array(
        [
            cordic_magnitude_fixed(x, y, N, frac_bits_xy, csd, frac_bits_scale)
            for x, y in zip(X_arr, Y_arr)
        ]
    )


def avg_phase_error_fixed(
    X_arr: np.ndarray,
    Y_arr: np.ndarray,
    N: int,
    frac_bits_xy: int,
    frac_bits_theta: int,
) -> float:
    """Average absolute phase error over the test inputs.

    Reference is atan2(Y, X) in (-pi, pi] — the true output of the CORDIC
    algorithm — not the raw alpha_m angle (which can exceed pi).
    """
    estimated = batch_phase_fixed(X_arr, Y_arr, N, frac_bits_xy, frac_bits_theta)
    reference = np.arctan2(Y_arr, X_arr)
    return float(np.mean(np.abs(estimated - reference)))


def avg_magnitude_error_fixed(
    X_arr: np.ndarray,
    Y_arr: np.ndarray,
    N: int,
    frac_bits_xy: int,
    csd: Optional[dict] = None,
    frac_bits_scale: int = 0,
) -> float:
    """Average relative magnitude error over the 10 test inputs (inputs are unit-circle)."""
    estimated = batch_magnitude_fixed(
        X_arr, Y_arr, N, frac_bits_xy, csd, frac_bits_scale
    )
    true_mag = np.sqrt(X_arr**2 + Y_arr**2)
    return float(np.mean(np.abs(estimated - true_mag) / true_mag))
