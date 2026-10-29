import csv
import sys

print(f"{'endpoint':<15} {'reqs':>5} {'P50':>5} {'P95':>6} {'P99':>6}")
for row in csv.DictReader(open(sys.argv[1])):
    name = row["Name"].replace("Aggregated", "all together")
    if name == "/auth/login":
        continue
    print(
        f"{name:<15} {row['Request Count']:>5} {row['50%']:>5} "
        f"{row['95%']:>6} {row['99%']:>6}"
    )
