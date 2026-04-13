import os
import sys
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from models.bf16 import _encode, _decode, bf16_add


def _bf16(s: int, e: int, m: int) -> int:
    return (s << 15) | (e << 7) | m


def _golden(a_bits: int, b_bits: int) -> int:
    return _encode(bf16_add(_decode(a_bits), _decode(b_bits)))


def _cases() -> list[tuple[int, int]]:
    cases = []

    # both zero
    cases.append((0x0000, 0x0000))

    # one operand zero
    cases.append((_bf16(0, 127, 0), 0x0000))   # 1.0 + 0
    cases.append((0x0000, _bf16(0, 127, 0)))   # 0 + 1.0

    # exact cancellation
    cases.append((_bf16(0, 127, 0), _bf16(1, 127,   0)))  # 1.0 + -1.0
    cases.append((_bf16(0, 127, 1), _bf16(1, 127,   1)))  # 1.0078.. + -1.0078..

    # same exponent, same sign
    cases.append((_bf16(0, 127,   0), _bf16(0, 127,   0)))  # 1.0  + 1.0  = 2.0
    cases.append((_bf16(1, 127,   0), _bf16(1, 127,   0)))  # -1.0 + -1.0 = -2.0
    cases.append((_bf16(0, 127, 127), _bf16(0, 127, 127)))  # near-2 + near-2 → right-shift norm

    # same exponent, opposite sign (large cancellation → left-shift norm)
    cases.append((_bf16(0, 127, 127), _bf16(1, 127,   0)))  # 1.992 + -1.0  → small pos
    cases.append((_bf16(0, 127,   1), _bf16(1, 127,   0)))  # 1.0078 + -1.0 → tiny pos

    # exponent difference tests
    for diff in [1, 2, 3, 4, 7, 8, 10, 15]:
        e_a = 150
        e_b = max(1, e_a - diff)
        for s_a, s_b in [(0, 0), (0, 1), (1, 1)]:
            cases.append((_bf16(s_a, e_a, 0), _bf16(s_b, e_b, 0)))
            cases.append((_bf16(s_a, e_a, 64), _bf16(s_b, e_b, 32)))

    # all four sign combos at representative values
    for s_a, s_b in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        cases.append((_bf16(s_a, 130, 0), _bf16(s_b, 128, 0)))   # 8.0 ± 2.0
        cases.append((_bf16(s_a, 130, 64), _bf16(s_b, 129, 32)))

    # near-max (overflow clamp)
    cases.append((_bf16(0, 254, 127), _bf16(0, 254, 127)))
    cases.append((_bf16(0, 254,   0), _bf16(0, 253,   0)))

    # near-min (underflow → 0)
    cases.append((_bf16(0, 1, 0), _bf16(1, 1, 0)))   # tiny - tiny = 0
    cases.append((_bf16(0, 4, 0), _bf16(1, 1, 0)))   # small - very small

    # random cases
    rng = random.Random(42)
    for _ in range(64):
        a = _bf16(rng.randint(0, 1), rng.randint(1, 254), rng.randint(0, 127))
        b = _bf16(rng.randint(0, 1), rng.randint(1, 254), rng.randint(0, 127))
        cases.append((a, b))

    return cases


def preview() -> None:
    cases = _cases()
    w = len(str(len(cases) - 1))
    print(f"{'#':{w}}  {'a':>14}  {'b':>14}  {'out':>14}  {'a_hex':>6}  {'b_hex':>6}  {'out_hex':>7}")
    print('-' * (w + 14*3 + 6*2 + 7 + 7*2 + 6))
    for i, (a_bits, b_bits) in enumerate(cases):
        gold = _golden(a_bits, b_bits)
        a_f  = _decode(a_bits)
        b_f  = _decode(b_bits)
        g_f  = _decode(gold)
        print(f"{i:{w}}  {a_f:>14.6g}  {b_f:>14.6g}  {g_f:>14.6g}  {a_bits:04x}    {b_bits:04x}    {gold:04x}")


def run(out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)
    cases = _cases()

    fa_path = os.path.join(out_dir, 'add_in_a.txt')
    fb_path = os.path.join(out_dir, 'add_in_b.txt')
    fg_path = os.path.join(out_dir, 'add_golden.txt')

    with open(fa_path, 'w') as fa, open(fb_path, 'w') as fb, open(fg_path, 'w') as fg:
        for a_bits, b_bits in cases:
            gold = _golden(a_bits, b_bits)
            fa.write(f'{a_bits:04x}\n')
            fb.write(f'{b_bits:04x}\n')
            fg.write(f'{gold:04x}\n')

    print(f'[gen_add] {len(cases)} cases → {out_dir}')


if __name__ == '__main__':
    _root = os.path.join(os.path.dirname(__file__), '..', '..', 'design', '01_RTL', 'vectors')
    run(os.path.normpath(_root))