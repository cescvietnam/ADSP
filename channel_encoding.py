import numpy as np
from one_bit_encoding import one_bit_encoding

def channel_encoding(frame, function_matrix = np.ones((2,3))):
	N = function_matrix.shape[1] - 1
	current = [0] * N
	result = []
	for i, bit in enumerate(frame):
		output, current = one_bit_encoding(bit, current, function_matrix)
		result.extend(list(output))
	return np.array(result)





