"""Common utilities shared by cryptographic visualizations."""
from __future__ import annotations

from dataclasses import dataclass
import os
import random
from typing import Iterator, Iterable


RANDOM_MESSAGE_LENGTH = 8  # bytes


def truncate_digest(digest: bytes, bits: int) -> int:
    """Return the integer value of ``digest`` truncated to ``bits`` bits.

    Args:
        digest: Raw digest bytes from a cryptographic hash function.
        bits: Number of most-significant bits to keep (1 <= bits <= len(digest)*8).

    Raises:
        ValueError: If ``bits`` is out of range.
    """

    if bits <= 0:
        raise ValueError("bits must be positive")
    if bits > len(digest) * 8:
        raise ValueError("bits exceeds digest size")

    value = int.from_bytes(digest, "big")
    mask = (1 << bits) - 1
    return value & mask


def random_message(
    length: int = RANDOM_MESSAGE_LENGTH,
    *,
    rng: random.Random | None = None,
) -> bytes:
    """Return a pseudo-random byte string of ``length`` bytes.

    The RNG parameter enables deterministic simulations for tests.
    """

    if length <= 0:
        raise ValueError("length must be positive")
    if rng is None:
        return os.urandom(length)
    return bytes(rng.getrandbits(8) for _ in range(length))


def iter_random_messages(
    count: int,
    length: int = RANDOM_MESSAGE_LENGTH,
    *,
    rng: random.Random | None = None,
) -> Iterator[bytes]:
    """Yield ``count`` random byte strings using ``random_message``."""

    for _ in range(count):
        yield random_message(length, rng=rng)


@dataclass
class CollisionResult:
    """Holds the outcome of a collision search."""

    trials: int
    first_message: bytes
    second_message: bytes
    collision_value: int


@dataclass
class SampledSequence:
    """Stores a sequence of integer states for visualization."""

    states: list[int]

    def __iter__(self) -> Iterator[int]:
        return iter(self.states)

    def tail(self, size: int) -> list[int]:
        """Return the last ``size`` states (or fewer if not enough)."""

        if size <= 0:
            return []
        return self.states[-size:]


__all__ = [
    "CollisionResult",
    "RANDOM_MESSAGE_LENGTH",
    "SampledSequence",
    "iter_random_messages",
    "random_message",
    "truncate_digest",
]
