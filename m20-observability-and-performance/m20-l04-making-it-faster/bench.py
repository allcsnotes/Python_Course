import statistics, sys, time, httpx
c = httpx.Client(base_url="http://localhost:8204")
tok = c.post("/auth/login", data={"username": "meera@example.com", "password": "meera-demo-pass"}).json()["access_token"]
h = {"Authorization": f"Bearer {tok}"}
c.get("/me/dashboard", headers=h)
ts = []
for _ in range(int(sys.argv[1]) if len(sys.argv) > 1 else 20):
    t = time.perf_counter(); r = c.get("/me/dashboard", headers=h); ts.append((time.perf_counter() - t) * 1000)
print(f"median {statistics.median(ts):.0f} ms  min {min(ts):.0f}  max {max(ts):.0f}  status {r.status_code}")
