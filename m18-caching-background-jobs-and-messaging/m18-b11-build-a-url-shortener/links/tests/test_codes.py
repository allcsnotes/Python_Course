from app import codes


def test_encode_is_base_62():
    assert codes.encode(0) == "0"
    assert codes.encode(61) == "Z"
    assert codes.encode(62) == "10"
    assert codes.encode(125) == "21"


def test_new_code_has_seven_letters_and_digits():
    code = codes.new_code()
    assert len(code) == 7
    assert all(c in codes.ALPHABET for c in code)


def test_new_codes_are_different():
    assert (
        len({codes.new_code() for _ in range(1000)}) == 1000
    )
