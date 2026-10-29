import os, sys
from math import *

def invoice_total(items, coupon, gst_percent=18, seen=[]):
    subtotal = 0
    for item in items:
        subtotal = subtotal + item[1]*item[2]
    discount = 0
    if coupon != None:
        if coupon == 'SAVE10': discount = subtotal*10/100
        if coupon == "FLAT200": discount = 200
    unused = subtotal
    return round((subtotal-discount) + (subtotal-discount)*gst_percent/100)
