import os
import sys

from gen import gen_add

sys.path.insert(0, os.path.dirname(__file__))
from gen import gen_mul, gen_interp

if __name__ == '__main__':
    vectors_dir = os.path.normpath(
        os.path.join(os.path.dirname(__file__), '..', 'design', '01_RTL', 'vectors')
    )
    gen_add.preview()
    gen_add.run(vectors_dir)
    gen_mul.preview()
    gen_mul.run(vectors_dir)
    gen_interp.run(vectors_dir)