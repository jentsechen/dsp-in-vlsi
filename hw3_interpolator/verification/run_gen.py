import os
import sys

from gen import gen_add

sys.path.insert(0, os.path.dirname(__file__))
from gen import gen_mul, gen_interp

if __name__ == '__main__':
    _base = os.path.dirname(__file__)
    rtl_dir = os.path.normpath(os.path.join(_base, '..', 'design', '01_RTL', 'vectors'))
    gl_dir  = os.path.normpath(os.path.join(_base, '..', 'design', '03_GATESIM', 'vectors'))

    gen_add.preview()
    gen_add.run(rtl_dir)
    gen_mul.preview()
    gen_mul.run(rtl_dir)
    gen_interp.run(rtl_dir)
    gen_interp.run(gl_dir)