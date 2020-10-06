from __future__ import division

import copy
from scipy import signal

from classes.CDS import CDS
from classes.CryptoSignal import CryptoSignal
from classes.Hadamar import Hadamar
from modules.arr_procedures import test_auto_correl, derivativeSigFromTo, print_derivative, writeListInFile, \
    get_decimated_signals
from modules.plot import build_spectrum, build_spectrum_plotly
from modules.arr_procedures import getDecimation
import numpy as np
from modules.plot import build_plot

def print_freq_and_ps(frequencies, power_spectrum):
    print('Frequency:', frequencies)
    print('PSD:', power_spectrum)

    print(
        '\nСнизу приведены значения из полученных массивов –'
        ' пара ( частота, значения спектральной плотности соответствующая данной частоте)')

    for i in range(0,len(frequencies)):
        print('Frequency = {0} Hz, PSD = {1}'.format(frequencies[i],power_spectrum[i]))

def print_spectrum_info_w_plot(mode):

    def pfak_spectrum (freq_pfak, ps_pfak,sigName=''):
        # printing and build plot
        print(
            '\nРассчитаем спектр используя ПФАК. Для того, чтобы его рассчитать используем преобразование Фурье. Получили следующие результаты (2 массива – в одном хранятся частоты, а в другом значения спектральной плотности):')
        print('=====PFAK SPECTRUM======')
        print_freq_and_ps(freq_pfak, ps_pfak)
        build_spectrum(freq_pfak, ps_pfak, 'PFAK PSD of ' + sigName)

    def afak_spectrum(freq_pfak,ps_pfak,sigName=''):
        print(
            '\nРассчитаем спектр используя АФАК. Для того, чтобы его рассчитать используем преобразование Фурье. Получили следующие результаты (2 массива – в одном хранятся частоты, а в другом значения спектральной плотности):')
        print('=====AFAK SPECTRUM======')
        print_freq_and_ps(freq_pfak, ps_pfak)
        build_spectrum(freq_pfak, ps_pfak, 'AFAK PSD of ' + sigName)

    if (mode=='PFAK'):
        return pfak_spectrum
    else:
        return afak_spectrum

def test_cs_spectrum():
    fak_spectrum_info = print_spectrum_info_w_plot('PFAK')
    afak_spectrum_info = print_spectrum_info_w_plot('AFAK')
    # Creating CS
    cs = CryptoSignal(1024)
    sig = cs.generateDefRandomSeq(81)
    # calculatin pfak and afak
    pfak_list, afak_list = test_auto_correl(sig)
    build_plot(pfak_list, 'PFAK CS'+str(len(sig)))
    build_plot(afak_list, 'AFAK CS'+str(len(sig)))

    # setting sampling rate
    sampling_rate = 30
    # [1:len(pfak_list)-1) excluding pfak
    # calculate spctrum using pfak list

    freq_pfak, ps_pfak = calculate_spectrum_autocorrel(pfak_list[1:len(pfak_list)-1], sampling_rate)

    # calculate spectrum using afak list
    freq_afak, ps_afak = calculate_spectrum_autocorrel(afak_list[1:len(afak_list)], sampling_rate)

    # including main peaks
    # # calculate spctrum using pfak list
    # freq_pfak1, ps_pfak1 = calculate_spectrum_autocorrel(pfak_list, sampling_rate)
    #
    # # calculate spectrum using afak list
    # freq_afak1, ps_afak1 = calculate_spectrum_autocorrel(afak_list, sampling_rate)

    # the same as above function
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.periodogram.html
    # freq_1, ps_1 = signal.periodogram(pfak_list, sampling_rate)

    # printing and build plot
    print('\nПФАК без учета основных пиков:',pfak_list[1:len(pfak_list)-1])
    fak_spectrum_info(freq_pfak, ps_pfak, 'CS'+str(len(sig)) )

    print('\nАФАК без учета основных пиков:',afak_list[1:len(afak_list) - 1])
    afak_spectrum_info(freq_afak, ps_afak,'CS'+str(len(sig)) )


    # including main peaks
    # # printing and build plot
    # fak_spectrum_info(freq_pfak1, ps_pfak1, 'CS(fft)' + str(len(sig)))
    # afak_spectrum_info(freq_afak1, ps_afak1, 'CS(fft)' + str(len(sig)))


    # print('Frequency:', freq_1)
    # print('PSD', ps_1)
    # build_spectrum(freq_1,ps_1)

    # if you need a left part but it make
    # no sense to use it because its mirrored
    freq_pfak_1, ps_pfak_1, idx_pfak_1 = calculate_spectrum_autocorrel_fft(pfak_list[1:len(pfak_list)-1], sampling_rate)
    build_spectrum(freq_pfak_1[idx_pfak_1], ps_pfak_1[idx_pfak_1], 'PFAK PSD OF CS'+str(len(sig)))
    #
    freq_afak_1, ps_afak_1, idx_afak_1 = calculate_spectrum_autocorrel_fft(afak_list[1:len(pfak_list)-1], sampling_rate)
    build_spectrum(freq_afak_1[idx_afak_1], ps_afak_1[idx_afak_1],'AFAK PSD OF CS'+str(len(sig)))

    # PLOTLY PLOT all above are regular plots with matplotlib
    # build_spectrum_plotly(frequency=freq, power_spectrum=ps,
    #                       graph_name='../plotly_plots/CS_{0}_Spectrum'.format(len(sig)))



