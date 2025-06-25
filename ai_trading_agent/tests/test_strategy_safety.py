from __future__ import annotations

from ai_trading_agent.src.strategies.ai_trading_strategy import AITradingStrategy


def test_invalid_llm_output(monkeypatch):
    strategy = AITradingStrategy()

    def fake_call(_):
        return {"bad": "data"}

    monkeypatch.setattr(strategy, "client", type("C", (), {"call_llm": fake_call})())
    strategy.decision = strategy.client.call_llm("data")

    import pandas as pd
    df = pd.DataFrame({"close": [1, 2, 3]})
    df = strategy.populate_entry_trend(df, {})
    assert df["enter_long"].sum() == 0
    assert strategy.stoploss <= 0.2

