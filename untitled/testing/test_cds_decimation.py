import copy

from classes.CDS import CDS
from modules import calculations as cal, arr_procedures as ap
from modules.arr_procedures import test_auto_correl, decimation, get_decimated_signals, test_cross_correl


def askForP():
    # input until its prime
    p = 0
    while True:
        p = int(input("Enter P:"))
        if cal.isPrime(p):
            print("Prime")
            break
        else:
            print("is not prime")
    return  p

# coef 2
def test_cds_decimation_2():
    p = askForP()
    signal = CDS(p)
    signal.print_general_info()
    signal.print_table()
    # getting source signal from the table
    source_sig = signal.table[5]

    print("SOURCE SIGNAL: ")
    # Source signal calculate PFAK, AFAK
    pfak_list, afak_list = test_auto_correl(source_sig)

    # Copy source signal (in order to not interfere source signal)
    sig1_ = copy.deepcopy(source_sig)
    sig2_ = [0 for i in range(len(source_sig))]
    # creating singal with decimation
    decimation(sig1_, sig2_, 2)
    print("DECIMATION 2: ")
    # decimated signal calculate PFAK, AFAK
    dec_pfak_list, dec_afak_list = test_auto_correl(sig2_)

# test with all decimated sig
def test_cds_decimation(source_sig,decimation_list):

    only_decimated_signals = get_decimated_signals(decimation_list)
    print("SOURCE AND REST")
    test_cross_correl(source_sig, only_decimated_signals[1:10])

    print("\nPFAK Decimated SIGNALS")
    # print(len(only_decimated_signals))
    # asnsam_pfak_list = cal.auto_corel_all(only_decimated_signals, "PFAK")
    # cal.printFullStat(asnsam_pfak_list, 1, 256 - 1, True)
    # cal.printFullStat(asnsam_pfak_list, 1, 256 - 1)

    # Defined variables for function that will
    # calculate correlation for whole ensemble of signals
    pfak_function = ap.ansamble_correlation('PFAK')
    afak_function = ap.ansamble_correlation('AFAK')
    pfvk_function = ap.ansamble_correlation('PFVK')
    afvk_function = ap.ansamble_correlation('AFVK')

    pfak_function(only_decimated_signals[1:10])
    afak_function(only_decimated_signals[1:10])
    pfvk_function(only_decimated_signals[1:10])
    afvk_function(only_decimated_signals[1:10])





if __name__=='__main__':

    test_cds_decimation_2()

    # p = askForP()
    # signal = CDS(p)
    # signal.print_general_info()
    # source_sig = signal.table[5]
    #
    # # Source signal calculate PFAK, AFAK
    # pfak_list, afak_list = test_auto_correl(source_sig)
    # cal.printFullStat([pfak_list], 1, len(source_sig) - 1, True)
    # cal.printFullStat([afak_list], 1, len(source_sig) - 1, True)
    #
    # # Getting singals created with decimation method
    # decimations = ap.getDecimation(source_sig)
    # test_cds_decimation(source_sig, decimations)