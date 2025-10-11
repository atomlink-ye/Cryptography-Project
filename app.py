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


def _render_birthday() -> None:
    params = ui_components.birthday_controls()
    graphs.show_birthday(params)
    st.divider()
    graphs.show_difficulty_scaling(DEFAULT_DIFFICULTY_BITS)


def _render_pollard() -> None:
    params = ui_components.pollard_controls()
    animator.show_pollard(params)
    st.divider()
    graphs.show_difficulty_scaling(DEFAULT_DIFFICULTY_BITS)


def _render_avalanche() -> None:
    params = ui_components.avalanche_controls()
    graphs.show_avalanche(params)


def _render_length_extension() -> None:
    params = ui_components.length_extension_controls()
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

    if attack == "Birthday Attack":
        _render_birthday()
    elif attack == "Pollard's Rho":
        _render_pollard()
    elif attack == "Length Extension":
        _render_length_extension()
    else:
        _render_avalanche()


if __name__ == "__main__":
    main()
