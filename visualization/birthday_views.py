"""Graph rendering helpers for Streamlit."""
from __future__ import annotations

import math
import random
from typing import Iterable

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from core import (
    BirthdayRun,
    estimate_collision_probability,
    simulate_birthday_trials,
)
from .ui_components import BirthdayParameters


def birthday_dataframe(params: BirthdayParameters) -> pd.DataFrame:
    rng = random.Random(params.rng_seed) if params.rng_seed is not None else random.Random()
    runs = simulate_birthday_trials(
        bits=params.bits,
        runs=params.runs,
        rng=rng,
        message_length=params.message_length,
        max_trials=params.max_trials,
    )
    rows = [
        {
            "run": index + 1,
            "trials": run.trials,
            "collision": run.collision is not None,
            "collision_value": run.collision.collision_value if run.collision else None,
        }
        for index, run in enumerate(runs)
    ]
    return pd.DataFrame(rows)


def birthday_probability_curve(bits: int, max_trials: int, points: int = 50) -> pd.DataFrame:
    trial_counts = np.linspace(1, max_trials, num=points, dtype=int)
    probabilities = [estimate_collision_probability(int(trial), bits) for trial in trial_counts]
    return pd.DataFrame({"trials": trial_counts, "probability": probabilities})


def show_birthday(params: BirthdayParameters) -> None:
    data = birthday_dataframe(params)
    if data.empty:
        st.info("No collision data available")
        return

    fig = px.scatter(
        data,
        x="trials",
        y="run",
        color="collision",
        labels={"trials": "Trials until collision", "run": "Simulation run"},
        title="Birthday collision search trials",
        hover_data=["collision_value"],
        color_discrete_map={True: "dodgerblue", False: "lightblue"},
    )
    st.plotly_chart(fig, use_container_width=True)

    probability = birthday_probability_curve(params.bits, params.max_trials)
    prob_fig = go.Figure()
    prob_fig.add_trace(
        go.Scatter(
            x=probability["trials"],
            y=probability["probability"],
            name="Probability",
            mode="lines",
        )
    )

    p = 0.5
    birthday_bound = math.sqrt(2 * (2**params.bits) * math.log(1 / (1 - p)))
    prob_fig.add_vline(
        x=birthday_bound,
        line_width=2,
        line_dash="dash",
        line_color="red",
        annotation_text="50% probability",
        annotation_position="top left",
    )

    prob_fig.update_layout(
        title="Collision probability vs trials",
        xaxis_title="Trials",
        yaxis_title="Probability",
    )
    st.plotly_chart(prob_fig, use_container_width=True)

    average_trials = data["trials"].mean()
    st.caption(
        f"Average trials to collision across {params.runs} runs: {average_trials:,.0f} "
        f"(theoretical: {birthday_bound:,.0f})"
    )


def difficulty_scaling_dataframe(bit_sizes: Iterable[int]) -> pd.DataFrame:
    rows = []
    for bits in bit_sizes:
        birthday_cost = 2 ** (bits / 2)
        pollard_cost = math.sqrt(math.pi * (2 ** (bits - 1)))
        brute_force_cost = 2 ** bits
        rows.extend(
            [
                {"algorithm": "Birthday", "bits": bits, "operations": birthday_cost},
                {"algorithm": "Pollard's Rho", "bits": bits, "operations": pollard_cost},
                {"algorithm": "Brute Force", "bits": bits, "operations": brute_force_cost},
            ]
        )
    return pd.DataFrame(rows)


def show_difficulty_scaling(bit_sizes: Iterable[int]) -> None:
    data = difficulty_scaling_dataframe(bit_sizes)
    fig = px.line(
        data,
        x="bits",
        y="operations",
        color="algorithm",
        log_y=True,
        title="Attack complexity vs hash size",
    )
    fig.update_traces(mode="markers+lines")
    fig.update_yaxes(title="Operations (log scale)")
    st.plotly_chart(fig, use_container_width=True)


__all__ = [
    "birthday_dataframe",
    "birthday_probability_curve",
    "difficulty_scaling_dataframe",
    "show_birthday",
    "show_difficulty_scaling",
]
