import inspect

from logstream import Entry, entries, errors, first, parse_line, read_file, slowest, status_counts

LINES = [
    "GET /courses 200 12",
    "garbage",
    "POST /enroll 201 40",
    "GET /courses 500 300",
    "GET /x abc 5",
    "GET /pay 503 120",
]


def test_parse_line():
    assert parse_line("GET /a 200 7") == Entry("GET", "/a", 200, 7)
    assert parse_line("nonsense") is None
    assert parse_line("GET /a x 7") is None


def test_entries_skips_bad_lines():
    assert [e.path for e in entries(LINES)] == ["/courses", "/enroll", "/courses", "/pay"]


def test_entries_is_lazy():
    assert inspect.isgenerator(entries(LINES))

    def endless():
        while True:
            yield "GET /a 200 1"

    assert len(first(entries(endless()), 5)) == 5        # works on an endless stream


def test_errors_and_slowest():
    assert [e.status for e in errors(entries(LINES))] == [500, 503]
    assert [e.ms for e in slowest(entries(LINES), 2)] == [300, 120]


def test_status_counts():
    assert dict(status_counts(entries(LINES))) == {200: 2, 500: 2}


def test_read_file(tmp_path):
    f = tmp_path / "access.log"
    f.write_text("\n".join(LINES) + "\n")
    assert len(list(entries(read_file(f)))) == 4
