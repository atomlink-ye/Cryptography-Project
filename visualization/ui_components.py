"""Reusable UI widgets for the Streamlit front-end."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import streamlit as st


ATTACK_OPTIONS = [
    "Birthday Attack",
    "Pollard's Rho",
]


@dataclass
class BirthdayParameters:
    bits: int
    runs: int
    max_trials: int
    message_length: int
    rng_seed: Optional[int]


@dataclass
class PollardParameters:
    bits: int
    start: int
    max_steps: int


def attack_selector() -> str:
    st.sidebar.title("Simulation Controls")
    return st.sidebar.selectbox("Select demonstration", ATTACK_OPTIONS, key="attack-select")


def _parse_optional_seed(value: str) -> Optional[int]:
    value = value.strip()
    if not value:
        return None
    try:
        return int(value, 10)
    except ValueError:
        st.sidebar.error("Seed must be an integer")
        return None


def birthday_controls(default_bits: int = 16) -> BirthdayParameters:
    bits = st.slider("Hash bit length", 8, 32, default_bits, key="birthday-bits")
    runs = st.slider("Simulation runs", 5, 200, 50, key="birthday-runs")
    max_trials = st.number_input("Max trials per run", min_value=1, max_value=1_000_000, value=10000, step=1000, key="birthday-max")
    message_length = st.number_input(
        "Message size (bytes)", min_value=1, max_value=64, value=8, step=1, key="birthday-msg-len"
    )
    seed_text = st.text_input("Random seed (optional)", value="", key="birthday-seed")
    rng_seed = _parse_optional_seed(seed_text)
    return BirthdayParameters(
        bits=bits,
        runs=runs,
        max_trials=max_trials,
        message_length=message_length,
        rng_seed=rng_seed,
    )


def pollard_controls(default_bits: int = 16) -> PollardParameters:
    bits = st.slider("Hash bit length", 8, 32, default_bits, key="pollard-bits")
    start = st.number_input("Start value", min_value=0, max_value=2 ** 16, value=1, step=1, key="pollard-start")
    max_steps = st.number_input(
        "Max iterations", min_value=10, max_value=500_000, value=10_000, step=100, key="pollard-steps"
    )
    return PollardParameters(bits=bits, start=start, max_steps=max_steps)


def info_box(label: str, value: str) -> None:
    st.metric(label, value)


__all__ = [
    "ATTACK_OPTIONS",
    "BirthdayParameters",
    "PollardParameters",
    "attack_selector",
    "birthday_controls",
    "info_box",
    "pollard_controls",
]