def test_cds_spectrum():
    cds = CDS(257)
    cds.print_general_info()
    # cds.print_table()
    source_sig = cds.table[5]

    print('Source CDS'+str(len(source_sig)))
    pfak_list, afak_list = test_auto_correl(source_sig)
    build_plot(pfak_list, 'ПФАК ' + 'Source CDS{0}'.format(len(source_sig)))
    build_plot(afak_list, 'АФАК ' + 'Source CDS{0}'.format(len(source_sig)))

    decimations = getDecimation(source_sig)
    writeListInFile(decimations,
                    'D:/DIPLOM/спектры_маг_досл/обновл_спектрХДС/ХДС{0}_децимация.txt'.format(len(source_sig)))

    # setting sampling rate
    sampling_rate = 30

    pfak_spectrum_info = print_spectrum_info_w_plot('PFAK')
    afak_spectrum_info = print_spectrum_info_w_plot('AFAK')

    # SOURCE CDS
    # calculate spctrum using pfak list
    freq_pfak, ps_pfak = calculate_spectrum_autocorrel(pfak_list[1:len(pfak_list) - 1], sampling_rate)
    # calculate spectrum using afak list
    freq_afak, ps_afak = calculate_spectrum_autocorrel(afak_list[1:len(afak_list) - 1], sampling_rate)

    print('\nПФАК без учета основных пиков:', pfak_list[1:len(pfak_list) - 1])
    pfak_spectrum_info(freq_pfak,ps_pfak,'Source CDS'+str(len(source_sig)))
    print('\nАФАК без учета основных пиков:', afak_list[1:len(afak_list) - 1])
    afak_spectrum_info(freq_afak,ps_afak,'Source CDS'+str(len(source_sig)))

    # if you need a left part but it make
    # no sense to use it because its mirrored
    freq_pfak_1, ps_pfak_1, idx_pfak_1 = calculate_spectrum_autocorrel_fft(pfak_list[1:len(pfak_list) - 1],
                                                                           sampling_rate)
    build_spectrum(freq_pfak_1[idx_pfak_1], ps_pfak_1[idx_pfak_1], 'PFAK PSD OF ' + 'Source CDS'+str(len(source_sig)))
    #
    freq_afak_1, ps_afak_1, idx_afak_1 = calculate_spectrum_autocorrel_fft(afak_list[1:len(pfak_list) - 1],
                                                                           sampling_rate)
    build_spectrum(freq_afak_1[idx_afak_1], ps_afak_1[idx_afak_1], 'AFAK PSD OF CS' + 'Source CDS'+str(len(source_sig)))

    # from 1 because the 0th element(decimation coef 1)
    # is the same as the source signal
    for i in range(1, 3):
        sigName = 'CDS{0} Decimation Coef.'.format(len(source_sig)) + str(decimations[i][1])
        print('\n' + sigName)
        pfak_list, afak_list = test_auto_correl(decimations[i][0])
        build_plot(pfak_list, 'ПФАК ' + sigName)
        build_plot(afak_list, 'АФАК ' + sigName)

        # calculate spctrum using pfak list

        freq_pfak, ps_pfak = calculate_spectrum_autocorrel(pfak_list[1:len(pfak_list)-1], sampling_rate)
        # calculate spectrum using afak list
        freq_afak, ps_afak = calculate_spectrum_autocorrel(afak_list[1:len(afak_list) - 1], sampling_rate)

        # printing and build plot
        print('\nПФАК без учета основных пиков:', pfak_list[1:len(pfak_list) - 1])
        pfak_spectrum_info(freq_pfak, ps_pfak, sigName)
        print('\nАФАК без учета основных пиков:', afak_list[1:len(afak_list) - 1])
        afak_spectrum_info(freq_afak, ps_afak, sigName)

        # if you need a left part but it make
        # no sense to use it because its mirrored
        freq_pfak_1, ps_pfak_1, idx_pfak_1 = calculate_spectrum_autocorrel_fft(pfak_list[1:len(pfak_list) - 1],
                                                                               sampling_rate)
        build_spectrum(freq_pfak_1[idx_pfak_1], ps_pfak_1[idx_pfak_1], 'PFAK PSD OF ' + sigName)
        #
        freq_afak_1, ps_afak_1, idx_afak_1 = calculate_spectrum_autocorrel_fft(afak_list[1:len(pfak_list) - 1],
                                                                               sampling_rate)
        build_spectrum(freq_afak_1[idx_afak_1], ps_afak_1[idx_afak_1], 'AFAK PSD OF CS' + sigName)

    # PLOTLY PLOT all above are regular plots with matplotlib
    # build_spectrum_plotly(frequency=freq, power_spectrum=ps,
    #                       graph_name='../plotly_plots/CDS_{0}_Spectrum'.format(len(source_sig)))


    # freq_1, ps_1 = signal.periodogram(pfak_list, sampling_rate)
    # print('Frequency:', freq_1)
    # print('PSD', ps_1)
    # build_spectrum(freq_1, ps_1)


