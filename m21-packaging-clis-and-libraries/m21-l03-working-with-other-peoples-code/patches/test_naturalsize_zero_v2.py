# Second version, after Meera's review: replace the first version at the end of
# tests/test_filesize.py with this one (it needs "import pytest", which the file already has).


@pytest.mark.parametrize(
    "test_args, expected",
    [
        ([0], "0 Bytes"),
        ([0, True], "0 Bytes"),
        ([0, False, True], "0B"),
    ],
)
def test_naturalsize_zero(test_args: list[int | bool], expected: str) -> None:
    assert humanize.naturalsize(*test_args) == expected
