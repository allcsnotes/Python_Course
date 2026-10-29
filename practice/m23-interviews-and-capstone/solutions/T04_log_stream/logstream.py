"""Task 4 - analyse a huge log file lazily with generators."""
import heapq
from collections import Counter
from dataclasses import dataclass
from itertools import islice


@dataclass(frozen=True)
class Entry:
    method: str
    path: str
    status: int
    ms: int


def parse_line(line: str) -> Entry | None:
    """'GET /courses 200 12' -> Entry, or None for a broken line."""
    parts = line.split()
    if len(parts) != 4:
        return None
    method, path, status, ms = parts
    if not (status.isdigit() and ms.isdigit()):
        return None
    return Entry(method, path, int(status), int(ms))


def entries(lines):
    """Lazy: yields one Entry at a time, silently skipping bad lines."""
    for line in lines:
        entry = parse_line(line)
        if entry is not None:
            yield entry


def errors(stream):
    return (e for e in stream if e.status >= 500)


def slowest(stream, n=3):
    """Top n slowest entries without keeping the whole stream in memory."""
    return heapq.nlargest(n, stream, key=lambda e: e.ms)


def status_counts(stream):
    return Counter(e.status // 100 * 100 for e in stream)


def read_file(path):
    with open(path) as handle:
        yield from handle               # one line at a time


def first(stream, n):
    return list(islice(stream, n))
