import os, sys
from math import *

def basket_subtotal(items):
    subtotal = 0
    for _, price, quantity in items:
        subtotal = subtotal + price*quantity
    return subtotal

def coupon_discount(subtotal, coupon):
    if coupon != None:
        if coupon == 'SAVE10': return subtotal*10/100
        if coupon == "FLAT200": return 200
    return 0

def invoice_total(items, coupon, gst_percent=18, seen=[]):
    subtotal = basket_subtotal(items)
    unused = subtotal
    after_discount = subtotal - coupon_discount(subtotal, coupon)
    return round(after_discount + after_discount*gst_percent/100)
