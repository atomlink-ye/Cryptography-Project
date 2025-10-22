"""Cryptography visualization entry point."""
from __future__ import annotations

from typing import Iterable

import streamlit as st

from core import SimpleMDHasher
from visualization import animator, graphs, ui_components


DEFAULT_DIFFICULTY_BITS: Iterable[int] = [8, 12, 16, 20, 24]


def _running_inside_streamlit() -> bool:
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        return get_script_run_ctx() is not None
    except Exception:  # pragma: no cover - defensive: streamlit internals may differ
        return False


def _render_birthday(params: ui_components.BirthdayParameters) -> None:
    st.markdown(
        """
        The **Birthday Attack** is a statistical technique to find collisions in hash functions. 
        It exploits the mathematics behind the birthday problem in probability theory.
        """
    )
    graphs.show_birthday(params)
    st.divider()
    graphs.show_difficulty_scaling(DEFAULT_DIFFICULTY_BITS)


def _render_pollard(params: ui_components.PollardParameters) -> None:
    st.markdown(
        """
        **Pollard's Rho** is an algorithm for finding collisions in hash functions. 
        It uses a random walk to detect a cycle in the sequence of hashed values.
        """
    )
    animator.show_pollard(params)
    st.divider()
    graphs.show_difficulty_scaling(DEFAULT_DIFFICULTY_BITS)


def _render_avalanche(params: ui_components.AvalancheParameters) -> None:
    st.markdown(
        """
        The **Avalanche Effect** is a desirable property of cryptographic hash functions. 
        It means that a small change in the input (like flipping a single bit) produces a large change in the output.
        """
    )
    graphs.show_avalanche(params)


def _render_length_extension(params: ui_components.LengthExtensionParameters) -> None:
    st.markdown(
        """
        A **Length Extension Attack** is an attack on certain types of hash functions (like those based on the Merkle–Damgård construction). 
        If you know the hash of a message, you can compute the hash of a longer message without knowing the original message.
        """
    )
    hasher = SimpleMDHasher()
    result = graphs.show_length_extension(params, hasher=hasher)
    if result is not None and params.secret is not None:
        st.caption("Forged message verified using supplied secret.")


def main() -> None:
    if not _running_inside_streamlit():
        print("This application is designed to run with 'streamlit run app.py'.")
        return

    st.set_page_config(page_title="Hash Function Visualizer", page_icon="🔐", layout="wide")
    st.title("🔐 Cryptography Hash Function Visualizer")
    st.write("Interactive simulations of classic hash-based attacks.")

    attack = ui_components.attack_selector()

    with st.sidebar.expander(attack, expanded=True):
        if attack == "Birthday Attack":
            params = ui_components.birthday_controls()
        elif attack == "Pollard's Rho":
            params = ui_components.pollard_controls()
        elif attack == "Length Extension":
            params = ui_components.length_extension_controls()
        else:
            params = ui_components.avalanche_controls()

    if attack == "Birthday Attack":
        _render_birthday(params)
    elif attack == "Pollard's Rho":
        _render_pollard(params)
    elif attack == "Length Extension":
        _render_length_extension(params)
    else:
        _render_avalanche(params)


if __name__ == "__main__":
    main()
