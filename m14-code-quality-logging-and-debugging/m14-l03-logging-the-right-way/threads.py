import logging
import threading

logging.basicConfig(
    level=logging.INFO,
    format="%(threadName)s: %(message)s",
)


def send_email(name):
    logging.info("emailing %s", name)


for name in ("Lukas", "Priya"):
    worker = threading.Thread(target=send_email, args=(name,))
    worker.start()
    worker.join()
