import asyncio
import statistics
import time

import httpx

TARGETS = {
    "cache on": "http://localhost:8691",
    "cache off": "http://localhost:8791",
}
ROUNDS = 7
TOTAL = 3000
WORKERS = 50


async def misses(client):
    reply = await client.get("/cache/stats")
    return reply.json()["misses"]


async def one_round(client, path):
    times = []

    async def worker(count):
        for _ in range(count):
            start = time.perf_counter()
            await client.get(path, follow_redirects=False)
            times.append(time.perf_counter() - start)

    begin = time.perf_counter()
    jobs = [worker(TOTAL // WORKERS) for _ in range(WORKERS)]
    await asyncio.gather(*jobs)
    seconds = time.perf_counter() - begin
    return len(times) / seconds, sorted(times)


async def main():
    body = {"url": "https://allcsvideos.com/courses/git"}
    clients, paths, before, rounds = {}, {}, {}, {}
    for name, url in TARGETS.items():
        clients[name] = httpx.AsyncClient(base_url=url)
        reply = await clients[name].post("/links", json=body)
        paths[name] = "/" + reply.json()["code"]
        before[name] = await misses(clients[name])
        rounds[name] = []
    for _ in range(ROUNDS):
        for name, client in clients.items():
            found = await one_round(client, paths[name])
            rounds[name].append(found)
    print(f"best of {ROUNDS} rounds, {TOTAL} requests each")
    print(
        "           per second  median  slowest 5%  Postgres"
    )
    for name, client in clients.items():
        asked = await misses(client) - before[name]
        speed, times = max(rounds[name], key=lambda r: r[0])
        median = statistics.median(times) * 1000
        slow = times[int(len(times) * 0.95)] * 1000
        print(
            f"{name:<10}{speed:>10.0f}{median:>7.0f} ms"
            f"{slow:>8.0f} ms{asked:>12}"
        )


asyncio.run(main())
