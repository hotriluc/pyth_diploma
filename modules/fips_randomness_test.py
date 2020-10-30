from collections import Counter



def monobit_test(bin_string):
    number_of_ones = 0
    for bit in bin_string:
        if bit == '1':
            number_of_ones += 1
    if (number_of_ones > 9654) and (number_of_ones < 10346):
        return (True, number_of_ones)
    else:
        return (False, number_of_ones)


def poker_test(bin_string):
    contiguous_segments = [bin_string[i:i+4] for i in range(0, len(bin_string), 4)]
    contador = Counter(contiguous_segments)

    f_i = 0
    for string, quantidade in contador.items():
        f_i += quantidade*quantidade
    x = ((16/5000) * f_i) - 5000

    if (x > 1.03) and (x < 57.4):
        return (True, x)
    else:
        return (False, x)


def runs_test(bin_string):
    count = 1
    repetitions = []
    counter_0 = [0, 0, 0, 0, 0, 0]
    counter_1 = [0, 0, 0, 0, 0, 0]
    if len(bin_string) > 1:
        for i in range(1, len(bin_string)):
            if bin_string[i - 1] == bin_string[i]:
                count += 1
            else:
                repetitions.append([bin_string[i - 1], count])
                count = 1
        repetitions.append([bin_string[i], count])

    for rep in repetitions:
        if rep[0] == '0':
            if rep[1] >= 6:
                counter_0[5] += 1
            else:
                counter_0[rep[1]-1] += 1
        if rep[0] == '1':
            if rep[1] >= 6:
                counter_1[5] += 1
            else:
                counter_1[rep[1]-1] += 1

    zero_ok = False
    one_ok = False
    if (counter_0[0] > 2267) and (counter_0[0] < 2733) and (counter_0[1] > 1079) and (counter_0[1] < 1421) and \
        (counter_0[2] > 502) and (counter_0[2] < 748) and (counter_0[3] > 223) and (counter_0[3] < 402) and \
        (counter_0[4] > 90) and (counter_0[4] < 223) and (counter_0[5] > 90) and (counter_0[5] < 223):
        zero_ok = True

    if (counter_1[0] > 2267) and (counter_1[0] < 2733) and (counter_1[1] > 1079) and (counter_1[1] < 1421) and \
        (counter_1[2] > 502) and (counter_1[2] < 748) and (counter_1[3] > 223) and (counter_1[3] < 402) and \
        (counter_1[4] > 90) and (counter_1[4] < 223) and (counter_1[5] > 90) and (counter_1[5] < 223):
        one_ok = True

    if zero_ok and one_ok:
        return (True, counter_1, counter_0)
    else:
        return (False, counter_1, counter_0)


def long_run(bin_string):
    count = 1
    longest = 0
    if len(bin_string) > 1:
        for i in range(1, len(bin_string)):
            if bin_string[i - 1] == bin_string[i]:
                count += 1
            else:
                if count >= 34:
                    return False
                if count > longest:
                    longest = count
                count = 1
    return (True,longest)