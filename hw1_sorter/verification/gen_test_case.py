import os
import numpy as np

VECTORS_DIR = os.path.join(os.path.dirname(__file__), "../design/01_RTL/vectors")


def gen_test_case(n_block, seed=123):
    n_group, n_element_per_group = 4, 8
    np.random.seed(seed)
    data = np.random.randint(-256, 256, size=(n_block, n_group, n_element_per_group))

    os.makedirs(VECTORS_DIR, exist_ok=True)

    with open(os.path.join(VECTORS_DIR, "tb_Sort8_input.txt"), "w") as fin, open(
        os.path.join(VECTORS_DIR, "tb_Sort8_golden.txt"), "w"
    ) as fgold:
        for block_index in range(n_block):
            vals = data[block_index][0]
            fin.write(" ".join(map(str, vals)) + "\n")
            sorted_vals = np.sort(vals)[::-1]
            fgold.write(" ".join(map(str, sorted_vals)) + "\n")

    with open(os.path.join(VECTORS_DIR, "tb_SelectTopK_input.txt"), "w") as fin, open(
        os.path.join(VECTORS_DIR, "tb_SelectTopK_golden.txt"), "w"
    ) as fgold:
        for block_index in range(n_block):
            for group_index in range(n_group):
                blk_in = 1 if group_index == 0 else 0
                vals = data[block_index][group_index]
                fin.write(f"{blk_in} " + " ".join(map(str, vals)) + "\n")
            top4 = np.sort(data[block_index].flatten())[-4:][::-1]
            fgold.write(" ".join(map(str, top4)) + "\n")


if __name__ == "__main__":
    gen_test_case(n_block=4)