def test_derivative_cs_spectrum():
    p = 16
    h = Hadamar(p)
    cs = CryptoSignal(p)
    # setting sampling rate
    sampling_rate = 30
    # Putting function into variable to use it later
    pfak_spectrum_info = print_spectrum_info_w_plot('PFAK')
    afak_spectrum_info = print_spectrum_info_w_plot('AFAK')

    # creating source signal and hadamard matrix
    source_sig = cs.generateDefRandomSeq(4)
    hadamar_sig_list = h.getHadamMatrix()

    # writing hadamard matrix into file
    writeListInFile(hadamar_sig_list, "D:/DIPLOM/спектры_маг_досл/обновл_спектрКСпроизводные/hadamar"
                    + str(p) + ".txt")
    # derivative
    dersig, combinations = derivativeSigFromTo([source_sig], hadamar_sig_list, 1, 4)

    print('Исходный сигнал\nCS#0: ', source_sig)
    print('Получаем производные сигналы:')
    print_derivative(dersig, combinations)

    for i in range(0,len(dersig)):
        sigName = 'Derivative Signal #'+str(i) \
                  + "\n(CS#{0} and HADAMAR#{1})".format(combinations[i][0], combinations[i][1])
        print('\n'+sigName)
        pfak_list, afak_list = test_auto_correl(dersig[i])
        build_plot(pfak_list, 'ПФАК '+sigName)
        build_plot(afak_list, 'АФАК '+sigName)


        # calculate spctrum using pfak list
        freq_pfak, ps_pfak = calculate_spectrum_autocorrel(pfak_list[1:len(pfak_list) - 1], sampling_rate)
        # calculate spectrum using afak list
        freq_afak, ps_afak = calculate_spectrum_autocorrel(afak_list[1:len(afak_list) - 1], sampling_rate)

        # printing and build plot
        print('\nПФАК без учета основных пиков:', pfak_list[1:len(pfak_list) - 1])
        pfak_spectrum_info(freq_pfak,ps_pfak,sigName)
        print('\nАФАК без учета основных пиков:', afak_list[1:len(afak_list) - 1])
        afak_spectrum_info(freq_afak,ps_afak,sigName)

        # build_spectrum_plotly(frequency=freq, power_spectrum=ps,
        #                       graph_name='../plotly_plots/DERIVATIVE#{0}_{1}_Spectrum'.format(i,len(sig)))
        # if you need a left part but it make
        # no sense to use it because its mirrored
        freq_pfak_1, ps_pfak_1, idx_pfak_1 = calculate_spectrum_autocorrel_fft(pfak_list[1:len(pfak_list) - 1],
                                                                               sampling_rate)
        build_spectrum(freq_pfak_1[idx_pfak_1], ps_pfak_1[idx_pfak_1], 'PFAK PSD OF ' + sigName)
        #
        freq_afak_1, ps_afak_1, idx_afak_1 = calculate_spectrum_autocorrel_fft(afak_list[1:len(pfak_list) - 1],
                                                                               sampling_rate)
        build_spectrum(freq_afak_1[idx_afak_1], ps_afak_1[idx_afak_1], 'AFAK PSD OF ' + sigName)


