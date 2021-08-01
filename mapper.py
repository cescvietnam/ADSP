# mapper function definition
import numpy as np


def mapper(tx_bits, b, N_frame):
    result = np.zeros(N_frame) * 1j
    mapper_dict = {(0, 0, 0, 0): -3 - 3 * 1j,
                   (0, 0, 0, 1): -3 - 1 * 1j,
                   (0, 0, 1, 0): -3 + 3 * 1j,
                   (0, 0, 1, 1): -3 + 1 * 1j,
                   (0, 1, 0, 0): -1 - 3 * 1j,
                   (0, 1, 0, 1): -1 - 1 * 1j,
                   (0, 1, 1, 0): -1 + 3 * 1j,
                   (0, 1, 1, 1): -1 + 1 * 1j,
                   (1, 0, 0, 0): +3 - 3 * 1j,
                   (1, 0, 0, 1): +3 - 1 * 1j,
                   (1, 0, 1, 0): +3 + 3 * 1j,
                   (1, 0, 1, 1): +3 + 1 * 1j,
                   (1, 1, 0, 0): +1 - 3 * 1j,
                   (1, 1, 0, 1): +1 - 1 * 1j,
                   (1, 1, 1, 0): +1 + 3 * 1j,
                   (1, 1, 1, 1): +1 + 1 * 1j}
    for i in range(0, N_frame*b, b):
        chunk = tuple(tx_bits[i:i + b])
        result[int(i/b)] = mapper_dict[chunk]
    return result
