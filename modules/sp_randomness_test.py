import math
import sys
import numpy
import random
from fractions import Fraction
from  modules.gamma_functions import *

# NIST SP tests

def count_ones_zeroes(bits):
    ones = 0
    zeroes = 0
    # Counting 0's and 1's
    for bit in bits:
        if (bit == 1):
            ones += 1
        else:
            zeroes += 1
    return (zeroes, ones)

#======================Монобитный тест
def monobit_test(bits):
    n = len(bits)

    zeroes, ones = count_ones_zeroes(bits)
    # Sn = abs (X1 + X2 +...+Xn)
    # Sum of all bits 1 and -1 is the same as number of 1s minus number of 0s
    s = abs(ones - zeroes)
    print("  Ones count   = %d" % ones)
    print("  Zeroes count = %d" % zeroes)

    # Calculating P-value, where efrc - error function
    p = math.erfc(float(s) / (math.sqrt(float(n)) * math.sqrt(2.0)))

    success = (p >= 0.01)
    return (success, p)

##====================== частотный блочный тест
def frequency_within_block_test(bits):
    # Compute number of blocks M = block size. N=num of blocks
    # N = floor(n/M)
    # miniumum block size 20 bits, most blocks 100
    n = len(bits)
    M = 20
    N = int(math.floor(n / M))
    if N > 99:
        N = 99
        M = int(math.floor(n / N))

    if len(bits) < 100:
        print("Too little data for test. Supply at least 100 bits")
        return (False, 1.0)

    print("  n = %d" % len(bits))
    print("  N = %d" % N)
    print("  M = %d" % M)

    num_of_blocks = N
    block_size = M  # int(math.floor(len(bits)/num_of_blocks))
    # n = int(block_size * num_of_blocks)

    # Calculating zeroes and ones for each blocks
    proportions = list()
    for i in range(num_of_blocks):
        block = bits[i * (block_size):((i + 1) * (block_size))]
        zeroes, ones = count_ones_zeroes(block)
        proportions.append(Fraction(ones, block_size))

    # Calculating Chi Square
    chisq = 0.0
    for prop in proportions:
        chisq += 4.0 * block_size * ((prop - Fraction(1, 2)) ** 2)

    # Calculating P-value, gammainc is gamma function
    p = gammaincc((num_of_blocks / 2.0), float(chisq) / 2.0)
    success = (p >= 0.01)
    return (success, p)
#======================

#======================Тест на одинаковые идущие подряд биты
def runs_test(bits):
    n = len(bits)
    zeroes, ones = count_ones_zeroes(bits)

    prop = float(ones) / float(n)
    print("  prop ", prop)

    tau = 2.0 / math.sqrt(n)
    print("  tau ", tau)

    if abs(prop - 0.5) > tau:
        return (False, 0.0)

    vobs = 1.0
    for i in range(n - 1):
        if bits[i] != bits[i + 1]:
            vobs += 1.0

    print("  vobs ", vobs)

    p = math.erfc(abs(vobs - (2.0 * n * prop * (1.0 - prop))) / (2.0 * math.sqrt(2.0 * n) * prop * (1 - prop)))
    success = (p >= 0.01)
    return (success, p)
#======================

#======================Тест на самую длинную последовательность из единиц в блоке

def probs(K, M, i):
    M8 = [0.2148, 0.3672, 0.2305, 0.1875]
    M128 = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
    M512 = [0.1170, 0.2460, 0.2523, 0.1755, 0.1027, 0.1124]
    M1000 = [0.1307, 0.2437, 0.2452, 0.1714, 0.1002, 0.1088]
    M10000 = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]
    if (M == 8):
        return M8[i]
    elif (M == 128):
        return M128[i]
    elif (M == 512):
        return M512[i]
    elif (M == 1000):
        return M1000[i]
    else:
        return M10000[i]

