import calculations as cl


if __name__=="__main__":
    n = 761
    a = cl.prim_roots(n)
    print(a[0])
    print("Smallest primitive root of",
          n, "is", cl.findPrimitive(n))
