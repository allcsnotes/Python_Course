import cProfile
import pstats

import data
import stats

rows = data.make_rows(60000)
with cProfile.Profile() as profiler:
    stats.unique_students(rows)
    stats.total_revenue(rows)
report = pstats.Stats(profiler)
report.sort_stats("cumulative")
report.print_stats(3)
