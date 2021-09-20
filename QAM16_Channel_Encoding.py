import math
import numpy as np
from mapper import mapper
from harddemapper import harddemapper
from softdemapper import softdemapper
import matplotlib.pyplot as plt
import time
from ifft import ifft
from fft import fft
from channel_encoding import channel_encoding
from channel_decoding import viterbi_decoding_soft_input, viterbi_decoding_hard_input


N_packet = 10000
N_frame = 64
M = 16
b = int(math.log2(M))
SNRdBs = np.arange(0, 45, 5)
channel = 'rayleigh'
plotconst = 'on'
N_tx     = 4
N_rx     = 4
hard_BER = np.zeros(len(SNRdBs))
soft_BER = np.zeros(len(SNRdBs))
soft_time = 0
hard_time = 0

function_matrix = np.array([[1,0,1], [1,1,1]])

# Send N_packet with different SNRdB, range +5
for i_SNR, SNRdB in enumerate(SNRdBs):
    print('Finished {:.2f} %'.format(i_SNR / len(SNRdBs) * 100))
    sigma = math.sqrt(0.5/(10**(SNRdB/10)))
    hard_errors = np.zeros(N_packet)
    soft_errors = np.zeros(N_packet)
    tx_error_symbols = []
    hard_error_symbols = []
    for i_packet in range(N_packet):
        X_tx=[]
        all_msg=[]
        for i in range(N_tx):
            msg_symbol = np.random.randint(2, size=N_frame * b // function_matrix.shape[0])
            all_msg.append(msg_symbol)
            tx_bits = channel_encoding(msg_symbol, function_matrix)
            tx_sym = mapper(tx_bits, b, N_frame)
        #(tx_sym)
        #X = ifft(tx_sym)
            X = np.fft.ifft(tx_sym, N_frame)
            X_tx.append(X)
        X_tx = np.stack(X_tx)
        all_msg = np.stack(all_msg)

        #print(tx_sym)
        #X = tx_sym
        if channel == 'rayleigh':
            H = np.array([((np.random.standard_normal(N_tx) + np.random.standard_normal(N_tx) * 1j) / math.sqrt(2)) for i in range(N_tx) ])
        elif channel == 'awgn':
            H = np.matlib.repmat([1,0],N_tx,1) # To be checked
        else:
            raise ValueError('This channel is not supported')
        N = (np.random.standard_normal(N_tx) + np.random.standard_normal(N_tx) * 1j) * sigma
        #H = np.tile(H, N_frame)
        #N = np.tile(N, N_frame)
        #print(X.shape, H.shape, N.shape)
        #print(H)
        #print("X",X_tx)
        W_ZF = H**(-1)
        #print(H)
        #H_H = np.asmatrix(H).getH()
        H_H = np.conjugate(H)
        #print(H_H)
        #print(H)
        #W_MMSE = (H + ((10** (-SNRdB/10)) * np.eye(N_tx))) **(-1) 
        #print(10** (SNRdB/10) )
        W_MMSE = (H_H * H + (10** (-SNRdB/10)) * np.eye(N_tx)) **(-1) * H_H
        #W_MMSE = np.squeeze(np.asarray(W_MMSE))
        #W_MMSE = (H' *H + (10 ^(-SNR_dB/10)) *eye(N_tx)) \H';
        #print(W_MMSE.shape)
        # print(test.shape)
       # print(W_ZF.shape)
        Y = H * X + N
        #Y = R / H
        #print(R.shape, Y.shape)
        #rx_sym = fft(Y)
        rx_sym = np.fft.fft(Y*W_MMSE, N_frame)
        #print(rx_sym.shape)
        Y_tx_hard=[]
        Y_tx_soft=[]
        for i in range(N_rx):
            t1 = time.time()
            hard_rx_bits = harddemapper(rx_sym[0])
            hard_rx_bits = viterbi_decoding_hard_input(hard_rx_bits, function_matrix)
            Y_tx_hard.append(hard_rx_bits)
            t2 = time.time()
            soft_rx_bits = softdemapper(rx_sym[0], real=True)
            soft_rx_bits = viterbi_decoding_soft_input(soft_rx_bits, function_matrix)
            Y_tx_soft.append(soft_rx_bits)
            t3 = time.time()
            soft_time = soft_time + t3 - t2
            hard_time = hard_time + t2 - t1
        # Keep error of each i_packet then we calculate BER
        Y_tx_hard = np.stack(Y_tx_hard)
        Y_tx_soft = np.stack(Y_tx_soft)
        #print(Y_tx_hard,"matrix",Y_tx_soft,all_msg)
        hard_error = sum(abs(all_msg - Y_tx_hard))
        #print(hard_error)
        if hard_error > 0:
            tx_error_symbols.extend(tx_sym)
            hard_error_symbols.extend(rx_sym)
        soft_error = sum(abs(all_msg - Y_tx_soft))
        hard_errors[i_packet] = hard_error
        soft_errors[i_packet] = soft_error
    has_error = len(tx_error_symbols)
    tx_iphases = np.zeros(has_error)
    tx_qphases = np.zeros(has_error)
    rx_iphases = np.zeros(has_error)
    rx_qphases = np.zeros(has_error)
    if has_error >= 1:
        if plotconst == 'on':
            for idx in range(has_error):
                tx_error_sym = tx_error_symbols[idx]
                rx_error_sym = hard_error_symbols[idx]
                tx_iphase = tx_error_sym.real
                tx_qphase = tx_error_sym.imag
                rx_iphase = rx_error_sym.real
                rx_qphase = rx_error_sym.imag
                tx_iphases[idx] = tx_iphase
                tx_qphases[idx] = tx_qphase
                rx_iphases[idx] = rx_iphase
                rx_qphases[idx] = rx_qphase
            plt.scatter(tx_iphases, tx_qphases, c='r')
            plt.scatter(rx_iphases, rx_qphases, c='b')
            plt.xlim([-10, 10])
            plt.ylim([-10, 10])
            plt.grid('on')
            plt.savefig('images/QAM16_OFDM_Channel_encode/new/error_' + str(i_SNR) + '.png')
            plt.close()
    hard_BER[i_SNR] = sum(hard_errors) / (N_packet * N_frame * b)
    soft_BER[i_SNR] = sum(soft_errors) / (N_packet * N_frame * b)
print("Processing speed of hard demapper (us/bit): ", hard_time / (N_packet * N_frame * b)*1000000)
print("Processing speed of soft demapper (us/bit): ", soft_time / (N_packet * N_frame * b)*1000000)
plt.plot(SNRdBs, hard_BER, c='b', label='hard demapper')
plt.plot(SNRdBs, soft_BER, c='r', label='soft demapper')
plt.xlabel('SNRdB')
plt.ylabel('BER (log scale)')
plt.yscale('log')
plt.grid('on')
plt.ylim([10**-5, 1])
plt.xlim([0, 45])
plt.title('BER vs SNRdB in Rayleigh channel - QAM16_OFDM_Channel_encode')
plt.legend()
plt.savefig('images/QAM16_OFDM_Channel_encode/new/BER.png')
plt.close()