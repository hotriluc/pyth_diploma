import math
import numpy as np
import random
from scipy.integrate import quad
import matplotlib.pyplot as plt

from modules.noise import print_info
from modules.plot import build_BER


def integrand(t,sig_with_noise,w_zero):
    return sig_with_noise[t]*np.sin(w_zero*t)

def diffrence(x,x1,k):
    res = 0
    for i in range(0,k):
        res+= math.fmod(  math.fmod((math.floor(x/2**i)),2) +
                          math.fmod((math.floor(x1/2**i)),2)
                          ,2)
    return res

def test_agwn_analytical():
    f_zero = 1
    w_zero = 2 * math.pi * f_zero
    V = 1
    T = 1 / V
    Pw = 1
    k = 4

    N = 20
    M = 10000
    a = math.sqrt((8 / 5) * Pw)

    x = math.floor(np.random.randint(0, 2 ** k))
    print('X: ', x)

    x_high = math.floor(x / 2 ** 2)
    x_low = round(math.fmod(x, 2 ** 2))

    print('High: {0} Low: {1}'.format(x_high, x_low))

    s = lambda t: a * ((3 / 2) - x_high) * np.sin(w_zero * t) - a * ((3 / 2) - x_low) * np.cos(w_zero * t)

    p_sn = []

    for s_n in range(1, N):
        print(s_n)
        count = 0
        n_zero = 1 / s_n
        for i in range(0, M):
            r = np.random.normal(0, math.sqrt(n_zero / 4), 10)

            # fourier
            noise = lambda t: r[0] / 2 + np.sum(
                [r[2 * j - 1] * np.sin((2 * math.pi * j / 2 * T) * t) + r[2 * j] * np.cos((2 * math.pi * j / 2 * T) * t)
                 for j in range(0, 4)])

            # signal with noise
            st = lambda t: s(t) + noise(t)

            # demodulation
            function_alpha = lambda t: st(t) * np.sin(w_zero * t)
            alpha = quad(function_alpha, 0, 1)
            res_alpha = (2 / (T * a)) * alpha[0]

            function_beta = lambda t: st(t) * np.cos(w_zero * t)
            beta = quad(function_beta, 0, 1)
            res_beta = (2 / (T * a)) * beta[0]

            high_1 = round((3 / 2) - res_alpha)
            if high_1 < 0:
                high_1 = 0
            elif high_1 > (2 ** k) - 1:
                high_1 = (2 ** k) - 1
            else:
                high_1 = high_1

            low_1 = round((3 / 2) + res_beta)
            if low_1 < 0:
                low_1 = 0
            elif low_1 > (2 ** k) - 1:
                low_1 = (2 ** k) - 1
            else:
                low_1 = low_1

            x1 = high_1 * (2 ** 2) + low_1

            dif = diffrence(x, x1, k)
            # print(x,x1,dif)

            count += dif

        p_sn.append(count / (k * M))
        print_info(s_n, s_n, p_sn[s_n - 1])


    print(p_sn)

    snr_inDb = range(0,20)
    build_BER(snr_inDb,p_sn)


if __name__=="__main__":

    f_zero = 1
    w_zero = 2*math.pi*f_zero
    V = 1
    T = 1/V
    Pw = 1
    k = 4


    N = 20
    snr_in_db_range = range(1,N)
    M = 10000
    a = math.sqrt((8/5)*Pw)

    x = math.floor(np.random.randint(0,2**k))
    print('X: ',x)

    x_high = math.floor(x / 2 ** 2)
    x_low = round(math.fmod(x, 2 ** 2))

    print('High: {0} Low: {1}'.format(x_high,x_low))

    s = lambda t: a*((3/2)-x_high)*np.sin(w_zero*t) - a*((3/2)-x_low)*np.cos(w_zero*t)

    p_sn = []


    for s_n in range(1,N):
        print(s_n)
        count = 0
        n_zero = 1/s_n
        for i in range(0,M):
            r = np.random.normal(0,math.sqrt(n_zero/4),10)

            # fourier
            noise = lambda t: r[0]/2 + np.sum([r[2*j-1]*np.sin((2*math.pi*j/2*T)*t) + r[2*j]*np.cos((2*math.pi*j/2*T)*t)
                                        for j in range(0,4)])

            # signal with noise
            st = lambda t: s(t)+noise(t)

            # demodulation
            function_alpha = lambda t: st(t)*np.sin(w_zero*t)
            alpha= quad(function_alpha,0,1)
            res_alpha = (2/(T*a))*alpha[0]

            function_beta = lambda t: st(t)*np.cos(w_zero*t)
            beta= quad(function_beta,0,1)
            res_beta = (2/(T*a))*beta[0]

            high_1 = round((3/2)-res_alpha)
            if high_1 < 0:
                high_1 = 0
            elif high_1>(2**k)-1:
                high_1 = (2**k)-1
            else:
                high_1 = high_1

            low_1 = round((3 / 2) + res_beta)
            if low_1 < 0:
                low_1 = 0
            elif low_1 > (2 ** k) - 1:
                low_1 = (2 ** k) - 1
            else:
                low_1 = low_1

            x1 = high_1*(2**2)+low_1


            dif = diffrence(x,x1,k)
            # print(x,x1,dif)

            count+=dif

        p_sn.append(count/(k*M))
        print_info(s_n, count, p_sn[s_n - 1])



    print(p_sn)

    build_BER(snr_in_db_range,p_sn)