from __future__ import division

import copy
from scipy import signal

from classes.CryptoSignal import CryptoSignal
from modules.arr_procedures import test_auto_correl
from modules.plot import  build_spectrum

import numpy as np
import matplotlib.pyplot as plt
from modules.plot import build_plot

def test_cs_spectrum():
    # Creating CS
    cs = CryptoSignal(256)
    sig = cs.generateDefRandomSeq(32)
    # calculatin pfak and afak
    pfak_list, afak_list = test_auto_correl(sig)
    build_plot(pfak_list)

    # setting sampling rate
    sampling_rate = 30
    # calculate spctrum
    freq, ps = calculate_spectrum_autocorrel(pfak_list, sampling_rate)

    # the same as above function
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.periodogram.html
    freq_1, ps_1 = signal.periodogram(pfak_list,sampling_rate)



    print('Frequency:',freq)
    print('PSD',ps)
    print('Frequency:', freq_1)
    print('PSD', ps_1)
    build_spectrum(freq, ps)

    build_spectrum(freq_1,ps_1)

    # if you need a left part but it make
    # no sense to use it because its mirrored
    # ps1 = np.abs(np.fft.fft(pfak_list))
    # time_step = 1 / sampling_rate
    #
    # freqs = np.fft.fftfreq(len(pfak_list), time_step)
    # idx = np.argsort(freqs)
    #
    # plt.plot(freqs[idx], ps1[idx])
    # plt.show()



# power spectrum = abs(forier_transform(f(t))
def calculate_spectrum(data_list, sampling_rate):

    data = np.asarray(data_list)
    # Using foruier transformation on data (
    fourier_transform = np.fft.rfft(data)
    # Absolute values
    abs_fourier_transform = np.abs(fourier_transform)
    # to calcluate power spectrum you need to square
    # absolute values of data transformed by Fourier transformation
    power_spectrum = np.square(abs_fourier_transform)

    frequency = np.linspace(0, sampling_rate / 2, len(power_spectrum))

    return frequency, power_spectrum

# Also another way to calculate spectrum
# power_spectrum = forier_transform ( auto-correlation function of f(t))
def calculate_spectrum_autocorrel(fak_list, sampling_rate):
    data = np.asarray(fak_list)
    fourier_transform = np.fft.rfft(data)
    power_spectrum = fourier_transform
    frequency = np.linspace(0, sampling_rate / 2, len(power_spectrum))
    return frequency, power_spectrum

# as pure signal we use correaltion function
def add_noise(pure):
    # Converting pure (list) to ndarray
    data = np.asarray(pure)
    # Generating noise (normal distributed values from 0 to 1) depends on data length
    noise = np.random.normal(0,1, len(pure))
    # Adding noise (sum or multipilcation depends on nature of noise)
    #  for our model we use sum
    signal = data + noise

    return signal


if __name__=='__main__':
    test_cs_spectrum()

    # https://www.kite.com/python/answers/how-to-plot-a-power-spectrum-in-python
    # раскладываем в ряд фурье ФАК
    # ps = np.abs(np.fft.fft(pfak_list)) ** 2
    # time_step = 1 / 30
    #
    # freqs = np.fft.fftfreq(len(pfak_list), time_step)
    # idx = np.argsort(freqs)
    #
    # plt.plot(freqs[idx], ps[idx])
    # plt.show()

    # =====================
    # This bellow you only need positive part of spectrum because the
    # negative is the same ===================
    # sampling_rate = 60.0
    # #
    # # time = np.arange(0, 10, 1 / sampling_rate)
    # #
    # # # data = np.sin(2*np.pi*6*time) + np.random.randn(len(time)) // вместо второго значения надо данные пфак
    # # # прогнать по циклу и складывать с синусойдой
    # data = np.asarray(pfak_list)
    #
    #
    # fourier_transform = np.fft.rfft(data)
    #
    # abs_fourier_transform = np.abs(fourier_transform)
    #
    # power_spectrum = np.square(abs_fourier_transform)
    #
    # frequency = np.linspace(0, sampling_rate / 2, len(power_spectrum))
    #
    # plt.plot(frequency, power_spectrum)
    # plt.show()

