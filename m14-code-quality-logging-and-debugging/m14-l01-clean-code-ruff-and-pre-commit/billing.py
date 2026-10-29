import os, sys
from math import *

def calc(l, c, t=18, seen=[]):
    s = 0
    for x in l:
        s = s + x[1]*x[2]
    d = 0
    if c != None:
        if c == 'SAVE10': d = s*10/100
        if c == "FLAT200": d = 200
    unused = s
    return round((s-d) + (s-d)*t/100)
