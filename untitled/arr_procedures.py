import itertools

import numpy as np
def print_2d_arr(aList):

    for row in aList:
        for item in row:
            print("{0:5d}".format(item),end="")
        print("")

#using simple pop and insert we created Shifting list with zeroing
def ShiftRight(aList:list,steps:int):
        #for negative steps
        if steps < 0:
            steps = abs(steps)
            for i in range(steps):
                #pop first element
                #everything is shifted to the left after we pop
                aList.pop(0)
                #adding to the end 0
                aList.append(0)
        else:
            for i in range(steps):
                #insert zero to the 0 position
                aList.insert(0, 0)
                #poping last el
                #everything is shifted to right
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

#def ShiftRight(aList:list,pos:int):
   #return aList[pos:len(aList):]*0 + aList[0:pos:]

    #for i in range(1,len(aList)-1):




if __name__ == "__main__":
    a  = [1,'b','c']
    b = [12,2,3,4,3,4,1,4,12]
    for pair in itertools.combinations(a,2):
        print(pair)
