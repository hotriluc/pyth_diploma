from __future__ import division

import copy
from scipy import signal

from classes.CDS import CDS
from classes.CryptoSignal import CryptoSignal
from classes.Hadamar import Hadamar
from modules.arr_procedures import test_auto_correl, derivativeSigFromTo, print_derivative
from modules.plot import build_spectrum, build_spectrum_plotly
from modules.arr_procedures import getDecimation

import numpy as np
from modules.plot import build_plot

def print_freq_and_ps(frequencies, power_spectrum):
    print('Frequency:', frequencies)
    print('PSD:', power_spectrum)

    for i in range(0,len(frequencies)):
        print('Frequency = {0} Hz, PSD = {1}'.format(frequencies[i],power_spectrum[i]))


def test_cs_spectrum():
    # Creating CS
    cs = CryptoSignal(256)
    sig = cs.generateDefRandomSeq(32)
    # calculatin pfak and afak
    pfak_list, afak_list = test_auto_correl(sig)
    build_plot(pfak_list, 'ПФАК')
    build_plot(afak_list, 'АФАК')

    # setting sampling rate
    sampling_rate = 30
    # calculate spctrum using pfak list
    freq_pfak, ps_pfak = calculate_spectrum_autocorrel(pfak_list, sampling_rate)

    # calculate spectrum using afak list
    freq_afak, ps_afak = calculate_spectrum_autocorrel(afak_list, sampling_rate)

    # the same as above function
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.periodogram.html
    # freq_1, ps_1 = signal.periodogram(pfak_list, sampling_rate)

    # printing and build plot
    print('=====PFAK SPECTRUM======')
    print_freq_and_ps(freq_pfak, ps_pfak)
    build_spectrum(freq_pfak, ps_pfak)

    print('=====AFAK SPECTRUM======')
    print_freq_and_ps(freq_afak, ps_afak)
    build_spectrum(freq_afak, ps_afak)


    # print('Frequency:', freq_1)
    # print('PSD', ps_1)
    # build_spectrum(freq_1,ps_1)

    # if you need a left part but it make
    # no sense to use it because its mirrored
    freq_pfak_1, ps_pfak_1, idx_pfak_1 = calculate_spectrum_autocorrel_fft(pfak_list, sampling_rate)
    build_spectrum(freq_pfak_1[idx_pfak_1], ps_pfak_1[idx_pfak_1])

    freq_afak_1, ps_afak_1, idx_afak_1 = calculate_spectrum_autocorrel_fft(afak_list, sampling_rate)
    build_spectrum(freq_afak_1[idx_afak_1], ps_afak_1[idx_afak_1])

    # PLOTLY PLOT all above are regular plots with matplotlib
    # build_spectrum_plotly(frequency=freq, power_spectrum=ps,
    #                       graph_name='../plotly_plots/CS_{0}_Spectrum'.format(len(sig)))



def test_cds_spectrum():
    cds = CDS(1021)
    cds.print_general_info()
    cds.print_table()
    source_sig = cds.table[5]


    pfak_list, afak_list = test_auto_correl(source_sig)
    decimations = getDecimation(source_sig)

    # setting sampling rate
    sampling_rate = 30
    # calculate spctrum
    freq, ps = calculate_spectrum_autocorrel(pfak_list, sampling_rate)
    print('Frequency:', freq)
    print('PSD', ps)
    build_spectrum(freq, ps)

    # if you need a left part but it make
    # no sense to use it because its mirrored
    freq_1, ps_1, idx_1 = calculate_spectrum_autocorrel_fft(pfak_list, sampling_rate)
    build_spectrum(freq_1[idx_1], ps_1[idx_1])

    # PLOTLY PLOT all above are regular plots with matplotlib
    # build_spectrum_plotly(frequency=freq, power_spectrum=ps,
    #                       graph_name='../plotly_plots/CDS_{0}_Spectrum'.format(len(source_sig)))


    # freq_1, ps_1 = signal.periodogram(pfak_list, sampling_rate)
    # print('Frequency:', freq_1)
    # print('PSD', ps_1)
    # build_spectrum(freq_1, ps_1)


def test_derivative_cs_spectrum():
    p = 256
    h = Hadamar(p)
    cs = CryptoSignal(p)

    source_sig = cs.generateDefRandomSeq(32)
    hadamar_sig_list = h.getHadamMatrix()

    # setting sampling rate
    sampling_rate = 30

    # derivative
    dersig, combinations = derivativeSigFromTo([source_sig], hadamar_sig_list, 1, 5)
    print_derivative(dersig, combinations)
    # i=0
    for sig in dersig:
        pfak_list, afak_list = test_auto_correl(sig)
        freq, ps = calculate_spectrum_autocorrel(pfak_list, sampling_rate)
        print('Frequency:', freq)
        print('PSD', ps)
        build_spectrum(freq, ps)

        # build_spectrum_plotly(frequency=freq, power_spectrum=ps,
        #                       graph_name='../plotly_plots/DERIVATIVE#{0}_{1}_Spectrum'.format(i,len(sig)))
        # i+=1

    # for i in range(0, len(dersig)):
    #     print("CS#{0} and HADAMAR#{1}".format(combinations[i][0], combinations[i][1]))
    #     print(dersig[i])
    #
    #     pfak_list, afak_list = test_auto_correl(dersig[i])
    #
    #     # calculate spctrum
    #     freq, ps = calculate_spectrum_autocorrel(pfak_list, sampling_rate)
    #     print('Frequency:', freq)
    #     print('PSD', ps)
    #     build_spectrum(freq, ps)

def test_derivative_cds_spectrum():
    cds = CDS(257)
    cds.print_general_info()
    cds.print_table()
    source_sig = cds.table[5]
    h = Hadamar(256)
    hadamar_sig_list = h.getHadamMatrix()

    dersig, combinations = derivativeSigFromTo([source_sig], hadamar_sig_list, 1, 5)
    # setting sampling rate
    sampling_rate = 30


    for i in range(0, len(dersig)):

        print("CDS#{0} and HADAMAR#{1}".format(combinations[i][0], combinations[i][1]))
        print(dersig[i])
        print(dersig[i] == source_sig)

        pfak_list, afak_list = test_auto_correl(dersig[i])

        # calculate spctrum
        freq, ps = calculate_spectrum_autocorrel(pfak_list, sampling_rate)
        print('Frequency:', freq)
        print('PSD', ps)
        build_spectrum(freq, ps)


# ============SPECTRUM CALCULATION============================================

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

def calculate_spectrum_autocorrel_fft(fak_list, sampling_rate):
    power_spectrum = np.fft.fft(fak_list)
    time_step = 1/sampling_rate
    freqs = np.fft.fftfreq(len(fak_list), time_step)
    idx = np.argsort(freqs)


    return  freqs,power_spectrum,idx

# ========================================================

# ============NOISE============================================
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
# ========================================================

if __name__=='__main__':
    test_cs_spectrum()

    # test_cds_spectrum()

    # test_derivative_cs_spectrum()

    # test_derivative_cds_spectrum()



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

