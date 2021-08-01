import numpy as np


def softdemapper(rx_sym):
    result = []
    for sym in rx_sym:
        if sym.real < -2:
            sb_b0 = 2 * (sym.real + 1)
        elif sym.real < 2:
            sb_b0 = sym.real
        else:
            sb_b0 = 2 * (sym.real - 1)
        sb_b1 = -abs(sym.real) + 2
        if sym.imag < -2:
            sb_b2 = 2 * (sym.imag + 1)
        elif sym.imag < 2:
            sb_b2 = sym.imag
        else:
            sb_b2 = 2 * (sym.imag - 1)
        sb_b3 = -abs(sym.imag) + 2
        result.extend([sb_b0, sb_b1, sb_b2, sb_b3])
    return ((np.sign(np.array(result)) + 1) / 2).astype('uint8')
