import logging

logging.basicConfig(format="%(name)s: %(message)s")
shop = logging.getLogger("shop")
pay = logging.getLogger("shop.payments")

shop.setLevel(logging.ERROR)
pay.warning("child warning")
shop.error("parent error")
