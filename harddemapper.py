import numpy as np
import math

def harddemapper(rx_sym):
    mapper_dict = {0:(0, 0, 0, 0),
                   1:(0, 0, 0, 1),
                   2:(0, 0, 1, 0),
                   3:(0, 0, 1, 1),
                   4:(0, 1, 0, 0),
                   5:(0, 1, 0, 1),
                   6:(0, 1, 1, 0),
                   7:(0, 1, 1, 1),
                   8:(1, 0, 0, 0),
                   9:(1, 0, 0, 1),
                   10:(1, 0, 1, 0),
                   11:(1, 0, 1, 1),
                   12:(1, 1, 0, 0),
                   13:(1, 1, 0, 1),
                   14:(1, 1, 1, 0),
                   15:(1, 1, 1, 1)}
    mapper_dict1 = [ -3 - 3 * 1j,
                   -3 - 1 * 1j,
                   -3 + 3 * 1j,
                   -3 + 1 * 1j,
                   -1 - 3 * 1j,
                   -1 - 1 * 1j,
                   -1 + 3 * 1j,
                   -1 + 1 * 1j,
                   +3 - 3 * 1j,
                   +3 - 1 * 1j,
                   +3 + 3 * 1j,
                   +3 + 1 * 1j,
                   +1 - 3 * 1j,
                   +1 - 1 * 1j,
                   +1 + 3 * 1j,
                   +1 + 1 * 1j]
    result=[]
    side = lambda x, y: round(math.sqrt(x ** 2 + y ** 2), 2) # tính do dai
    for  i in rx_sym:
        i_real=i.real
        i_image=i.imag
        temp=list(map(lambda x: side(x.real - i_real,x.imag - i_image),mapper_dict1))
        result.append(mapper_dict[temp.index(min(temp))])
    return result
