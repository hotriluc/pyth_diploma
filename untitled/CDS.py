import math

import calculations as cal
import arr_procedures as ap
import copy
import Plot


class CDS:

    def __init__(self, p):
        self.__p = p
        self.__table = [[0 for j in range(p - 1)] for i in range(6)]
        self.fill_all_table()

    @property
    def table(self):
        return self.__table

    def getP(self):
        return self.__p

    # filling first row Ui of the table(_2darray)
    def fill_row_Ui(self):
        for i in range(0, self.__p - 1):
            self.__table[0][i] = i + 1

    # filling second row ai of the table(2darray) by using rule ai = θ^j mod P, j = 0.. P-1
    def fill_row_ai(self):
        # Getting Min Primative root of N(p)
        teta_min = cal.findPrimitive(self.__p)
        for i in range(0, self.__p - 1):
            b = i
            a = teta_min
            c = cal.power(a, b, self.__p)
            self.__table[1][i] = c

    # filling third row Ai of the table(2darray)
    def fill_row_Ai(self):
        tmp = 0
        position = 0
        for i in range(0, self.__p - 1):
            # choosing Ui element from first row
            tmp = self.__table[0][i]
            # each Ui corresponds to its own ai , saving ai as position for Ai
            position = self.__table[1][i]
            # adding Ui to saved position
            self.table[2][position - 1] = tmp

    # filling fourth row bi of the table(2darray)
    def fill_row_bi(self):
        tmp = 0
        for i in range(0, self.__p - 1):
            tmp = self.__table[1][i]
            self.__table[3][i] = (tmp + 1) % self.__p
            if self.table[3][i] == 0:
                self.table[3][i] = 1

    # filling fifth row MHi of the table(2darray)
    def fill_row_MH(self):
        pos1 = 0
        pos2 = 0
        tmp = 0
        for i in range(0, self.__p - 1):
            # saving bi as pos1
            pos1 = self.__table[3][i]
            for j in range(0, self.__p - 1):
                # looking for bi in Ui row
                if self.__table[0][j] == pos1:
                    # saving Ui as position for further appealing to Ai
                    pos2 = self.__table[0][j] - 1
                    # Getting A[Ui]
                    tmp = self.__table[2][pos2]
                    break
            self.__table[4][i] = tmp

    # filling 6th row Psi of the table(2darray) if even = 1 odd = -1
    def fill_row_Psi(self):
        for i in range(0, self.__p - 1):
            if self.__table[4][i] % 2 == 0:
                self.__table[5][i] = -1
            else:
                self.__table[5][i] = 1

    def fill_all_table(self):
        self.fill_row_Ui()
        self.fill_row_ai()
        self.fill_row_Ai()
        self.fill_row_bi()
        self.fill_row_MH()
        self.fill_row_Psi()

    def getDecimation(self):
        # Copy source signal
        sig1_ = copy.deepcopy(self.__table[5])
        decimation_list = list()
        coprime_list = cal.coprimes(self.__p - 1)[1]

        for i in range(len(coprime_list)):
            # tmp for signal we are going to get with decimation
            sig2_ = [0 for i in range(self.__p - 1)]

            # creating rest signals with decimation
            cal.decimation(sig1_, sig2_, coprime_list[i])

            # appending decimation_list with list
            # that contains decimated sig and
            # decimation cof that used to create that sig
            decimation_list.append([sig2_, coprime_list[i]])
        return decimation_list


if __name__ == "__main__":

    # input until its prime
    p = 0
    while True:
        p = int(input("Enter P:"))
        if cal.isPrime(p):
            print("Prime")
            break
        else:
            print("is not prime")

    # Creating object CDS
    c = CDS(p)
    # Print General Info
    print("P = {0}\nL = {1}".format(p, p - 1))
    print("ϕ({0}) = {1}".format(p - 1, cal.coprimes(p - 1)))
    print(("ϴmin = {0}".format(cal.findPrimitive(p))))
    ap.print_2d_arr(c.table)

    # decimated signals and coef
    d = c.getDecimation()

    # getting source signal from the table
    source_sig = c.table[5]

    sig1_ = copy.deepcopy(source_sig)
    sig2_ = copy.deepcopy(source_sig)

    print("PFAK")
    pereodic_auto_corel_list = cal.getCorellation(sig1_, sig2_)
    print("R = ", pereodic_auto_corel_list)
    print("Rmax = ", cal.getMax(pereodic_auto_corel_list, 1, p - 1, True))

    print("AFAK")
    apereodic_auto_corel_list = cal.getCorellation(sig1_, sig2_, True)
    print("R = ", apereodic_auto_corel_list)
    print("Rmax = ", cal.getMax(apereodic_auto_corel_list, 1, p - 1))

    # Plot.build_plot(pereodic_auto_corel_list, "PFAK")

    # Decimated signals without first sig(because its the same as source)
    b = list()
    for item in d:
        # we only need signals so use 0th pos
        b.append(item[0])
    b.pop(0)

    # cal.printPair(d)

    print("\nDecimation: ", d)

    ansamble_of_pereodic_cross_corel_list = cal.corel_source_and_rest(sig1_, b, "PFVK")
    print("\nPFVK")
    cal.printFullStat(ansamble_of_pereodic_cross_corel_list, 0, p, True)
    cal.printFullStat(ansamble_of_pereodic_cross_corel_list, 0, p)

    ansamble_of_apereodic_cross_corel_list = cal.corel_source_and_rest(sig1_, b, "AFVK")
    print("\nAFVK")
    cal.printFullStat(ansamble_of_apereodic_cross_corel_list, 0, p, True)
    cal.printFullStat(ansamble_of_apereodic_cross_corel_list, 0, p)

    ansamble_of_pereodic_auto_corel_list = cal.corel_source_and_rest(sig1_, b, "PFAK")
    print("\nPFAK")
    cal.printFullStat(ansamble_of_pereodic_auto_corel_list, 1, p-1, True)
    cal.printFullStat(ansamble_of_pereodic_auto_corel_list, 1, p-1)

    ansamble_of_apereodic_auto_corel_list = cal.corel_source_and_rest(sig1_, b, "AFAK")
    print("\nAFAK")
    cal.printFullStat(ansamble_of_apereodic_auto_corel_list, 1, p-1, True)
    cal.printFullStat(ansamble_of_apereodic_auto_corel_list, 1, p-1)
