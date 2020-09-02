import copy
import itertools
import pickle
import numpy as np
from modules.calculations import coprimes, printFullStat, getPair


#==============================BASIC MANIPULATION WITH ARRAYS==============================
# write string



def writeListInFile(aList:list,filepath):
    f = open(filepath,"w")
    for i in range(0,len(aList)):
        f.write(str(i)+") "+str(aList[i])+"\n")

    f.close()

# write binary mode
def writeListInBinFile(aList:list,file_name):
    with open(file_name, 'wb') as F:
        # Dump the list to file
        pickle.dump(aList, F)
    F.close()

def loadFromBinFile(file_name):
    with open(file_name, 'rb') as F:
        aList = pickle.load(F)
    F.close()
    return aList


def print_2d_arr(aList):
    for row in aList:
        for item in row:
            print("{0:5d}".format(item), end="")
        print("")


# print list of list(signals)
def print_sig_in_list(aList):
    i = 0
    for item in aList:
        print(i, ") ", item)
        i += 1


# using simple pop and insert we created Shifting list with zeroing
def ShiftRight(aList: list, steps: int):
    # for negative steps
    if steps < 0:
        steps = abs(steps)
        for i in range(steps):
            # pop first element
            # everything is shifted to the left after we pop
            aList.pop(0)
            # adding to the end 0
            aList.append(0)
    else:
        for i in range(steps):
            # insert zero to the 0 position
            aList.insert(0, 0)
            # poping last el
            # everything is shifted to right
            aList.pop()


def CyclicShiftRight(aList: list, steps: int):
    # for negative steps
    if steps < 0:
        steps = abs(steps)
        for i in range(steps):
            # adding to the end popped 0th el
            aList.append(aList.pop(0))
    else:
        for i in range(steps):
            # adding to the beginning popped(last) el
            aList.insert(0, aList.pop())


# def ShiftRight(aList:list,pos:int):
# return aList[pos:len(aList):]*0 + aList[0:pos:]

# for i in range(1,len(aList)-1):




#============================== ADVANCED MANIPULATION WITH ARRAYS(SIGNALS==============================

#============================== DECIMATION==============================
def decimation(a_List: list, b_List: list, d: int):
    for i in range(0, len(a_List)):
        pos = (d + d * i) % len(a_List)
        b_List[i] = a_List[pos]


def getDecimation(source_signal):
   #getting source singal length
    sig_len = len(source_signal)
    # Copy source signal (in order to not interfere source signal)
    sig1_ = copy.deepcopy(source_signal)
    # Creating list for storing signals
    decimation_list = list()

    #Geting coprimes of sign len e.g len=  256 coprimes = [1,3,5,7 ... 255]
    # index 1 because of coprimes method return tuple of 2element
    # (the number of total coprimes, and list of coprimes)
    #
    coprime_list = coprimes(sig_len)[1]

    # For each coprime of source signal length we will create a signal using decimation
    for i in range(len(coprime_list)):
        # tmp for signal we are going to get with decimation
        sig2_ = [0 for i in range(sig_len)]

        # creating rest signals with decimation
        decimation(sig1_, sig2_, coprime_list[i])

        # appending decimation_list with list
        # that contains decimated sig and
        # decimation coefficient that used to create that sig
        decimation_list.append([sig2_, coprime_list[i]])
    return decimation_list

# decimation list consist lists that have elements signals and its decimtion coefficient
def get_decimated_signals(decimation_list):
    only_decimated_signals = list()
    for i in range(0, len(decimation_list)):
        only_decimated_signals.append(decimation_list[i][0])
    return only_decimated_signals





#============================== DERIVATIVE SIGNALS FORMATION==============================
# ansambles must contain same number of signals
# USING WITH HADAMAR DISCRETE SIGNALS in order to get derivative signals
def derivativeSig(ansamble_sig1: list, ansamble_sig2: list):
    der_sig_list = []
    for i in range(0, len(ansamble_sig1)):
        tmp = np.array(ansamble_sig1[i]) * np.array(ansamble_sig2[i])
        der_sig_list.append(tmp.tolist())

    return der_sig_list


def derivativeSigALL(ansamble_sig1: list, ansamble_sig2: list):
    der_sig_list = []
    sig_comb_list = []

    for i in range(0, len(ansamble_sig1)):
        for j in range(0, len(ansamble_sig2)):
            der_sig_list.append(np.multiply(ansamble_sig1[i], ansamble_sig2[j]).tolist())
            sig_comb_list.append((i, j))

    return der_sig_list, sig_comb_list

# Same as above but used starting and ending point of inner cycle (from to)
# of course you can used the first mentioned by passing slice of an array(list)
# but if you do that index of your arrays will stat from 0 for slice
# but this from to allows us to identify which exactly hadamar sinal was used to form
# derivative
def derivativeSigFromTo(ansamble_sig1: list, hadamar_sig: list,hadam_from,hadam_to):
    der_sig_list = []
    sig_comb_list = []
    for i in range(0, len(ansamble_sig1)):
        for j in range(hadam_from, hadam_to):
            der_sig_list.append(np.multiply(ansamble_sig1[i], hadamar_sig[j]).tolist())
            sig_comb_list.append((i, j))
    return der_sig_list, sig_comb_list



