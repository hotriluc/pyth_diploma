from __future__ import division
from classes.CryptoSignal import CryptoSignal
from modules.arr_procedures import test_auto_correl

import numpy as np
import matplotlib.pyplot as plt
from modules.plot import build_plot

def test():
    cs = CryptoSignal(20)
    sig = cs.generateRandomSeq()
    pfak_list, afak_list = test_auto_correl(sig)


if __name__=='__main__':
    cs = CryptoSignal(256)
    sig = cs.generateDefRandomSeq(32)
    pfak_list, afak_list = test_auto_correl(sig)
    build_plot(pfak_list)
    # https://www.kite.com/python/answers/how-to-plot-a-power-spectrum-in-python
    # раскладываем в ряд фурье ФАК
    ps = np.abs(np.fft.fft(pfak_list)) ** 2
    time_step = 1 / 30

    freqs = np.fft.fftfreq(len(pfak_list), time_step)
    idx = np.argsort(freqs)

    plt.plot(freqs[idx], ps[idx])
    plt.show()

    # This bellow you only need positive part of spectrum because the negative is the same
    # sampling_rate = 30.0
    #
    # time = np.arange(0, 10, 1 / sampling_rate)
    #
    # data = np.sin(2*np.pi*6*time) + np.random.randn(len(time)) // вместо второго значения надо данные пфак
    # прогнать по циклу и складывать с синусойдой
    # data = pfak_list
    #
    # fourier_transform = np.fft.rfft(pfak_list)
    #
    # abs_fourier_transform = np.abs(fourier_transform)
    #
    # power_spectrum = np.square(abs_fourier_transform)
    #
    # frequency = np.linspace(0, sampling_rate / 2, len(power_spectrum))
    #
    # plt.plot(frequency, power_spectrum)
    # plt.show()



    # f = 10  # Frequency, in cycles per second, or Hertz
    # f_s = 100  # Sampling rate, or number of measurements per second
    #
    # t = np.linspace(0, 2, 2 * f_s, endpoint=False)
    # x = np.sin(f * 2 * np.pi * t)
    #
    # fig, ax = plt.subplots()
    # ax.plot(t, x)
    # ax.set_xlabel('Time [s]')
    # ax.set_ylabel('Signal amplitude');
    # plt.show()