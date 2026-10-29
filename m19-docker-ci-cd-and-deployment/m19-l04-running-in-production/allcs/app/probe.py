import urllib.request

urllib.request.urlopen("http://localhost:8000/health/ready", timeout=1)
