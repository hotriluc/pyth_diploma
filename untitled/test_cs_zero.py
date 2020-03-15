
from CryptoSignal import CryptoSignal
from arr_procedures import print_sig_in_list,derivativeSigALL,derivativeSigFromTo
import calculations as cal
import Plot

if __name__=="__main__":
    p = 1024
    cs = CryptoSignal(p)

    # 2048 pfak 140
    # 256 pfak 32
    # 16 pfak 4
    # 1024 81pfak
    crypto_sig_ansam = cs.genereteAnsambleOfCryptoSig(3, 81)

    print("\nPFAK CRYPTOGRAPHIC SIGNALS")
    ansam_pfak_list = cal.auto_corel_all(crypto_sig_ansam, "PFAK")

    for i in range(0, len(crypto_sig_ansam)):
         print(i+1, ")", crypto_sig_ansam[i])
         print("PFAK: ", ansam_pfak_list[i])
         #Plot.build_plotly(ansam_pfak_list[i], "ПФАК КС №{0} L = {1}".format(i+1, p))
