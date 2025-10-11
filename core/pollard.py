"""Pollard's rho collision finder utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List

from .hash_utils import toy_hash, DEFAULT_HASH_BITS


def _hash_step(value: int, bits: int) -> int:
    # Use a fixed-width encoding so the map size remains bounded by ``bits``.
    byte_length = max(1, (bits + 7) // 8)
    return toy_hash(value.to_bytes(byte_length, "big"), bits)


@dataclass
class PollardResult:
    collision_value: int
    iterations: int
    tail_length: int
    cycle_length: int
    tortoise_path: list[int]
    hare_path: list[int]


def _locate_cycle_parameters(
    *,
    bits: int,
    start: int,
    meeting: int,
) -> tuple[int, int]:
    """Compute the tail (μ) and cycle (λ) length after a collision was detected."""

    tortoise = start
    hare = meeting
    mu = 0
    while tortoise != hare:
        tortoise = _hash_step(tortoise, bits)
        hare = _hash_step(hare, bits)
        mu += 1

    hare = _hash_step(tortoise, bits)
    lam = 1
    while tortoise != hare:
        hare = _hash_step(hare, bits)
        lam += 1
    return mu, lam


def pollard_rho(
    *,
    bits: int = DEFAULT_HASH_BITS,
    start: int = 1,
    max_steps: int = 100_000,
) -> PollardResult:
    """Execute Floyd's cycle detection for the toy hash function."""

    tortoise = start
    hare = start
    tortoise_path = [tortoise]
    hare_path = [hare]

    for iteration in range(1, max_steps + 1):
        tortoise = _hash_step(tortoise, bits)
        hare = _hash_step(_hash_step(hare, bits), bits)
        tortoise_path.append(tortoise)
        hare_path.append(hare)
        if tortoise == hare:
            mu, lam = _locate_cycle_parameters(bits=bits, start=start, meeting=tortoise)
            return PollardResult(
                collision_value=tortoise,
                iterations=iteration,
                tail_length=mu,
                cycle_length=lam,
                tortoise_path=tortoise_path,
                hare_path=hare_path,
            )

    raise RuntimeError("Pollard rho did not converge within max_steps")


def pollard_trace(
    *,
    bits: int = DEFAULT_HASH_BITS,
    start: int = 1,
    steps: int = 200,
) -> dict[int, int]:
    """Return a mapping of ``state -> f(state)`` for visualization graphs."""

    trace: dict[int, int] = {}
    value = start
    for _ in range(steps):
        next_value = _hash_step(value, bits)
        trace[value] = next_value
        value = next_value
        if value in trace:
            break
    return trace


__all__ = [
    "PollardResult",
    "pollard_rho",
    "pollard_trace",
]
