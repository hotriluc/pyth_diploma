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
    def P(self,p):
        if p <= 0:
            raise Exception("P can't be less or equal to 0")
        self.P = p



    def generateRandomSeq(self):
        secrets_generator = secrets.SystemRandom()
        signal = list()
        for i in range(0,self.__P):
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
            #Getting PFAK
            corel_list = cal.getCorellation(sig,sig)
            rmax = cal.getMax(corel_list,1,self.__P-1,True)
            if rmax[0]<=if_rmax:
                return sig
                break
            else:
                print("trying to generate another")


    #стоит некий счетчик и после 100 попыток если не удалось найти сигнал с заданной кореляцией
    #значение за которым отбирается увеличивается на 1
    def generateDefRandomSeq2(self, if_rmax):
        counter = 0
        while True:
            if counter>=100:
                counter=0
                if_rmax+=1

            sig = self.generateRandomSeq()
            #Getting PFAK
            corel_list = cal.getCorellation(sig,sig)
            rmax = cal.getMax(corel_list,1,self.__P-1,True)
            if rmax[0]<=if_rmax:
                return sig
                break
            else:
                counter+=1



if __name__=="__main__":
    cs = CryptoSignal(16)
    sig1 = cs.generateRandomSeq()
    print(sig1)
    print(cal.getCorellation(sig1,sig1,True))


    #pfak rmax = 4 L =16
    sig2 = cs.generateDefRandomSeq(4)
    print(sig2)
    print(cal.getCorellation(sig2, sig2))


    sig3 = cs.generateDefRandomSeq2(2)
    print(sig3)
    print(cal.getCorellation(sig3, sig3))