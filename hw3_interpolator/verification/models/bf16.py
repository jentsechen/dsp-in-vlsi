import numpy as np


S_BITS = 1
E_BITS = 8
M_BITS = 7
E_BIAS = 127
E_MAX = (1 << E_BITS) - 1
M_MASK = (1 << M_BITS) - 1


def _encode(value: float) -> int:
    if value == 0.0:
        return 0
    s = 1 if value < 0 else 0
    abs_val = abs(value)
    e_unbiased = int(np.floor(np.log2(abs_val)))
    e = e_unbiased + E_BIAS
    if e <= 0:
        return 0
    if e >= E_MAX:
        e = E_MAX - 1
    m_full = abs_val / (2 ** e_unbiased) - 1.0
    m = int(m_full * (1 << M_BITS))
    m = min(m, M_MASK)
    return (s << (E_BITS + M_BITS)) | (e << M_BITS) | m


def _decode(bits: int) -> float:
    s = (bits >> (E_BITS + M_BITS)) & 1
    e = (bits >> M_BITS) & ((1 << E_BITS) - 1)
    m = bits & M_MASK
    if e == 0:
        return 0.0
    value = (1.0 + m / (1 << M_BITS)) * (2 ** (e - E_BIAS))
    return -value if s else value


def _truncate(bits: int) -> int:
    s = (bits >> (E_BITS + M_BITS)) & 1
    e = (bits >> M_BITS) & ((1 << E_BITS) - 1)
    m = bits & M_MASK
    return (s << (E_BITS + M_BITS)) | (e << M_BITS) | m


def bf16_add(a: float, b: float) -> float:
    a_bits = _encode(a)
    b_bits = _encode(b)

    s_a = (a_bits >> (E_BITS + M_BITS)) & 1
    e_a = (a_bits >> M_BITS) & ((1 << E_BITS) - 1)
    m_a = a_bits & M_MASK

    s_b = (b_bits >> (E_BITS + M_BITS)) & 1
    e_b = (b_bits >> M_BITS) & ((1 << E_BITS) - 1)
    m_b = b_bits & M_MASK

    if e_a == 0 and e_b == 0:
        return 0.0

    sig_a = (1 << M_BITS) | m_a
    sig_b = (1 << M_BITS) | m_b

    if e_a >= e_b:
        shift = e_a - e_b
        sig_b >>= shift
        e_out = e_a
    else:
        shift = e_b - e_a
        sig_a >>= shift
        e_out = e_b

    val_a = sig_a if s_a == 0 else -sig_a
    val_b = sig_b if s_b == 0 else -sig_b
    val_sum = val_a + val_b

    if val_sum == 0:
        return 0.0

    s_out = 1 if val_sum < 0 else 0
    mag = abs(val_sum)

    msb = mag.bit_length() - 1
    if msb > M_BITS:
        mag >>= (msb - M_BITS)
        e_out += (msb - M_BITS)
    elif msb < M_BITS:
        mag <<= (M_BITS - msb)
        e_out -= (M_BITS - msb)

    if e_out <= 0:
        return 0.0
    if e_out >= E_MAX:
        e_out = E_MAX - 1

    m_out = mag & M_MASK
    result_bits = (s_out << (E_BITS + M_BITS)) | (e_out << M_BITS) | m_out
    return _decode(_truncate(result_bits))


def bf16_mul(a: float, b: float) -> float:
    a_bits = _encode(a)
    b_bits = _encode(b)

    s_a = (a_bits >> (E_BITS + M_BITS)) & 1
    e_a = (a_bits >> M_BITS) & ((1 << E_BITS) - 1)
    m_a = a_bits & M_MASK

    s_b = (b_bits >> (E_BITS + M_BITS)) & 1
    e_b = (b_bits >> M_BITS) & ((1 << E_BITS) - 1)
    m_b = b_bits & M_MASK

    if e_a == 0 or e_b == 0:
        return 0.0

    s_out = s_a ^ s_b
    e_out = e_a + e_b - E_BIAS - M_BITS

    sig_a = (1 << M_BITS) | m_a
    sig_b = (1 << M_BITS) | m_b
    prod = sig_a * sig_b

    msb = prod.bit_length() - 1
    target = M_BITS
    if msb > target:
        prod >>= (msb - target)
        e_out += (msb - target)
    elif msb < target:
        prod <<= (target - msb)
        e_out -= (target - msb)

    if e_out <= 0:
        return 0.0
    if e_out >= E_MAX:
        e_out = E_MAX - 1

    m_out = prod & M_MASK
    result_bits = (s_out << (E_BITS + M_BITS)) | (e_out << M_BITS) | m_out
    return _decode(_truncate(result_bits))


class BF16:
    def __init__(self, v: float):
        self.v = float(v)

    def __add__(self, other):
        return BF16(bf16_add(self.v, float(other)))

    def __radd__(self, other):
        return BF16(bf16_add(float(other), self.v))

    def __mul__(self, other):
        return BF16(bf16_mul(self.v, float(other)))

    def __rmul__(self, other):
        return BF16(bf16_mul(float(other), self.v))

    def __neg__(self):
        return BF16(-self.v)

    def __float__(self):
        return self.v

    def __repr__(self):
        return f"BF16({self.v})"


class BF16Complex:
    def __init__(self, real, imag=0.0):
        self.real = BF16(float(real)) if not isinstance(real, BF16) else real
        self.imag = BF16(float(imag)) if not isinstance(imag, BF16) else imag

    def __add__(self, other):
        other = _to_bf16c(other)
        return BF16Complex(self.real + other.real, self.imag + other.imag)

    def __radd__(self, other):
        return _to_bf16c(other) + self

    def __mul__(self, other):
        other = _to_bf16c(other)
        r = self.real * other.real + (-(self.imag * other.imag))
        i = self.real * other.imag + self.imag * other.real
        return BF16Complex(r, i)

    def __rmul__(self, other):
        return _to_bf16c(other) * self

    def __neg__(self):
        return BF16Complex(-self.real, -self.imag)

    def __complex__(self):
        return complex(self.real.v, self.imag.v)

    def __float__(self):
        return self.real.v

    def __repr__(self):
        return f"BF16Complex({self.real.v}, {self.imag.v})"


def _to_bf16c(v) -> BF16Complex:
    if isinstance(v, BF16Complex):
        return v
    if isinstance(v, BF16):
        return BF16Complex(v)
    if isinstance(v, complex):
        return BF16Complex(v.real, v.imag)
    return BF16Complex(float(v))


def bf16_from_bits(s: int, e_str: str, f_str: str) -> float:
    e = int(e_str.replace("_", ""), 2)
    f = int(f_str.replace("_", ""), 2)
    bits = (s << (E_BITS + M_BITS)) | (e << M_BITS) | f
    return _decode(bits)


def bf16_to_bin(value: float) -> tuple[int, str, str]:
    bits = _encode(value)
    s = (bits >> (E_BITS + M_BITS)) & 1
    e = (bits >> M_BITS) & ((1 << E_BITS) - 1)
    m = bits & M_MASK
    e_str = f"{e:08b}"
    f_str = f"{m:07b}"
    return s, e_str, f_str


def to_bf16c_array(arr) -> np.ndarray:
    arr = np.asarray(arr)
    out = np.empty(arr.shape, dtype=object)
    for idx in np.ndindex(arr.shape):
        v = arr[idx]
        out[idx] = BF16Complex(v.real, v.imag)
    return out