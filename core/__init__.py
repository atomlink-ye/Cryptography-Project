"""Core cryptographic simulation utilities."""
from .common import CollisionResult, SampledSequence, random_message, iter_random_messages
from .hash_utils import toy_hash, avalanche_test, run_avalanche_suite
from .birthday import birthday_attack, estimate_collision_probability, simulate_birthday_trials, BirthdayRun
from .pollard import pollard_rho, pollard_trace
from .length_ext import (
    SimpleMDHasher,
    compute_tag,
    forge_length_extension,
    LengthExtensionResult,
)

__all__ = [
    "CollisionResult",
    "SampledSequence",
    "toy_hash",
    "avalanche_test",
    "run_avalanche_suite",
    "birthday_attack",
    "estimate_collision_probability",
    "simulate_birthday_trials",
    "BirthdayRun",
    "pollard_rho",
    "pollard_trace",
    "SimpleMDHasher",
    "compute_tag",
    "forge_length_extension",
    "LengthExtensionResult",
    "random_message",
    "iter_random_messages",
]
