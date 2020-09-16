import copy

import modules.arr_procedures
from modules import calculations as cal, arr_procedures as ap;
from classes.CryptoSignal import CryptoSignal


def test_cs_decimation(source_sig,decimation_list):

    only_decimated_signals = ap.get_decimated_signals(decimation_list)
    print("SOURCE AND REST")
    ap.test_cross_correl(source_sig, only_decimated_signals[1:10])

    print("\nPFAK Decimated SIGNALS")
    # print(len(only_decimated_signals))
    # asnsam_pfak_list = cal.auto_corel_all(only_decimated_signals, "PFAK")
    # cal.printFullStat(asnsam_pfak_list, 1, 256 - 1, True)
    # cal.printFullStat(asnsam_pfak_list, 1, 256 - 1)
    # Defined variables for function that will
    # calculate correlation for whole ensemble of signals
    pfak_function = modules.arr_procedures.ansamble_correlation('PFAK')
    afak_function = modules.arr_procedures.ansamble_correlation('AFAK')
    pfvk_function = modules.arr_procedures.ansamble_correlation('PFVK')
    afvk_function = modules.arr_procedures.ansamble_correlation('AFVK')

    pfak_function(only_decimated_signals[1:10])
    afak_function(only_decimated_signals[1:10])
    pfvk_function(only_decimated_signals[1:10])
    afvk_function(only_decimated_signals[1:10])

    # ap.print_sig_in_list(only_decimated_signals)



def printDecimation(decimations):
    for i in range(len(decimations)):
        print('Decimation coefficient: ',decimations[i][1])
        print(i,') ',decimations[i][0])

if __name__ =='__main__':
    # Generating random sequence with 256 el
    cs = CryptoSignal(256)
    source_sig = cs.generateDefRandomSeq(32)

    #Source signal calculate PFAK, AFAK
    pfak_list,afak_list = ap.test_auto_correl(source_sig)

    # print source signal's full stat of PFAK
    cal.printFullStat([pfak_list],1,len(source_sig)-1,True)
    cal.printFullStat([pfak_list], 1, len(source_sig) - 1)
    cal.printFullStat([afak_list], 1, len(source_sig) - 1,True)
    cal.printFullStat([afak_list], 1, len(source_sig) - 1)

    # Getting singals created with decimation method
    decimations = modules.arr_procedures.getDecimation(source_sig)



    test_cs_decimation(source_sig,decimations)

    printDecimation(decimations)
    #For each decimation signal calculate PFAK AFAK

