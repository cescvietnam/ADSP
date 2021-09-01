import numpy as np


def one_bit_encoding(bit, current=[0, 0], function_matrix = np.ones((2,3))):
	s_list = np.zeros(function_matrix.shape[1]).astype('uint8')
	s_list[0] = bit
	s_list[1:] = current
	temp = np.tile(s_list, (function_matrix.shape[0], 1))
	outs = function_matrix * temp
	out_sums = np.sum(outs, axis=1)
	return np.mod(out_sums, 2).astype('uint8'), list(s_list[:-1])