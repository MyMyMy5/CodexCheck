"""Freqtrade strategy integrating an OpenRouter LLM."""
from __future__ import annotations

import json
from typing import Any, Dict

import pandas as pd
from freqtrade.strategy.interface import IStrategy
from freqtrade.persistence import Trade

from ai_trading_agent.src.ai_modules.openrouter_client import OpenRouterClient
from ai_trading_agent.src.utils.formatting import format_market_data


class AITradingStrategy(IStrategy):
    """AI-driven trading strategy."""

    timeframe = "5m"
    minimal_roi = {"0": 0.01}
    startup_candle_count: int = 30

    def bot_start(self, **kwargs: Any) -> None:
        self.client = OpenRouterClient()
        self.current_position: Dict[str, float] = {}
        self.stoploss: float = 0.1
        self.desired_stake_pct: float = 1.0
        self.last_processed: int = 0

    def bot_loop_start(self, current_time, **kwargs: Any) -> None:
        if self.dp.runmode.value == "live" and not self.open_trades:  # use dp timeframe
            pass
        df = self.dp.get_ohlcv(self.config["exchange"].get("pair"), self.timeframe)
        if df is None or len(df) < self.startup_candle_count:
            return
        last = df.iloc[-1]
        if last.name == self.last_processed:
            return
        self.last_processed = last.name
        indicators = {"close": float(last["close"])}
        prompt = format_market_data(df, indicators, self.current_position)
        decision = self.client.call_llm(prompt)
        self.decision = decision
        if decision.get("adjustments"):
            adj = decision["adjustments"]
            sl_pct = max(0.0, min(0.2, float(adj.get("stop_loss_pct", self.stoploss))))
            stake_pct = max(0.0, min(1.0, float(adj.get("stake_pct", self.desired_stake_pct))))
            self.stoploss = sl_pct
            self.desired_stake_pct = stake_pct

    def populate_entry_trend(self, df: pd.DataFrame, metadata: Dict[str, Any]) -> pd.DataFrame:
        df["enter_long"] = 0
        if hasattr(self, "decision") and self.decision.get("decision") == "buy":
            df.loc[df.index == self.last_processed, "enter_long"] = 1
        return df

    def populate_exit_trend(self, df: pd.DataFrame, metadata: Dict[str, Any]) -> pd.DataFrame:
        df["exit_long"] = 0
        if hasattr(self, "decision") and self.decision.get("decision") == "sell":
            df.loc[df.index == self.last_processed, "exit_long"] = 1
        return df

    def custom_stoploss(self, pair: str, trade: Trade, current_time, current_rate: float, current_profit: float, **kwargs: Any) -> float:
        return -abs(self.stoploss)

    def custom_stake_amount(self, pair: str, current_entry_price: float, current_stop_price: float, **kwargs: Any) -> float:
        wallet = self.wallets.get_total(self.config["stake_currency"])
        return wallet * self.desired_stake_pct

