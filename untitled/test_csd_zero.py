import calculations as cal
import arr_procedures as ap
import copy
import Plot
from CDS import CDS

if __name__=="__main__":
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

    # Decimated signals without first sig(because its the same as source)
    b = list()
    for item in d:
        # we only need signals so use 0th pos
        b.append(item[0])
    b.pop(0)

    ansamble_of_pereodic_auto_corel_list = cal.corel_source_and_rest(sig1_, b, "PFAK")


    for i in range(1, 4):
        print(i, ")", b[i])
        print("PFAK: ", ansamble_of_pereodic_auto_corel_list[i])
        Plot.build_plotly(ansamble_of_pereodic_auto_corel_list[i],"ПФАК ХДС №{0} L = {1}".format(i,len(source_sig)))
