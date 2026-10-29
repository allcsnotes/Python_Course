from math import *

GST_PERCENT = 18

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

def invoice_total(items, coupon, gst_percent=GST_PERCENT):
    """Return the total in rupees: discount first, then GST."""
    subtotal = basket_subtotal(items)
    after_discount = subtotal - coupon_discount(subtotal, coupon)
    # GST is charged on the price after the discount, as the finance team wants.
    tax = after_discount*gst_percent/100
    return round(after_discount + tax)
