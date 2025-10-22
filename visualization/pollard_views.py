"""Animation data for Pollard's rho demonstration."""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core import pollard_rho, pollard_trace
from core.pollard import PollardResult
from .ui_components import PollardParameters


def _path_dataframe(result: PollardResult) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "step": list(range(len(result.tortoise_path))),
            "tortoise": result.tortoise_path,
            "hare": result.hare_path,
        }
    )


def show_pollard(params: PollardParameters) -> PollardResult:
    result = pollard_rho(bits=params.bits, start=params.start, max_steps=params.max_steps)
    data = _path_dataframe(result)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["step"],
            y=data["tortoise"],
            mode="lines+markers",
            name="Tortoise",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data["step"],
            y=data["hare"],
            mode="lines+markers",
            name="Hare",
        )
    )

    # Add markers for start and collision
    collision_step = result.iterations
    fig.add_trace(
        go.Scatter(
            x=[0, collision_step],
            y=[result.tortoise_path[0], result.tortoise_path[collision_step]],
            mode="markers",
            marker=dict(size=10, color=["green", "red"]),
            name="Events",
            hoverinfo="text",
            text=["Start", f"Collision at step {collision_step}"],
        )
    )

    fig.update_layout(
        title="Pollard's rho pointer progression",
        xaxis_title="Iteration",
        yaxis_title="State value",
        legend_title_text="Pointers",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.info(
        f"Collision found after **{result.iterations}** iterations. "
        f"The cycle starts at iteration **{result.tail_length}** and has a length of **{result.cycle_length}**. "
        f"The graph shows the paths of the tortoise and hare pointers, which meet at the collision point."
    )

    st.subheader("State transitions")
    mapping = pollard_trace(bits=params.bits, start=params.start)
    table = pd.DataFrame({"state": list(mapping.keys()), "next_state": list(mapping.values())})
    st.dataframe(table.head(20), use_container_width=True, height=300)

    return result


__all__ = ["show_pollard"]
