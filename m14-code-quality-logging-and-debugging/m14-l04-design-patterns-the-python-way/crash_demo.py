from events import OrderEvents
from listeners import count_sale, send_receipt, send_sms

events = OrderEvents()
events.subscribe(send_receipt)
events.subscribe(send_sms)
events.subscribe(count_sale)
events.publish("Lukas", 590)
