import calculations as cl
import  numpy as np

if __name__=="__main__":
    a = [[2,2,2],[3,3,3],[4,4,4]]
    b = [[-1,1,1],[-1,-1,-1],[1,-1,1]]
    print(np.multiply(a,b))
    res =  []


    for i in a:
        for j in b:
           res.append(np.multiply(i,j).tolist())
    print(res)