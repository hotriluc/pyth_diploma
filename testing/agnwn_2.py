from numpy import sqrt
import random
import matplotlib.pyplot as plt
import numpy as np

from classes.CDS import CDS
from classes.CryptoSignal import CryptoSignal

# Generating list of normal distributed values (gaussian distributed)
from modules import plot


def generate_noise(mean,std,n):
    noise =[]
    for i in range(n):
        noise.append(random.gauss(mean, std))
    return noise

# applying noise to signal
# signal and noise must be the same length
def received_sig (sig,noise):
    rx_sig = []
    for i in range(0,len(sig)):
        rx_sig.append(sig[i]+noise[i])
    return rx_sig

# detecting signal
def detected_sig(received_sig):
    det_sig = []
    for i in range(0,len(received_sig)):
        det_sig.append(2 * (received_sig[i] >= 0) - 1)
    return det_sig

def err(detected_sig,transmited_sig):
    cnt = 0
    for i in range(0,len(transmited_sig)):
        cnt += 1 * (transmited_sig[i] != detected_sig[i])

    return cnt


def test_noise_symbol():
    N = 20000
    snrindB_range = range(0, 10)
    itr = len(snrindB_range)
    ber = [None] * itr


    for n in range(0, itr):
        snrindB = snrindB_range[n]
        # linear snr
        snr = 10.0 ** (snrindB / 10.0)
        noise_std = 1 / sqrt(2 * snr)
        noise_mean = 0
        no_errors = 0

        # Передаем N символов
        for m in range(0, N):
            # transported symbol
            tx_symbol = 2 * random.randint(0, 1) - 1
            # generating noise
            noise = random.gauss(noise_mean, noise_std)
            # received symbol(applying noise to transported sig)
            rx_symbol = tx_symbol + noise
            # detecting signal
            # if rx_symbol >=0 then det_symbol = 1
            # else det_symbol = -1
            det_symbol = 2 * (rx_symbol >= 0) - 1

            # if detected symbols not the same as transmitted then +plus error
            no_errors += 1 * (tx_symbol != det_symbol)

        #     !!!!!
        #     ЗАВТРА СДЕЛАТЬ ДЛЯ СИГНАЛОВ КС, т.е вместо 1го символа
        #     сравнить все символы последовательности которую отправили
        #  и которую получили

        ber[n] = no_errors / N
        print("SNR in dB:", snrindB)
        print("Numbder of errors:", no_errors)
        print("Error probability:", ber[n])
    plt.semilogy()
    plt.plot(snrindB_range, ber, 'o-', label='practical')
    # plt.axis([0, 10, 0, 0.1])
    plt.xlabel('snr(dB)')
    plt.ylabel('BER')
    plt.grid(True)
    plt.title('BPSK Modulation')
    plt.legend()
    plt.show()

# Отправляем по N раз сигналы размером bit_length
# ЗАВТРА ИЗМЕНИТЬ ФУНЕЦИЮ ДОБАВИТЬ ПАРАМЕТР СИГНАЛ, ЧТОБЫ МОЖНО БЫЛО ИСПОЛЬЗОВАТЬ И ДЛЯ ДРУГИХ СИГНАЛОВ
def test_seq():
    N = 10000
    bit_length = 256
    snrindB_range = range(0, 10)
    itr = len(snrindB_range)
    ber = [None] * itr
    cs = CryptoSignal(bit_length)
    signal = cs.generateRandomSeq()

    for n in range(0, itr):
        snrindB = snrindB_range[n]
        snr = 10.0 ** (snrindB / 10.0)
        noise_std = 1 / sqrt(2 * snr)

        noise_mean = 0
        no_errors = 0

        # ВЫПОЛНЯЕМ N испітаний по отправке сигнала размером bit_length
        for m in range(0, N):

            noise = generate_noise(noise_mean, noise_std, len(signal))
            rx_sig = received_sig(signal, noise)
            det_sig = detected_sig(rx_sig)
            no_errors = err(det_sig, signal)

        ber[n] = no_errors / N*bit_length
        print("SNR in dB:", snrindB)
        print("Numbder of errors:", no_errors)
        print("Error probability:", ber[n])
    plt.semilogy(snrindB_range, ber, 'o-', label='practical')


    plt.xlabel('snr(dB)')
    plt.ylabel('BER')
    plt.grid(True)
    plt.title('BPSK Modulation')
    plt.legend()
    plt.show()

# Отправляем по 1 бит сигнала (КС или ХДС, или производій)
def test_seq_symbol():
    N = 2048
    snrindB_range = range(0, 10)
    itr = len(snrindB_range)
    ber = [None] * itr

    cs = CryptoSignal(N)
    sig = cs.generateRandomSeq()

    # cds = CDS(N)
    # sig = cds.table[5]

    for n in range(0, itr):
        snrindB = snrindB_range[n]
        # linear snr
        snr = 10.0 ** (snrindB / 10.0)
        noise_std = 1 / sqrt(2 * snr)
        noise_mean = 0
        no_errors = 0

        # Передаем N символов (для хдс Н-1)
        for m in range(0, N):
            # transported symbol of signal
            tx_symbol = sig[m]
            # generating noise
            noise = random.gauss(noise_mean, noise_std)
            # received symbol(applying noise to transported sig)
            rx_symbol = tx_symbol + noise
            # detecting signal
            # if rx_symbol >=0 then det_symbol = 1
            # else det_symbol = -1
            det_symbol = 2 * (rx_symbol >= 0) - 1

            # if detected symbols not the same as transmitted then +plus error
            no_errors += 1 * (tx_symbol != det_symbol)

        ber[n] = no_errors / N
        print("SNR in dB:", snrindB)
        print("Numbder of errors:", no_errors)
        print("Error probability:", ber[n])
    plt.semilogy()
    plt.plot(snrindB_range, ber, 'o-', label='practical')
    # plt.axis([0, 10, 0, 0.1])
    plt.xlabel('snr(dB)')
    plt.ylabel('BER')
    plt.grid(True)
    plt.title('BPSK Modulation')
    plt.legend()
    plt.show()

if __name__=='__main__':
   # test_noise_symbol()
    test_seq()
   # test_seq_symbol()