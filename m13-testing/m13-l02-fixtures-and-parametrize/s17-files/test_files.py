import pytest

from roster import announce, load_roster, save_roster


def test_roster_round_trip(course, tmp_path):
    course.enroll("Lukas")
    course.enroll("Priya")
    path = save_roster(course, tmp_path)
    assert path.read_text() == "Lukas\nPriya"
    assert load_roster(path) == ["Lukas", "Priya"]


def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_roster(tmp_path / "nope.txt")


def test_announce(course, capsys):
    course.enroll("Lukas")
    announce(course)
    out = capsys.readouterr().out
    assert out == "Python Basics: 1 of 2 seats taken\n"
