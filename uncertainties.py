import math
POGSON_RATIO = -2.5

def e_dist(d, plx, e_plx):
    return -d * (e_plx/plx)

def e_AbsMag(appMag, e_appMag, dist, e_dist):
    return e_appMag + (5 * 0.434 * (e_dist/dist))

def e_BM(e_AM):
    return e_AM

def e_L(L,e_BM):
    return L * 2.303 * (e_BM/POGSON_RATIO)

def e_Inner(e_L, L, I):
    return (I/2) * (e_L/(1.1 * L))

def e_Outer(e_L, L, O):
    return (O/2) * (e_L/(0.53 * L))