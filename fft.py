import numpy as np
from math import e, pi


def fft(rx_sym, N_frame=64):
	#rx_sym = rx_sym.reshape(-1)
	result = np.zeros(len(rx_sym)) *1j
	for i in range(0, len(rx_sym), N_frame):
		chunk = rx_sym[i:i+N_frame]
		result[i:i+N_frame] = np.fft.fft(chunk, N_frame)
	return result