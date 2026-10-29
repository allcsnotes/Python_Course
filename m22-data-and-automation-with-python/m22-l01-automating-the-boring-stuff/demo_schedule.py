import time

import schedule


def job():
    print("report runs at", time.strftime("%H:%M:%S"))


schedule.every(4).seconds.do(job)
schedule.every().monday.at("08:00").do(job)
for line in schedule.get_jobs():
    print(line)

while True:
    schedule.run_pending()
    time.sleep(1)
