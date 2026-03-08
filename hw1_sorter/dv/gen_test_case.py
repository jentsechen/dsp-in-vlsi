import numpy as np

def gen_test_case(n_block, seed=123):
    n_group, n_element_per_group = 4, 8
    np.random.seed(seed)
    input = np.random.randint(-256, 256, size=(n_block, n_group, n_element_per_group))
    with open("..\\rtl\\sorter\\sorter.sim\\sim_SelectTopK\\behav\\xsim\\input.txt", "w") as file:
        for block_index in range(n_block):
            for group_index in range(n_group):
                if group_index==0:
                    BlkIn = 1
                else:
                    BlkIn = 0
                input_str = f"{BlkIn} "
                for element_index in range(n_element_per_group):
                    input_str += f"{input[block_index][group_index][element_index]} "
                input_str += "\n"
                file.write(input_str)
    for block_index in range(n_block):
        sorted_values = np.sort(input[block_index].flatten())
        print(f"block {block_index}: {sorted_values[-4:][::-1]}")

if __name__ == "__main__":
    gen_test_case(n_block=4)

