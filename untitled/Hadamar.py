import calculations as cal
from scipy.linalg import hadamard
from CryptoSignal import CryptoSignal
from arr_procedures import derivativeSig, derivativeSig2
from arr_procedures import print_sig_in_list

class Hadamar:

    def __init__(self, N):
        if N <= 0:
            raise Exception("N can't be less or equal to 0")
        self.__N = N
        self.__hadam_list = hadamard(self.__N)

    def setN(self, N):
        self.__N = N
        self.__hadam_list = hadamard(self.__N)

    def getHadamMatrix(self):
        return self.__hadam_list

if __name__ == "__main__":
    p = 256
    h = Hadamar(p)
    cs = CryptoSignal(p)
    hadamar_sig_list = h.getHadamMatrix()
    #a =[[1,2,3,4],[3,2,1,7],[1,2,0,1],[1,2,3,4]]
    crypto_sig_ansam = cs.genereteAnsambleOfCryptoSig(256,32)


    print("HADAMAR")
    for i in range(0, len(hadamar_sig_list)):
        print(i+1,") ",list(hadamar_sig_list[i]))

    print("CRYPTOSIG")
    print_sig_in_list(crypto_sig_ansam)
    sig_num = [i for i in range(0,p)]
    asnsam_pfak_list = cal.auto_corel_all(crypto_sig_ansam, "PFAK")
    cal.printFullStat(asnsam_pfak_list, 1, p-1, True, sig_num)
    cal.printFullStat(asnsam_pfak_list, 1, p-1, sig_num)





    dersig = derivativeSig2(hadamar_sig_list,crypto_sig_ansam)
    print(dersig)