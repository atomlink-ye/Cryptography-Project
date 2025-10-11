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
    fig.update_layout(
        title="Pollard's rho pointer progression",
        xaxis_title="Iteration",
        yaxis_title="State value",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        f"Iterations: {result.iterations} · Tail length: {result.tail_length} · Cycle length: {result.cycle_length}"
    )

    mapping = pollard_trace(bits=params.bits, start=params.start)
    table = pd.DataFrame({"state": list(mapping.keys()), "next_state": list(mapping.values())})
    st.dataframe(table.head(20), use_container_width=True)

    return result


__all__ = ["show_pollard"]
