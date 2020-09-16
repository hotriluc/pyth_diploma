import modules.arr_procedures
from classes.Hadamar import Hadamar
from classes.CryptoSignal import CryptoSignal
from modules.arr_procedures import print_sig_in_list, derivativeSigFromTo
from modules import calculations as cal

if __name__ =="__main__":

    p = 256
    h = Hadamar(p)
    cs = CryptoSignal(p)

    # 2048 pfak 140
    # 256 pfak 32
    # 16 pfak 4
    # 512 pfak 52
    # 1024 pfak 81
    # 64 pfak 8
    hadamar_sig_list = h.getHadamMatrix()
    crypto_sig_ansam = cs.genereteAnsambleOfCryptoSig(5, 32)

    # for i in range(0, len(hadamar_sig_list)):
    #    print(i + 1, ") ", list(hadamar_sig_list[i]))

    # Defined variables for function that will
    # calculate correlation for whole ensemble of signals
    pfvk_stat = modules.arr_procedures.ansamble_correlation('PFVK')
    pfak_stat = modules.arr_procedures.ansamble_correlation('PFAK')

    print("\nCRYPTOSIG")
    print_sig_in_list(crypto_sig_ansam)

    sig_num = [i for i in range(0, len(crypto_sig_ansam))]

    print("\nPFAK CRYPTOGRAPHIC SIGNALS")
    pfak_stat(crypto_sig_ansam)
    # the commented part will have the same output(Result) as the function above
    # (use that to keepy DRY)
    # asnsam_pfak_list = modules.arr_procedures.auto_corel_all(crypto_sig_ansam, "PFAK")
    # cal.printFullStat(asnsam_pfak_list, 1, p - 1, True, sig_num)
    # cal.printFullStat(asnsam_pfak_list, 1, p - 1, list_of_num=sig_num)

    # Pairs of signal combinations (used only for output in printFullStat)
    # pair_list_cryptosig = cal.getPair([i for i in range(0, len(crypto_sig_ansam))])
    print("\nPFVK CRYPTOGRAPHIC SIGNALS")
    pfvk_stat(crypto_sig_ansam)
    # the commented part will have the same output(Result) as the function above
    # pfvk_cryptosig_list = modules.arr_procedures.cross_corel_btwn_pairs(crypto_sig_ansam, "PFVK")
    # cal.printFullStat(pfvk_cryptosig_list, 0, p, True, list_of_num=pair_list_cryptosig)
    # cal.printFullStat(pfvk_cryptosig_list, 0, p, list_of_num=pair_list_cryptosig)

    #derivative
    dersig, combinations = derivativeSigFromTo(crypto_sig_ansam, hadamar_sig_list,1,3)
    for i in range(0,len(dersig)):

        print("CS#{0} and HADAMAR#{1}".format(combinations[i][0],combinations[i][1]))
        print(dersig[i])

    pair_list_derivative = cal.getPair([i for i in range(0, len(dersig))])


    print("\nPFVK DERIVATIVE SIGNALS")
    pfvk_stat(dersig)
    # the commented part will have the same output(Result) as the function above
    # pfvk_corel_list = modules.arr_procedures.cross_corel_btwn_pairs2(dersig, pair_list_derivative, "PFVK")
    # cal.printFullStat(pfvk_corel_list, 0, p, True, pair_list_derivative)
    # cal.printFullStat(pfvk_corel_list, 0, p, False, pair_list_derivative)