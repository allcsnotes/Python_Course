# First version of Asha's change: append this to the end of tests/test_filesize.py


def test_naturalsize_zero() -> None:
    assert humanize.naturalsize(0) == "0 Bytes"
    assert humanize.naturalsize(0, binary=True) == "0 Bytes"
    assert humanize.naturalsize(0, gnu=True) == "0B"
