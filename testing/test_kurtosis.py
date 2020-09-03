from scipy.stats import kurtosis
from scipy.stats import moment

import modules.arr_procedures
from classes.Hadamar import Hadamar
import numpy as np
from modules import calculations as cal

import math


if __name__=="__main__":
    p = 64
    h = Hadamar(p)
    hadamar_sig_list = h.getHadamMatrix()
    for i in range(p-50,p):
        print(i,") ",hadamar_sig_list[i].tolist())

    hadamar_pfvk_list = modules.arr_procedures.cross_corel_btwn_pairs(hadamar_sig_list[p - 10:p].tolist(), "PFVK")

    cal.printFullStat(hadamar_pfvk_list,0,p)
    cal.printFullStat(hadamar_pfvk_list, 0, p,True)




    # calculation with formula
    a =[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

    print(kurtosis(a)/math.sqrt(p))



    moment4 = moment(a,moment=4)
    print("Moment4 = ",moment4)
    var = np.var(a)
    print("D^2 = ",var)
    print("D^4 = ",var*var)
    res =( moment4/(var*var)) - 3
    print ("Moment4/ D^4 - 3  =", res)

    exit()






