from modules import calculations as cal
from scipy.linalg import hadamard
from classes.CryptoSignal import CryptoSignal
from modules.arr_procedures import derivativeSigALL
from modules.arr_procedures import print_sig_in_list
from modules.arr_procedures import writeListInFile


class Hadamar:

    def __init__(self, N):
        if N <= 0:
            raise Exception("N can't be less or equal to 0")
        self.__N = N
        self.__hadam_list = hadamard(self.__N)

    # setting size of hamadamar matrix
    def setN(self, N):
        self.__N = N
        self.__hadam_list = hadamard(self.__N)

    # getter for hadamar matrix
    def getHadamMatrix(self):
        return self.__hadam_list


if __name__ == "__main__":
    p = 256
    h = Hadamar(p)
    cs = CryptoSignal(p)
    hadamar_sig_list = h.getHadamMatrix()


    crypto_sig_ansam = cs.genereteAnsambleOfCryptoSig(10, 32)

    # printing hadamar signals
    print("HADAMAR")
    print(hadamar_sig_list)
    # for i in range(0, len(hadamar_sig_list)):
    #   print(i + 1, ") ", list(hadamar_sig_list[i]))

    # printing generated cryptographic signals
    print("\nCRYPTOSIG")
    print_sig_in_list(crypto_sig_ansam)

    # counting numbers of cryptographic signals
    sig_num = [i for i in range(0, len(crypto_sig_ansam))]

    print("\nPFAK CRYPTOGRAPHIC SIGNALS")
    asnsam_pfak_list = cal.auto_corel_all(crypto_sig_ansam, "PFAK")
    cal.printFullStat(asnsam_pfak_list, 1, p - 1, True, sig_num)
    cal.printFullStat(asnsam_pfak_list, 1, p - 1, list_of_num=sig_num)

    pair_list_cryptosig = cal.getPair([i for i in range(0, len(crypto_sig_ansam))])
    print("\nPFVK CRYPTOGRAPHIC SIGNALS")
    pfvk_cryptosig_list = cal.cross_corel_btwn_pairs(crypto_sig_ansam, "PFVK")
    cal.printFullStat(pfvk_cryptosig_list, 0, p, True, list_of_num=pair_list_cryptosig )
    cal.printFullStat(pfvk_cryptosig_list, 0, p, list_of_num=pair_list_cryptosig)


    dersig, combinations = derivativeSigALL(crypto_sig_ansam, hadamar_sig_list)
    # print(dersig)
    print(combinations)

    pair_list_derivative = cal.getPair([i for i in range(0,len(dersig))])
    #print(pair_list)

    print("\nPFVK DERIVATIVE SIGNALS")
    pfvk_corel_list = cal.cross_corel_btwn_pairs2(dersig,pair_list_derivative[0:10],"PFVK")
    cal.printFullStat(pfvk_corel_list, 0, p, True, pair_list_derivative[0:10])
    cal.printFullStat(pfvk_corel_list, 0, p, False,pair_list_derivative[0:10])


    writeListInFile(crypto_sig_ansam,"cryptosignals"+str(p)+".txt")
    writeListInFile(hadamar_sig_list, "hadamar"+str(p)+".txt")
    writeListInFile(dersig, "../derivative_signals.txt")
