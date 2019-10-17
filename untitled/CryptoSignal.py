import secrets
import calculations as cal


class CryptoSignal:

    def __init__(self, p):
        if p <= 0:
            raise Exception("P can't be less or equal to 0")
        self.__P = p

    @property
    def P(self):
        return self.__p

    @P.setter
    def P(self, p):
        if p <= 0:
            raise Exception("P can't be less or equal to 0")
        self.P = p

    def generateRandomSeq(self):
        secrets_generator = secrets.SystemRandom()
        signal = list()
        for i in range(0, self.__P):
            random_number = secrets_generator.randint(0, 1)
            if random_number == 0:
                random_number = -1
                signal.append(random_number)
            else:
                signal.append(random_number)
        return signal

    def generateDefRandomSeq(self, if_rmax):

        while True:
            sig = self.generateRandomSeq()
            # Getting PFAK
            corel_list = cal.getCorellation(sig, sig)
            rmax = cal.getMax(corel_list, 1, self.__P - 1, True)
            if rmax[0] <= if_rmax:
                return sig
                break
            # else:
            #    print("trying to generate another")

    # стоит некий счетчик и после 100 попыток если не удалось найти сигнал с заданной кореляцией
    # значение за которым отбирается увеличивается на 1
    def generateDefRandomSeq2(self, if_rmax):
        counter = 0
        while True:
            if counter >= 100:
                counter = 0
                if_rmax += 1

            sig = self.generateRandomSeq()
            # Getting PFAK
            corel_list = cal.getCorellation(sig, sig)
            rmax = cal.getMax(corel_list, 1, self.__P - 1, True)
            if rmax[0] <= if_rmax:
                print(if_rmax)
                return sig
                break
            else:
                counter += 1

    def genereteAnsambleOfCryptoSig(self, n, ifrmax):
        tmp_list = []
        for i in range(0, n):
            tmp_list.append(self.generateDefRandomSeq(ifrmax))
        return tmp_list


if __name__ == "__main__":
    p=2048
    cs = CryptoSignal(p)
    # sig1 = cs.generateRandomSeq()
    # print(sig1)
    # print("AFAK",cal.getCorellation(sig1,sig1,True))

    # pfak rmax = 4 L =16
    # sig2 = cs.generateDefRandomSeq(4)
    # print(sig2)
    # print("PFAK",cal.getCorellation(sig2, sig2))

    # sig3 = cs.generateDefRandomSeq2(2)
    # print(sig3)
    # print("PFAK",cal.getCorellation(sig3, sig3))

    # generete asnsamble of signals with defined Rmax
    ansam = cs.genereteAnsambleOfCryptoSig(5, 140)
    print(ansam)

    # getting all pfaks
    asnsam_pfak_list = cal.cross_corel_btwn_pairs(ansam, "PFVK")
    # calculate stat for pfaks
    cal.printFullStat(asnsam_pfak_list, 0, p, True)
    cal.printFullStat(asnsam_pfak_list, 0, p)

    # for sig in ansam:
    #  print(sig)
    #  pfak_list = cal.getCorellation(sig,sig)
    #   print("PFAK",pfak_list)
    #   cal.printFullStat(pfak_list,1,255,True)
