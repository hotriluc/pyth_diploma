from Hadamar import Hadamar
from CryptoSignal import CryptoSignal
from arr_procedures import print_sig_in_list,derivativeSigALL,derivativeSigFromTo
import calculations as cal

if __name__ =="__main__":

    p = 256
    h = Hadamar(p)
    cs = CryptoSignal(p)

    # 2048 pfak 140
    # 256 pfak 32
    # 16 pfak 4
    hadamar_sig_list = h.getHadamMatrix()
    crypto_sig_ansam = cs.genereteAnsambleOfCryptoSig(5, 32)

    # for i in range(0, len(hadamar_sig_list)):
    #    print(i + 1, ") ", list(hadamar_sig_list[i]))

    print("\nCRYPTOSIG")
    print_sig_in_list(crypto_sig_ansam)

    sig_num = [i for i in range(0, len(crypto_sig_ansam))]

    print("\nPFAK CRYPTOGRAPHIC SIGNALS")
    asnsam_pfak_list = cal.auto_corel_all(crypto_sig_ansam, "PFAK")
    cal.printFullStat(asnsam_pfak_list, 1, p - 1, True, sig_num)
    cal.printFullStat(asnsam_pfak_list, 1, p - 1, list_of_num=sig_num)

    pair_list_cryptosig = cal.getPair([i for i in range(0, len(crypto_sig_ansam))])
    print("\nPFVK CRYPTOGRAPHIC SIGNALS")
    pfvk_cryptosig_list = cal.cross_corel_btwn_pairs(crypto_sig_ansam, "PFVK")
    cal.printFullStat(pfvk_cryptosig_list, 0, p, True, list_of_num=pair_list_cryptosig)
    cal.printFullStat(pfvk_cryptosig_list, 0, p, list_of_num=pair_list_cryptosig)

    dersig, combinations = derivativeSigFromTo(crypto_sig_ansam, hadamar_sig_list,1,3)
    for i in range(0,len(dersig)):
        print("CS#{0} and HADAMAR#{1}".format(combinations[i][0],combinations[i][1]))
        print(dersig[i])

    pair_list_derivative = cal.getPair([i for i in range(0, len(dersig))])
    print("\nPFVK DERIVATIVE SIGNALS")
    pfvk_corel_list = cal.cross_corel_btwn_pairs2(dersig, pair_list_derivative, "PFVK")
    cal.printFullStat(pfvk_corel_list, 0, p, True, pair_list_derivative)
    cal.printFullStat(pfvk_corel_list, 0, p, False, pair_list_derivative)