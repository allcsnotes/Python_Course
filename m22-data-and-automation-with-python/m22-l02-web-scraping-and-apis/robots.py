from urllib.robotparser import RobotFileParser

BASE = "http://localhost:22280"
rp = RobotFileParser(BASE + "/robots.txt")
rp.read()

for path in ["/courses", "/admin/students"]:
    print(path, rp.can_fetch("allcsv-bot", BASE + path))
print("delay:", rp.crawl_delay("allcsv-bot"))
