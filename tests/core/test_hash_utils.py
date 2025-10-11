import pytest

from core.hash_utils import toy_hash, run_avalanche_suite, avalanche_test


def test_toy_hash_range_and_repeatability():
    message = b"hello"
    bits = 16
    result = toy_hash(message, bits)
    assert 0 <= result < 2 ** bits
    # hashing same message yields same value
    assert result == toy_hash(message, bits)


def test_avalanche_suite_covers_message_bits():
    message = b"abc"
    results = run_avalanche_suite(message, bits=12)
    assert len(results) == len(message) * 8
    sample = avalanche_test(message, 0, bits=12)
    assert 0.0 <= sample.fraction_changed <= 1.0
    assert isinstance(sample.baseline_hash, int)
    assert isinstance(sample.flipped_hash, int)
