import math
import numpy as np
from mapper import mapper
from harddemapper import harddemapper
from softdemapper import softdemapper


N_packet = 1000
N_frame = 10
M = 16
b = int(math.log2(M))
SNRdBs = np.arange(0, 45, 5)
channel = 'rayleigh'
plotconst = 'off'
# Send N_packet with different SNRdB, range +5
for i_SNR, SNRdB in enumerate(SNRdBs):
    sigma = math.sqrt(0.5/(10**(SNRdB/10)))
    hard_errors = np.zeros((N_packet, 1))
    soft_errors = np.zeros((N_packet, 1))
    for i_packet in range(N_packet):
        tx_error_symbols = []
        hard_error_symbols = []
        msg_symbol = np.random.randint(2, size=int(N_frame*b))
        print(msg_symbol)
        tx_bits = msg_symbol
        tx_sym = mapper(tx_bits, b, N_frame)
        X = tx_sym
        if channel == 'rayleigh':
            H = (np.random.normal(size=(N_frame, 1)) + np.random.normal(size=(N_frame, 1)) * 1j) / math.sqrt(2)
        elif channel == 'awgn':
            H = np.array([1, 0]).T*N_frame
        else:
            raise ValueError('This channel is not supported')
        N = (np.random.normal(size=X.shape) + np.random.normal(size=X.shape) * 1j) * sigma
        R = H * X + N
        rx_sym = R / H
        print(rx_sym)
        print(rx_sym[0].real)
        print(rx_sym[0].imag)
        hard_rx_bits = harddemapper(rx_sym)
        print(hard_rx_bits)
        soft_rx_bits = softdemapper(rx_sym)
        # Keep error of each i_packet then we calculate BER
        hard_error = sum(abs(tx_bits - hard_rx_bits))
        if hard_error > 0:
            tx_error_symbols = np.logical_and(tx_error_symbols, rx_sym)
            hard_error_symbols = np.logical_and(hard_error_symbols, rx_sym)
        soft_error = sum(abs(tx_bits - soft_rx_bits))
        #hard_errors[i_packet, 0] = sum(hard_error)
        #soft_errors[i_packet, 0] = sum(soft_error)
        
