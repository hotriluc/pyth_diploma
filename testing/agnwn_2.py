from numpy import sqrt
import random
import matplotlib.pyplot as plt




def test_noise_symbol():
    N = 20000
    snrindB_range = range(0, 10)
    itr = len(snrindB_range)
    ber = [None] * itr

    for n in range(0, itr):

        snrindB = snrindB_range[n]
        snr = 10.0 ** (snrindB / 10.0)
        noise_std = 1 / sqrt(2 * snr)
        noise_mean = 0

        no_errors = 0
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
    plt.plot(snrindB_range, ber, 'o-', label='practical')
    plt.axis([0, 10, 0, 0.1])
    plt.xlabel('snr(dB)')
    plt.ylabel('BER')
    plt.grid(True)
    plt.title('BPSK Modulation')
    plt.legend()
    plt.show()

if __name__=='__main__':
   # test_noise_symbol()
   N = 20000
   snrindB_range = range(0, 10)
   itr = len(snrindB_range)
   ber = [None] * itr
   for n in range(0, itr):

       snrindB = snrindB_range[n]
       snr = 10.0 ** (snrindB / 10.0)
       noise_std = 1 / sqrt(2 * snr)
       noise_mean = 0

       no_errors = 0
       for m in range(0, N):
           # 1) cформироваь КС

           # 2) generating noise
           noise = random.gauss(noise_mean, noise_std)
           # received symbol(applying noise to transported sig)

           # 3) add noise to CS

           # 4) detecting signal
           # if rx_symbol >=0 then det_symbol = 1
           # else det_symbol = -1

           # det_symbol = 2 * (rx_symbol >= 0) - 1
           #  5) CHECKING IF DIFFERENT THEN ADD TO COUNTER
           # if detected symbols not the same as transmitted then +plus error
           # no_errors += 1 * (cs[i] != det[i])

       #     !!!!!
       #     ЗАВТРА СДЕЛАТЬ ДЛЯ СИГНАЛОВ КС, т.е вместо 1го символа
       #     сравнить все символы последовательности которую отправили
       #  и которую получили

       ber[n] = no_errors / N
       print("SNR in dB:", snrindB)
       print("Numbder of errors:", no_errors)
       print("Error probability:", ber[n])