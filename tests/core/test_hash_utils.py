from core.hash_utils import toy_hash


def test_toy_hash_range_and_repeatability():
    message = b"hello"
    bits = 16
    result = toy_hash(message, bits)
    assert 0 <= result < 2 ** bits
    # hashing same message yields same value
    assert result == toy_hash(message, bits)
