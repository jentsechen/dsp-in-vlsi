import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gen import gen_adder, gen_mul

if __name__ == '__main__':
    vectors_dir = os.path.normpath(
        os.path.join(os.path.dirname(__file__), '..', 'design', '01_RTL', 'vectors')
    )
    gen_adder.preview()
    gen_adder.run(vectors_dir)
    gen_mul.preview()
    gen_mul.run(vectors_dir)