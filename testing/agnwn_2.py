from numpy import sqrt
import random
import matplotlib.pyplot as plt

from classes.CDS import CDS
from classes.CryptoSignal import CryptoSignal


from modules import plot
from modules.noise import generate_noise, received_sig, detected_sig, err, print_info
from modules.plot import build_BER_compare


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
# N - numbers of experiment (how many times we will send& receive signal)
# signal - CDS/CS/DER_SIG
def test_seq(signal, N):


    snrindB_range = range(0, 11)
    itr = len(snrindB_range)
    ber = [None] * itr


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

        ber[n] = no_errors / N*len(signal)

        print_info(snrindB,no_errors,ber[n])

    plot.build_BER(snrindB_range, ber)


# Отправляем по 1 бит сигнала (КС или ХДС, или производій)
def test_seq_symbol(signal,N):

    snrindB_range = range(0, 11)
    itr = len(snrindB_range)
    ber = [None] * itr


    sig = signal
    # cds = CDS(N)
    # sig = cds.table[5]

    for n in range(0, itr):
        snrindB = snrindB_range[n]
        # linear snr
        snr = 10.0 ** (snrindB / 10.0)
        noise_std = 1 / sqrt(2 * snr)
        noise_mean = 0
        no_errors = 0

        # Передаем cигнал побитово
        for m in range(0, N):
            # transported symbol of signal
            tx_symbol = sig[m%len(sig)]
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

        print_info(snrindB,no_errors,ber[n])

    print(ber)
    plot.build_BER(snrindB_range,ber)

# SLICE
def test_seq_symbol2(signal):

    snrindB_range = range(0, 10)
    itr = len(snrindB_range)
    ber = [None] * itr
    N = 20000

    sig = signal
    # cds = CDS(N)
    # sig = cds.table[5]

    for n in range(0, itr):
        snrindB = snrindB_range[n]
        # linear snr
        snr = 10.0 ** (snrindB / 10.0)
        noise_std = 1 / sqrt(2 * snr)
        noise_mean = 0
        no_errors = 0

        # Передаем cигнал побитово
        for m in range(0, N):
            # transported 4symbol(frame) of signal
            tx_sig = sig[(4*m)%len(sig):(4*(m+1))%len(sig)]

            noise = generate_noise(noise_mean,noise_std,len(tx_sig))
            # received symbol(applying noise to transported sig)
            rx_sig = received_sig(tx_sig,noise)
            # detecting signal
            # if rx_symbol >=0 then det_symbol = 1
            # else det_symbol = -1
            det_sig = detected_sig(rx_sig)

            # if detected symbols not the same as transmitted then +plus error
            no_errors = err(det_sig,tx_sig)

        ber[n] = no_errors / (N*len(tx_sig))

        print_info(snrindB,no_errors,ber[n])

    print(ber)
    plot.build_BER(snrindB_range,ber)


def compare_plot():
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    b = [0.3328, 0.3584, 0.256, 0.128, 0.0768, 0.0768, 0.0256, 0.0, 0.0, 0.0, 0.0]
    c = [0.2816, 0.2304, 0.1792, 0.1792, 0.0512, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    build_BER_compare(a, b, c)

if __name__=='__main__':
   # test_noise_symbol()


   cs = CryptoSignal(256)
   sig = cs.generateDefRandomSeq(32)
   c = CDS(257)
   sig_2 = c.table[5]
   # test_seq(sig_2,10000)
   test_seq_symbol(sig_2,2560000)