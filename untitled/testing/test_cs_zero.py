
from classes.CryptoSignal import CryptoSignal
from modules import calculations as cal, plot

if __name__=="__main__":
    p = 256;
    cs = CryptoSignal(p)
    # путем ручного тестирования первое число длина сигнала, второе оптимальный
    # минимальный пфак по которому будут отбирать
    # сигналы, при таком пфак возможно найти сигналы с 0 пиками вблизи центра,
    # если меньше установить ,то на поиски уйдет больше времени

    # 2048 pfak 140
    # 256 pfak 32
    # 16 pfak 4
    # 1024 81pfak
    crypto_sig_ansam = cs.genereteAnsambleOfCryptoSig_zero(3, 32)

    print("\nPFAK CRYPTOGRAPHIC SIGNALS")
    ansam_pfak_list = cal.auto_corel_all(crypto_sig_ansam, "PFAK")

    for i in range(0, len(crypto_sig_ansam)):
         print(i+1, ")", crypto_sig_ansam[i])
         print("PFAK: ", ansam_pfak_list[i])
         plot.build_plotly(ansam_pfak_list[i], "ПФАК КС №{0} L = {1}".format(i + 1, p))