def test_derivative_cds_spectrum():
    # Putting function into variable to use it later
    pfak_spectrum_info = print_spectrum_info_w_plot('PFAK')
    afak_spectrum_info = print_spectrum_info_w_plot('AFAK')

    cds = CDS(257)
    cds.print_general_info()
    cds.print_table()
    source_sig = cds.table[5]
    h = Hadamar(256)
    hadamar_sig_list = h.getHadamMatrix()

    dersig, combinations = derivativeSigFromTo([source_sig], hadamar_sig_list, 1, 5)
    # setting sampling rate
    sampling_rate = 30

    print('Исходный сигнал\nCDS#0: ', source_sig)
    print('Получаем производные сигналы:')
    print_derivative(dersig, combinations)

    for i in range(0, len(dersig)):
        sigName = 'Derivative Signal #' + str(i) \
                  + "\n(CDS#{0} and HADAMAR#{1})".format(combinations[i][0], combinations[i][1])
        print(sigName)

        pfak_list, afak_list = test_auto_correl(dersig[i])
        build_plot(pfak_list, 'ПФАК ' + sigName)
        build_plot(afak_list, 'АФАК ' + sigName)

        # calculate spctrum using pfak list
        freq_pfak, ps_pfak = calculate_spectrum_autocorrel(pfak_list[1:len(pfak_list) - 1], sampling_rate)
        # calculate spectrum using afak list
        freq_afak, ps_afak = calculate_spectrum_autocorrel(afak_list[1:len(afak_list) - 1], sampling_rate)

        # printing and build plot
        print('\nПФАК без учета основных пиков:', pfak_list[1:len(pfak_list) - 1])
        pfak_spectrum_info(freq_pfak, ps_pfak, sigName)
        print('\nАФАК без учета основных пиков:', afak_list[1:len(afak_list) - 1])
        afak_spectrum_info(freq_afak, ps_afak, sigName)

        freq_pfak_1, ps_pfak_1, idx_pfak_1 = calculate_spectrum_autocorrel_fft(pfak_list[1:len(pfak_list) - 1],
                                                                               sampling_rate)
        build_spectrum(freq_pfak_1[idx_pfak_1], ps_pfak_1[idx_pfak_1], 'PFAK PSD OF ' + sigName)
        #
        freq_afak_1, ps_afak_1, idx_afak_1 = calculate_spectrum_autocorrel_fft(afak_list[1:len(pfak_list) - 1],
                                                                               sampling_rate)
        build_spectrum(freq_afak_1[idx_afak_1], ps_afak_1[idx_afak_1], 'AFAK PSD OF ' + sigName)


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

    # fak_list_copy =copy.deepcopy(fak_list)
    # fak_list_copy.pop(0)
    # fak_list_copy.pop()
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
    # test_cs_spectrum()

    test_cds_spectrum()

    # test_derivative_cs_spectrum()

#  test_derivative_cds_spectrum()



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

