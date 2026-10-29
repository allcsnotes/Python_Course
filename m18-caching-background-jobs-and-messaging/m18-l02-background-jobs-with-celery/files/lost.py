import subprocess
import time

import httpx

cmd = ["uvicorn", "lost_app:app", "--port", "8182"]
log = open("lost.log", "w")
server = subprocess.Popen(cmd, stdout=log, stderr=log)
time.sleep(2)

url = "http://localhost:8182/enrol"
email = {"email": "lukas@example.com"}
reply = httpx.post(url, params=email)
print("reply:", reply.status_code, reply.json())

time.sleep(0.5)
server.kill()  # a crash, or a restart in a deploy
time.sleep(3)
text = open("lost.log").read()
print("email lines:", text.count("email sent"))
