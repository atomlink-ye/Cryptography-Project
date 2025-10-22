"""Cryptography visualization entry point."""
from __future__ import annotations

from typing import Iterable

import streamlit as st

from visualization import birthday_views, pollard_views, ui_components


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
    birthday_views.show_birthday(params)
    st.divider()
    birthday_views.show_difficulty_scaling(DEFAULT_DIFFICULTY_BITS)


def _render_pollard(params: ui_components.PollardParameters) -> None:
    st.markdown(
        """
        **Pollard's Rho** is an algorithm for finding collisions in hash functions. 
        It uses a random walk to detect a cycle in the sequence of hashed values.
        """
    )
    pollard_views.show_pollard(params)
    st.divider()
    birthday_views.show_difficulty_scaling(DEFAULT_DIFFICULTY_BITS)


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
        else:  # defensive fallback
            st.warning("Unknown attack selection.")
            return

    if attack == "Birthday Attack":
        _render_birthday(params)
    elif attack == "Pollard's Rho":
        _render_pollard(params)


if __name__ == "__main__":
    main()
