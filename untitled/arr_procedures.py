import itertools
import pickle
import numpy as np

# write string
def writeListInFile(aList:list,filepath):
    f = open(filepath,"w")
    for i in range(0,len(aList)):
        f.write(str(i)+") "+str(aList[i])+"\n")

    f.close()

# write binary mode
def writeListInBinFile(aList:list,file_name):
    with open(file_name, 'wb') as F:
        # Dump the list to file
        pickle.dump(aList, F)
    F.close()

def loadFromBinFile(file_name):
    with open(file_name, 'rb') as F:
        aList = pickle.load(F)
    F.close()
    return aList


def print_2d_arr(aList):
    for row in aList:
        for item in row:
            print("{0:5d}".format(item), end="")
        print("")


# print list of list(signals)
def print_sig_in_list(aList):
    i = 0
    for item in aList:
        print(i, ") ", item)
        i += 1


# using simple pop and insert we created Shifting list with zeroing
def ShiftRight(aList: list, steps: int):
    # for negative steps
    if steps < 0:
        steps = abs(steps)
        for i in range(steps):
            # pop first element
            # everything is shifted to the left after we pop
            aList.pop(0)
            # adding to the end 0
            aList.append(0)
    else:
        for i in range(steps):
            # insert zero to the 0 position
            aList.insert(0, 0)
            # poping last el
            # everything is shifted to right
            aList.pop()


def CyclicShiftRight(aList: list, steps: int):
    # for negative steps
    if steps < 0:
        steps = abs(steps)
        for i in range(steps):
            # adding to the end popped 0th el
            aList.append(aList.pop(0))
    else:
        for i in range(steps):
            # adding to the beginning popped(last) el
            aList.insert(0, aList.pop())


# def ShiftRight(aList:list,pos:int):
# return aList[pos:len(aList):]*0 + aList[0:pos:]

# for i in range(1,len(aList)-1):

# ansamles must contain same number of signals
# USING WITH HADAMAR DISCRETE SIGNALS in order to get derivative signals
def derivativeSig(ansamble_sig1: list, ansamble_sig2: list):
    der_sig_list = []
    for i in range(0, len(ansamble_sig1)):
        tmp = np.array(ansamble_sig1[i]) * np.array(ansamble_sig2[i])
        der_sig_list.append(tmp.tolist())

    return der_sig_list


def derivativeSigALL(ansamble_sig1: list, ansamble_sig2: list):
    der_sig_list = []

    sig_comb_list = []
    for i in range(0, len(ansamble_sig1)):
        for j in range(0, len(ansamble_sig2)):
            der_sig_list.append(np.multiply(ansamble_sig1[i], ansamble_sig2[j]).tolist())
            sig_comb_list.append((i, j))
    return der_sig_list, sig_comb_list

def derivativeSigFromTo(ansamble_sig1: list, hadamar_sig: list,hadam_from,hadam_to):
    der_sig_list = []
    sig_comb_list = []
    for i in range(0, len(ansamble_sig1)):
        for j in range(hadam_from, hadam_to):
            der_sig_list.append(np.multiply(ansamble_sig1[i], hadamar_sig[j]).tolist())
            sig_comb_list.append((i, j))
    return der_sig_list, sig_comb_list


if __name__ == "__main__":
    a = [1, 'b', 'c']
    b = [12, 2, 3, 4, 3, 4, 1, 4, 12]
    for pair in itertools.combinations(a, 2):
        print(pair)
