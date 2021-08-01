import numpy as np


def harddemapper(rx_sym):
    result = []
    for sym in rx_sym:
        if (sym.real < -2) and (sym.imag < -2):
            result.extend([0, 0, 0, 0])
            continue
        if (sym.real < -2) and (sym.imag < 0):
            result.extend([0, 0, 0, 1])
            continue
        if (sym.real < -2) and (sym.imag < 2):
            result.extend([0, 0, 1, 1])
            continue
        if (sym.real < -2) and (sym.imag > 2):
            result.extend([0, 0, 1, 0])
            continue
        if (sym.real < 0) and (sym.imag < -2):
            result.extend([0, 1, 0, 0])
            continue
        if (sym.real < 0) and (sym.imag < 0):
            result.extend([0, 1, 0, 1])
            continue
        if (sym.real < 0) and (sym.imag < 2):
            result.extend([0, 1, 1, 1])
            continue
        if (sym.real < 0) and (sym.imag > 2):
            result.extend([0, 1, 1, 0])
            continue
        if (sym.real < 2) and (sym.imag < -2):
            result.extend([1, 1, 0, 0])
            continue
        if (sym.real < 2) and (sym.imag < 0):
            result.extend([1, 1, 0, 1])
            continue
        if (sym.real < 2) and (sym.imag < 2):
            result.extend([1, 1, 1, 1])
            continue
        if (sym.real < 2) and (sym.imag > 2):
            result.extend([1, 1, 1, 0])
            continue
        if (sym.real > 2) and (sym.imag < -2):
            result.extend([1, 0, 0, 0])
            continue
        if (sym.real > 2) and (sym.imag < 0):
            result.extend([1, 0, 0, 1])
            continue
        if (sym.real > 2) and (sym.imag < 2):
            result.extend([1, 0, 1, 1])
            continue
        if (sym.real > 2) and (sym.imag > 2):
            result.extend([1, 0, 1, 0])
            continue
    return np.array(result).astype('uint8')


def harddemapper1(rx_sym):
    result = []
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
    for sym in rx_sym:
        min_squared_distance = 2
        temp_bits = []
        for bits in mapper_dict:
            squared_distance = (sym.real-mapper_dict[bits].real)**2 + (sym.imag-mapper_dict[bits].imag)**2
            if squared_distance < 1:
                temp_bits = list(bits)
                break
            else:
                if squared_distance < min_squared_distance:
                    min_squared_distance = squared_distance
                    temp_bits = list(bits)
        result.extend(temp_bits)
    return np.array(result).astype('uint8')
