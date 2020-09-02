import modules.arr_procedures
from modules import arr_procedures as ap, calculations as cal
from classes.CDS import CDS
from classes.Hadamar import Hadamar

if  __name__=="__main__":
    # only for 256
    p = 257;

    # Creating object CDS
    c = CDS(p)
    # Print General Info
    print("P = {0}\nL = {1}".format(p, p - 1))
    print("ϕ({0}) = {1}".format(p - 1, cal.coprimes(p - 1)))
    print(("ϴmin = {0}".format(cal.findPrimitive(p))))
    ap.print_2d_arr(c.table)


    # decimated signals and coef
    decimation_signals = c.getDecimation()

    h = Hadamar(p - 1)
    hadamar_sig_list = h.getHadamMatrix()

    # Decimated signals without first sig(because its the same as source)
    b = list()
    for item in decimation_signals:
        # we only need signals so use 0th pos
        b.append(item[0])
    b.pop(0)

    # cal.printPair(d)

    #print("\nDecimation: ", decimation_signals)


    print("\nCDS")
    ap.print_sig_in_list(b[0:5])


    slice_of_b = b[0:5]
    # Подсчт пар
    pair_list_cryptosig = cal.getPair([i for i in range(0, len(slice_of_b))])
    print("\nPFVK CDS SIGNALS")
    # pfvk_cryptosig_list = cal.cross_corel_btwn_pairs(slice_of_b, "PFVK")
    # cal.printFullStat(pfvk_cryptosig_list, 0, p, True, list_of_num=pair_list_cryptosig)
    # cal.printFullStat(pfvk_cryptosig_list, 0, p, list_of_num=pair_list_cryptosig)
    pfvk_stat = modules.arr_procedures.ansamble_correlation('PFVK')
    pfvk_stat(slice_of_b)

    # derivative
    dersig, combinations = ap.derivativeSigFromTo(slice_of_b, hadamar_sig_list, 1, 3)
    for i in range(0, len(dersig)):
        print("CDS#{0} and HADAMAR#{1}".format(combinations[i][0], combinations[i][1]))
        print(dersig[i])


    print("\nPFVK DERIVATIVE SIGNALS")
    # pair_list_derivative = cal.getPair([i for i in range(0, len(dersig))])
    # pfvk_corel_list = cal.cross_corel_btwn_pairs2(dersig, pair_list_derivative, "PFVK")
    # cal.printFullStat(pfvk_corel_list, 0, p, True, pair_list_derivative)
    # cal.printFullStat(pfvk_corel_list, 0, p, False, pair_list_derivative)
    pfvk_stat(dersig)


