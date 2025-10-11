import random

from core.birthday import birthday_attack, simulate_birthday_trials, estimate_collision_probability


def test_birthday_attack_finds_collision_quickly():
    rng = random.Random(42)
    collision = birthday_attack(bits=8, max_trials=500, rng=rng)
    assert collision is not None
    assert collision.trials <= 500
    assert collision.first_message != collision.second_message


def test_simulation_returns_expected_runs():
    rng = random.Random(123)
    runs = simulate_birthday_trials(bits=8, runs=5, rng=rng, max_trials=1000)
    assert len(runs) == 5
    assert all(run.trials <= 1000 for run in runs)


def test_collision_probability_bounds():
    probability = estimate_collision_probability(50, 16)
    assert 0.0 <= probability <= 1.0
    assert probability > 0.0
