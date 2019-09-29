from scipy.linalg import hadamard


from CryptoSignal import CryptoSignal
import numpy as np
from arr_procedures import derivativeSig


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
    h = Hadamar(4)
    hadamar_sig_list = h.getHadamMatrix()
    a =[[1,2,3,4],[3,2,1,7],[1,2,0,1],[1,2,3,4]]

    print(hadamar_sig_list)
    print(a)

    print("=====")
    for i in range(0,len(hadamar_sig_list)):
        print(hadamar_sig_list[i]*a[i])

    print("=====")
    dersig = derivativeSig(hadamar_sig_list,a)
    print(dersig)