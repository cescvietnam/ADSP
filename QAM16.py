import math
import numpy as np

N_packet = 1000
N_frame = 10
M = 16
b = math.log2(M)

SNRdBs = np.arange(0, 45, 5)
channel = 'rayleigh'
plotconst = 'off'
# Send N_packet with different SNRdB, range +5
for i_SNR, SNRdB in enumerate(SNRdBs):
    sigma = math.sqrt(0.5/(10**(SNRdB/10)))
    for i_packet in range(N_packet):
        tx_error_symbols = []
        hard_error_symbols = []
        msg_symbol = np.random.randint(2, size=int(N_frame*b))
        tx_bits = msg_symbol
        tx_sym = mapper(tx_bits.T, b, N_frame)
        tx_sym = tx_sym.T
        X = tx_sym
        if channel == 'rayleigh':
            H = (np.random.normal(size=(N_frame, 1)) + np.random.normal(size=(N_frame, 1)) * 1j) / math.sqrt(2)
        elif channel == 'awgn':
            H = np.array([1, 0]).T*N_frame
        else:
            raise ValueError('This channel is not supported')
        N = (np.random.normal(size=(X, 1)) + np.random.normal(size=(X, 1)) * 1j) * sigma
        R = H * X + N
        rx_sym = R / H
