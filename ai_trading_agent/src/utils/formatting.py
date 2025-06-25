"""Helpers for formatting market data for the LLM."""
from __future__ import annotations

from typing import Dict

import pandas as pd


def format_market_data(df: pd.DataFrame, indicators: Dict[str, float], position: Dict[str, float]) -> str:
    """Return a text summary for the LLM prompt."""
    latest = df.tail(20).to_dict(orient="records")
    indicator_lines = ", ".join(f"{k}: {v:.4f}" for k, v in indicators.items())
    position_line = ", ".join(f"{k}: {v}" for k, v in position.items())
    return (
        "Market data (latest 20 candles):\n" +
        f"{latest}\n" +
        "Indicators: " + indicator_lines + "\n" +
        "Position: " + position_line
    )

