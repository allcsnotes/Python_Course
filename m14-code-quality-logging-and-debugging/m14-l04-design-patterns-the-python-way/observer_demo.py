from events import OrderEvents
from listeners import count_sale, send_receipt

events = OrderEvents()
events.subscribe(send_receipt)
events.subscribe(count_sale)
events.publish("Lukas", 590)