def longest_run_ones_in_a_block_test(bits):
    n = len(bits)

    if n < 128:
        return (False, 1.0, None)
    elif n < 6272:
        M = 8
    elif n < 750000:
        M = 128
    else:
        M = 10000

    # compute new values for K & N
    if M == 8:
        K = 3
        N = 16
    elif M == 128:
        K = 5
        N = 49
    else:
        K = 6
        N = 75

    # Table of frequencies
    v = [0, 0, 0, 0, 0, 0, 0]

    for i in range(N):  # over each block
        # find longest run
        block = bits[i * M:((i + 1) * M)]  # Block i

        run = 0
        longest = 0
        for j in range(M):  # Count the bits.
            if block[j] == 1:
                run += 1
                if run > longest:
                    longest = run
            else:
                run = 0

        if M == 8:
            if longest <= 1:
                v[0] += 1
            elif longest == 2:
                v[1] += 1
            elif longest == 3:
                v[2] += 1
            else:
                v[3] += 1
        elif M == 128:
            if longest <= 4:
                v[0] += 1
            elif longest == 5:
                v[1] += 1
            elif longest == 6:
                v[2] += 1
            elif longest == 7:
                v[3] += 1
            elif longest == 8:
                v[4] += 1
            else:
                v[5] += 1
        else:
            if longest <= 10:
                v[0] += 1
            elif longest == 11:
                v[1] += 1
            elif longest == 12:
                v[2] += 1
            elif longest == 13:
                v[3] += 1
            elif longest == 14:
                v[4] += 1
            elif longest == 15:
                v[5] += 1
            else:
                v[6] += 1

    # Compute Chi-Sq
    chi_sq = 0.0
    for i in range(K + 1):
        p_i = probs(K, M, i)
        upper = (v[i] - N * p_i) ** 2
        lower = N * p_i
        chi_sq += upper / lower
    print("  n = " + str(n))
    print("  K = " + str(K))
    print("  M = " + str(M))
    print("  N = " + str(N))
    print("  chi_sq = " + str(chi_sq))
    p = gammaincc(K / 2.0, chi_sq / 2.0)

    success = (p >= 0.01)
    return (success, p)
#======================

#======================спектральній тест
def dft_test(bits):
    n = len(bits)
    if (n % 2) == 1:  # Make it an even number
        bits = bits[:-1]

    ts = list()  # Convert to +1,-1
    for bit in bits:
        ts.append((bit * 2) - 1)

    ts_np = numpy.array(ts)
    fs = numpy.fft.fft(ts_np)  # Compute DFT

    if sys.version_info > (3, 0):
        mags = abs(fs)[:n // 2]  # Compute magnitudes of first half of sequence
    else:
        mags = abs(fs)[:n / 2]  # Compute magnitudes of first half of sequence

    T = math.sqrt(math.log(1.0 / 0.05) * n)  # Compute upper threshold
    N0 = 0.95 * n / 2.0
    print("  N0 = %f" % N0)

    N1 = 0.0  # Count the peaks above the upper theshold
    for mag in mags:
        if mag < T:
            N1 += 1.0
    print("  N1 = %f" % N1)
    d = (N1 - N0) / math.sqrt((n * 0.95 * 0.05) / 4)  # Compute the P value
    p = math.erfc(abs(d) / math.sqrt(2))

    success = (p >= 0.01)
    return (success, p)
#======================

#======================serial test Тест на подпоследовательности
def int2patt(n, m):
    pattern = list()
    for i in range(m):
        pattern.append((n >> i) & 1)
    return pattern


def countpattern(patt, bits, n):
    thecount = 0
    for i in range(n):
        match = True
        for j in range(len(patt)):
            if patt[j] != bits[i + j]:
                match = False
        if match:
            thecount += 1
    return thecount


def psi_sq_mv1(m, n, padded_bits):
    counts = [0 for i in range(2 ** m)]
    for i in range(2 ** m):
        pattern = int2patt(i, m)
        count = countpattern(pattern, padded_bits, n)
        counts.append(count)

    psi_sq_m = 0.0
    for count in counts:
        psi_sq_m += (count ** 2)
    psi_sq_m = psi_sq_m * (2 ** m) / n
    psi_sq_m -= n
    return psi_sq_m


def serial_test(bits, patternlen=None):
    n = len(bits)
    if patternlen != None:
        m = patternlen
    else:
        m = int(math.floor(math.log(n, 2))) - 2

        if m < 4:
            print("Error. Not enough data for m to be 4")
            return (False, 0)
        m = 4

    # Step 1
    padded_bits = bits + bits[0:m - 1]

    # Step 2
    psi_sq_m = psi_sq_mv1(m, n, padded_bits)
    psi_sq_mm1 = psi_sq_mv1(m - 1, n, padded_bits)
    psi_sq_mm2 = psi_sq_mv1(m - 2, n, padded_bits)

    delta1 = psi_sq_m - psi_sq_mm1
    delta2 = psi_sq_m - (2 * psi_sq_mm1) + psi_sq_mm2

    P1 = gammaincc(2 ** (m - 2), delta1 / 2.0)
    P2 = gammaincc(2 ** (m - 3), delta2 / 2.0)

    print("  psi_sq_m   = ", psi_sq_m)
    print("  psi_sq_mm1 = ", psi_sq_mm1)
    print("  psi_sq_mm2 = ", psi_sq_mm2)
    print("  delta1     = ", delta1)
    print("  delta2     = ", delta2)
    print("  P1         = ", P1)
    print("  P2         = ", P2)

    success = (P1 >= 0.01) and (P2 >= 0.01)
    return (success, [P1, P2])
#======================
