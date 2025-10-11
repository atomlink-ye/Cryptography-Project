"""Reusable UI widgets for the Streamlit front-end."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import streamlit as st


ATTACK_OPTIONS = [
    "Birthday Attack",
    "Pollard's Rho",
    "Length Extension",
    "Avalanche Test",
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


@dataclass
class AvalancheParameters:
    bits: int
    message: bytes


@dataclass
class LengthExtensionParameters:
    original_message: bytes
    appended_message: bytes
    key_length_guess: int
    observed_digest: Optional[str]
    secret: Optional[bytes]


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
    st.sidebar.subheader("Birthday Attack")
    bits = st.sidebar.slider("Hash bit length", 8, 32, default_bits, key="birthday-bits")
    runs = st.sidebar.slider("Simulation runs", 5, 200, 50, key="birthday-runs")
    max_trials = st.sidebar.number_input("Max trials per run", min_value=1, max_value=1_000_000, value=10000, step=1000, key="birthday-max")
    message_length = st.sidebar.number_input(
        "Message size (bytes)", min_value=1, max_value=64, value=8, step=1, key="birthday-msg-len"
    )
    seed_text = st.sidebar.text_input("Random seed (optional)", value="", key="birthday-seed")
    rng_seed = _parse_optional_seed(seed_text)
    return BirthdayParameters(
        bits=bits,
        runs=runs,
        max_trials=max_trials,
        message_length=message_length,
        rng_seed=rng_seed,
    )


def pollard_controls(default_bits: int = 16) -> PollardParameters:
    st.sidebar.subheader("Pollard's Rho")
    bits = st.sidebar.slider("Hash bit length", 8, 32, default_bits, key="pollard-bits")
    start = st.sidebar.number_input("Start value", min_value=0, max_value=2 ** 16, value=1, step=1, key="pollard-start")
    max_steps = st.sidebar.number_input(
        "Max iterations", min_value=10, max_value=500_000, value=10_000, step=100, key="pollard-steps"
    )
    return PollardParameters(bits=bits, start=start, max_steps=max_steps)


def avalanche_controls(default_bits: int = 16) -> AvalancheParameters:
    st.sidebar.subheader("Avalanche Test")
    bits = st.sidebar.slider("Hash bit length", 8, 32, default_bits, key="avalanche-bits")
    message_text = st.sidebar.text_area(
        "Message (ASCII)",
        value="hello world",
        key="avalanche-message",
        help="Message used to evaluate the avalanche effect",
    )
    message = message_text.encode("utf-8")
    return AvalancheParameters(bits=bits, message=message)


def length_extension_controls() -> LengthExtensionParameters:
    st.sidebar.subheader("Length Extension")
    original = st.sidebar.text_area(
        "Original message",
        value="transfer=1000&to=bob",
        key="length-original",
    )
    append = st.sidebar.text_area(
        "Appended data",
        value="&to=mallory",
        key="length-append",
    )
    key_guess = st.sidebar.number_input(
        "Key length guess (bytes)", min_value=0, max_value=128, value=8, step=1, key="length-key-guess"
    )
    digest = st.sidebar.text_input(
        "Observed digest (hex)",
        value="",
        key="length-digest",
        help="Digest of secret||original message. Provide if known.",
    )
    secret_text = st.sidebar.text_input(
        "(Optional) actual secret to verify",
        value="",
        help="Provide to verify the forged digest matches the real tag",
        key="length-secret",
    )
    secret = secret_text.encode("utf-8") if secret_text else None
    observed_digest = digest.strip() or None
    return LengthExtensionParameters(
        original_message=original.encode("utf-8"),
        appended_message=append.encode("utf-8"),
        key_length_guess=key_guess,
        observed_digest=observed_digest,
        secret=secret,
    )


def info_box(label: str, value: str) -> None:
    st.metric(label, value)


__all__ = [
    "ATTACK_OPTIONS",
    "AvalancheParameters",
    "BirthdayParameters",
    "LengthExtensionParameters",
    "PollardParameters",
    "attack_selector",
    "avalanche_controls",
    "birthday_controls",
    "info_box",
    "length_extension_controls",
    "pollard_controls",
]