#============================== CORRELATION==============================

def calculate_correlation_coef(sig1_: list, sig2_: list):
    R = 0
    for i in range(0, len(sig1_)):
        tmp = sig1_[i] * sig2_[i]
        R += tmp
    return R

# source_sig - source signal is NOT SHIFTED shifted_sig - copy of the signal WILL BE SHIFTED ( for pereodic auto
# correlation)/ other signal (for pereodic cross correlation) flag = true for APEREODIC correaltion
# else default for PEREODIC
def getCorellation(source_sig: list, shifted_sig: list, flag: bool = False):
    # Creating copy of shifted signal to not trasform array from main program(for further usage)
    # because in Python list contains not val but reference to objects

    tmp_shifted_sig = copy.deepcopy(shifted_sig)

    correl_list = list()
    r = calculate_correlation_coef(source_sig, tmp_shifted_sig)
    correl_list.append(r)

    for i in range(0, len(source_sig)):
        if flag == False:
            CyclicShiftRight(tmp_shifted_sig, 1)
        else:
            ShiftRight(tmp_shifted_sig, 1)

        r = calculate_correlation_coef(source_sig, tmp_shifted_sig)
        correl_list.append(r)

    return correl_list
    # for i in range(0,len(sig1_)):

# E.g you have ansamble of signals and you want to know all cross-correlation between all possible pairs
# for derivative signals(with HADAMAR)
# ONLY TO GET CROSS CORRELATION
def cross_corel_btwn_pairs(list_with_signals: list, mode_name):
    aList = list()
    for pair in itertools.combinations(list_with_signals, 2):
        a_sig, b_sig = pair
        # print(pair)
        if mode_name == "PFVK":
            r = getCorellation(a_sig, b_sig)
        if mode_name == "AFVK":
            r = getCorellation(a_sig, b_sig, True)

        aList.append(r)
    return aList

# the same logic as above function
# but here you passing list pair
# this one without usin itertools
def cross_corel_btwn_pairs2(list_with_signals: list, pair_list: list, mode_name):
    aList = list()
    for x, y in pair_list:

        # print(pair)
        if mode_name == "PFVK":
            r = getCorellation(list_with_signals[x], list_with_signals[y])
        if mode_name == "AFVK":
            r = getCorellation(list_with_signals[x], list_with_signals[y], True)

        aList.append(r)
    return aList


# Having list with signals
# getting list of list with signals' pereodic/apereodic auto correlation function
def auto_corel_all(list_with_signals: list, mode_name):
    aList = list()
    sig_num_list = list()

    for item in list_with_signals:
        if mode_name == "PFAK":
            r = getCorellation(item, item)
        if mode_name == "AFAK":
            r = getCorellation(item, item, True)

        aList.append(r)

    return aList

# исходный сигнал с другими сигналами
# getting list of correlations of all signals
def corel_source_and_rest(source_sig, list_with_signals: list, mode_name):
    aList = list()
    for item in list_with_signals:
        if mode_name == "PFVK":
            r = getCorellation(source_sig, item)
        if mode_name == "AFVK":
            r = getCorellation(source_sig, item, True)
        if mode_name == "PFAK":
            r = getCorellation(item, item)
        if mode_name == "AFAK":
            r = getCorellation(item, item, True)

        # print(r)
        aList.append(r)
    return aList


# Used for testing ansamble of sig and printed their statistics
# using closure to keep DRY
def ansamble_correlation(mode):

    def fak_stat(ansamble_of_sig):
        print(mode)
        sig_len = len(ansamble_of_sig[0])
        if (len(ansamble_of_sig) > 0):
            asnsam_fak_list = auto_corel_all(ansamble_of_sig, mode)
            printFullStat(asnsam_fak_list, 1, sig_len - 1, True)
            printFullStat(asnsam_fak_list, 1, sig_len - 1)

    def fvk_stat(ansamble_of_sig):
        print(mode)
        sig_len = len(ansamble_of_sig[0])
        if (len(ansamble_of_sig) > 0):
            pair_list = getPair([i for i in range(0, len(ansamble_of_sig))])
            fvk_sig_list = cross_corel_btwn_pairs(ansamble_of_sig, mode)
            printFullStat(fvk_sig_list, 0, sig_len, True, list_of_num=pair_list)
            printFullStat(fvk_sig_list, 0, sig_len, list_of_num=pair_list)

    if (mode == 'PFAK') or (mode =='AFAK'):
        return fak_stat
    elif (mode == 'PFVK') or (mode =='AFVK'):
        return fvk_stat
    else:
        print("Something wrong there is no mode like that")