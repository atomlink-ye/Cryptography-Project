"""Birthday attack simulation tools."""
from __future__ import annotations

import math
from dataclasses import dataclass
import random
from typing import Iterator, Iterable

from .common import CollisionResult, random_message
from .hash_utils import toy_hash, DEFAULT_HASH_BITS


@dataclass
class BirthdayRun:
    """Metadata about a full birthday experiment."""

    trials: int
    collision: CollisionResult | None


def birthday_attack(
    *,
    bits: int = DEFAULT_HASH_BITS,
    max_trials: int = 1_000_000,
    rng: random.Random | None = None,
    message_length: int = 8,
) -> CollisionResult | None:
    """Search for a collision using a birthday attack strategy."""

    seen: dict[int, bytes] = {}
    for trial in range(1, max_trials + 1):
        message = random_message(message_length, rng=rng)
        digest = toy_hash(message, bits)
        if digest in seen:
            other = seen[digest]
            return CollisionResult(
                trials=trial,
                first_message=other,
                second_message=message,
                collision_value=digest,
            )
        seen[digest] = message
    return None


def simulate_birthday_trials(
    *,
    bits: int = DEFAULT_HASH_BITS,
    runs: int = 100,
    rng: random.Random | None = None,
    message_length: int = 8,
    max_trials: int = 1_000_000,
) -> list[BirthdayRun]:
    """Run multiple simulations collecting the number of trials per run."""

    results: list[BirthdayRun] = []
    for _ in range(runs):
        collision = birthday_attack(
            bits=bits,
            max_trials=max_trials,
            rng=rng,
            message_length=message_length,
        )
        trials = collision.trials if collision else max_trials
        results.append(BirthdayRun(trials=trials, collision=collision))
    return results


def estimate_collision_probability(trials: int, bit_size: int) -> float:
    """Return the theoretical probability of at least one collision."""

    space_size = 2 ** bit_size
    exponent = -(trials * (trials - 1)) / (2 * space_size)
    probability = 1 - math.exp(exponent)
    return min(max(probability, 0.0), 1.0)


__all__ = [
    "BirthdayRun",
    "birthday_attack",
    "estimate_collision_probability",
    "simulate_birthday_trials",
]
