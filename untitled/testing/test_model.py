import math
import random
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import scipy.special as special

class TestModel:
    def __init__(self, f_zero, V, Pw, k):
        # Исходные данные
        self.__f_zero = f_zero
        self.__w_zero = 2 * np.pi * f_zero
        self.__V = V
        self.__T = 1 / V
        self.__Pw = Pw
        self.__k = k

        # Вычисление длины ребра сигнальной рештки на основе ее структуры и заданого бюджета Pw
        self.__a = np.sqrt((8 / 5) * Pw)

    @property
    def f_zero(self):
        return self.__f_zero

    @f_zero.setter
    def f_zero(self, f_zero):
        self.__f_zero = f_zero
        self.__w_zero = 2 * np.pi * f_zero

    @property
    def V(self):
        return self.__V

    @V.setter
    def V(self, V):
        self.__V = V
        self.__T = 1 / V

    @property
    def Pw(self):
        return self.__Pw

    @Pw.setter
    def Pw(self, Pw):
        self.__Pw = Pw
        self.__a = np.sqrt((8 / 5) * Pw)

    @property
    def k(self):
        return self.__k

    @k.setter
    def k(self, k):
        self.__k = k

    @property
    def a(self):
        return self.__a

    def getX(self):
        return np.floor(np.random.randint(0, np.power(2, self.__k) - 1))

    def calculate_stat_wo_Grey(self, N, M):
        # выибраем случайное сообщение от 0 до 2^k - 1
        x = self.getX()
        H = np.floor(x / math.pow(2, 2))
        L = x % np.power(2, 2)

        t = 100
        print(t)
        s_t = self.calculate_St(H,L,t)
        print(s_t)



    def get_S_t_function(self, t,H, L):
        #x = np.arange(t)
        #y = (self.__a * ((3 / 2) - H) * np.sin(self.__w_zero * x)) - (self.__a * ((3 / 2) - L) * np.cos(self.__w_zero * x))
        #plt.plot(x,y)
        #plt.show()

        return (self.__a * ((3 / 2) - H) * np.sin(self.__w_zero * t)) - (self.__a * ((3 / 2) - L) * np.cos(self.__w_zero * t))

    def get_r_norm(self,mu,sigma):
        return np.random.normal(mu,sigma,9)





if __name__ == "__main__":
    test = TestModel(1, 1, 1, 4)
    sample = 10

    x = test.getX()
    H = np.floor(x / math.pow(2, 2))
    L = x % np.power(2, 2)
    N = 10
    M = 20

    #интеграл
    s_t = lambda t:(test.a * ((3 / 2) - H) * np.sin(test.f_zero*2*np.pi * t)) \
                   - (test.a * ((3 / 2) - L) * np.cos(test.f_zero*2*np.pi  * t))
    i = integrate.quad(s_t, 0, 1)
    print(i)


    #for S_N in range(1,N):
    #        N_zero = 1/S_N
     #   for i in range(0,M-1):
      #      r = test.get_r_norm(0,np.sqrt())

