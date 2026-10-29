import time


def measure(name, job):
    wall_start = time.perf_counter()
    cpu_start = time.process_time()
    job()
    wall = time.perf_counter() - wall_start
    cpu = time.process_time() - cpu_start
    busy = cpu / wall * 100
    print(f"{name}: wall {wall:.2f} s, cpu {cpu:.2f} s, busy {busy:.0f}%")
