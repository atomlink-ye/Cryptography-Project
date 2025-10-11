"""Toy hash helpers and avalanche experiments."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Iterable, Iterator

from .common import truncate_digest


DEFAULT_HASH_BITS = 20


def toy_hash(message: bytes, bits: int = DEFAULT_HASH_BITS) -> int:
    """Return ``bits``-bit toy hash using SHA-256 truncation.

    The function remains intentionally lightweight but deterministic so that
    visualizations can run in real time while still reflecting cryptographic
    dynamics.
    """

    digest = hashlib.sha256(message).digest()
    return truncate_digest(digest, bits)


@dataclass
class AvalancheResult:
    bit_index: int
    fraction_changed: float
    baseline_hash: int
    flipped_hash: int


def _flip_bit(message: bytes, bit_index: int) -> bytes:
    if bit_index < 0:
        raise ValueError("bit_index must be non-negative")
    byte_index, offset = divmod(bit_index, 8)
    if byte_index >= len(message):
        raise ValueError("bit_index out of range for the message")
    mutable = bytearray(message)
    mutable[byte_index] ^= 1 << offset
    return bytes(mutable)


def avalanche_test(
    message: bytes,
    bit_index: int,
    *,
    bits: int = DEFAULT_HASH_BITS,
) -> AvalancheResult:
    """Flip ``bit_index`` of ``message`` and measure changed output bits."""

    baseline = toy_hash(message, bits)
    flipped_message = _flip_bit(message, bit_index)
    flipped = toy_hash(flipped_message, bits)
    diff = baseline ^ flipped
    changed = bin(diff).count("1")
    return AvalancheResult(
        bit_index=bit_index,
        fraction_changed=changed / bits,
        baseline_hash=baseline,
        flipped_hash=flipped,
    )


def run_avalanche_suite(
    message: bytes,
    *,
    bits: int = DEFAULT_HASH_BITS,
) -> list[AvalancheResult]:
    """Run the avalanche test for every input bit of ``message``."""

    total_bits = len(message) * 8
    return [avalanche_test(message, idx, bits=bits) for idx in range(total_bits)]


__all__ = [
    "AvalancheResult",
    "DEFAULT_HASH_BITS",
    "run_avalanche_suite",
    "toy_hash",
    "avalanche_test",
]
