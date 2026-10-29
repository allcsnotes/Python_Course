from discounts import DISCOUNTS
from events import OrderEvents
from listeners import count_sale, send_receipt
from payments import make_gateway
from shop import place_order

events = OrderEvents()
events.subscribe(send_receipt)
events.subscribe(count_sale)
receipt = place_order(
    "Lukas", 1000, DISCOUNTS["student"], make_gateway("upi"), events
)
print(receipt)
