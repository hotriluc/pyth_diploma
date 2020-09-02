import copy

from modules import calculations as cal, arr_procedures as ap;
from classes.CryptoSignal import CryptoSignal

#  FOR 1 SIGNAL
def test_auto_correl (source_sig, soure_sig_len):
    print("Signal: ",source_sig)

    sig1_ = copy.deepcopy(source_sig)
    sig2_ = copy.deepcopy(source_sig)

    print("PFAK")
    pereodic_auto_corel_list = cal.getCorellation(sig1_, sig2_)
    print("R = ", pereodic_auto_corel_list)
    print("Rmax = ", cal.getMax(pereodic_auto_corel_list, 1, soure_sig_len , True))

    print("AFAK")
    apereodic_auto_corel_list = cal.getCorellation(sig1_, sig2_, True)
    print("R = ", apereodic_auto_corel_list)
    print("Rmax = ", cal.getMax(apereodic_auto_corel_list, 1, soure_sig_len))

    return  pereodic_auto_corel_list, apereodic_auto_corel_list

# 1 source singal with each from ansamble
def test_cross_correl (source_sig, ansamble_of_sig):
    sig1_ = copy.deepcopy(source_sig)
    ansamble_of_pereodic_cross_corel_list = cal.corel_source_and_rest(sig1_, ansamble_of_sig, "PFVK")
    print("\nPFVK")
    cal.printFullStat(ansamble_of_pereodic_cross_corel_list, 0, len(source_sig), True)
    cal.printFullStat(ansamble_of_pereodic_cross_corel_list, 0, len(source_sig))


def test_stat_correl(decimation_list):

    only_decimated_signals = get_decimated_signals(decimation_list)
    print("SOURCE AND REST")
    test_cross_correl(source_sig, only_decimated_signals[1:10])

    print("\nPFAK Decimated SIGNALS")
    # print(len(only_decimated_signals))
    # asnsam_pfak_list = cal.auto_corel_all(only_decimated_signals, "PFAK")
    # cal.printFullStat(asnsam_pfak_list, 1, 256 - 1, True)
    # cal.printFullStat(asnsam_pfak_list, 1, 256 - 1)
    pfak_function = ansamble_correlation('PFAK')
    afak_function = ansamble_correlation('AFAK')
    pfvk_function = ansamble_correlation('PFVK')
    afvk_function = ansamble_correlation('AFVK')

    pfak_function(only_decimated_signals[1:10])
    afak_function(only_decimated_signals[1:10])
    pfvk_function(only_decimated_signals[1:10])
    afvk_function(only_decimated_signals[1:10])




def ansamble_correlation(mode):

    def fak_stat(ansamble_of_sig):
        print(mode)
        sig_len = len(ansamble_of_sig[0])
        if (len(ansamble_of_sig) > 0):
            asnsam_fak_list = cal.auto_corel_all(ansamble_of_sig, mode)
            cal.printFullStat(asnsam_fak_list, 1, sig_len - 1, True)
            cal.printFullStat(asnsam_fak_list, 1, sig_len - 1)

    def fvk_stat(ansamble_of_sig):
        print(mode)
        sig_len = len(ansamble_of_sig[0])
        if (len(ansamble_of_sig) > 0):
            pair_list_cryptosig = cal.getPair([i for i in range(0, len(ansamble_of_sig))])
            pfvk_cryptosig_list = cal.cross_corel_btwn_pairs(ansamble_of_sig, "PFVK")
            cal.printFullStat(pfvk_cryptosig_list, 0, sig_len, True, list_of_num=pair_list_cryptosig)
            cal.printFullStat(pfvk_cryptosig_list, 0, sig_len, list_of_num=pair_list_cryptosig)

    if (mode == 'PFAK') or (mode =='AFAK'):
        return fak_stat
    elif (mode == 'PFVK') or (mode =='AFVK'):
        return fvk_stat
    else:
        print("Something wrong there is no mode like that")



# decimation list consist lists that have elements signals and its decimtion coefficient
def get_decimated_signals(decimation_list):
    only_decimated_signals = list()
    for i in range(0, len(decimation_list)):
        only_decimated_signals.append(decimation_list[i][0])
    return only_decimated_signals


if __name__ =='__main__':
    # Generating random sequence with 256 el
    cs = CryptoSignal(256)
    source_sig = cs.generateDefRandomSeq(32)

    #Source signal calculate PFAK, AFAK
    pfak_list,afak_list = test_auto_correl(source_sig, len(source_sig))

    cal.printFullStat([pfak_list],1,len(source_sig)-1,True)



    # Getting singals created with decimation method
    decimations = cal.getDecimation(source_sig)
    test_stat_correl(decimations)

    #For each decimation signal calculate PFAK AFAK

