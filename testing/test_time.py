import time
from classes.CryptoSignal import CryptoSignal
from modules.arr_procedures import getDecimation


def test_time_ensemble():
    cs = CryptoSignal(256)
    time_list = list()
    for i in range(0, 10):
        start_time = time.process_time()
        cs_ensemble = cs.genereteAnsambleOfCryptoSig(128, 32)
        time_list.append(time.process_time() - start_time)
        print("{0:5f} seconds".format(time.process_time()-start_time))

    return time_list

# time for cs generaton excluded
def test_time_decimation():
    time_list = list()
    for i in range(0,10):
        sig = cs.generateDefRandomSeq(32)
        start_time = time.process_time()
        decimations = getDecimation(sig)
        time_list.append(time.process_time()-start_time)
        print("{0:5f} seconds".format(time.process_time()-start_time))

# time for cs generaton included
def test_time_decimation2():
    cs = CryptoSignal(256)
    time_list = list()

    for i in range(0, 10):

        start_time = time.process_time()
        sig = cs.generateDefRandomSeq(32)
        decimations = getDecimation(sig)
        time_list.append(time.process_time() - start_time)
        print("{0:5f} seconds".format(time.process_time() - start_time))

if __name__=='__main__':
    cs = CryptoSignal(256)
    time_list = list()

    for i in range(0, 10):

        start_time = time.process_time()
        sig = cs.generateDefRandomSeq(32)
        decimations = getDecimation(sig)
        time_list.append(time.process_time() - start_time)
        print("{0:5f} seconds".format(time.process_time() - start_time))
