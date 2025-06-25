"""Client to interact with OpenRouter-hosted LLMs."""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List

import openai


class OpenRouterClient:
    """Wrapper for OpenRouter LLM interactions."""

    SYSTEM_PROMPT: str = (
        "You are an automated trading assistant. Respond only with JSON adhering to "
        '{"decision": "buy|sell|hold", "reason": str, "adjustments": {"stop_loss_pct": float, "stake_pct": float}}.'
    )

    def __init__(self, model: str = "microsoft/mai-ds-r1:free", *, max_tokens: int = 1000, temperature: float = 0.0) -> None:
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = float(os.getenv("LLM_TEMPERATURE", temperature))
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not set")
        openai.api_key = api_key
        openai.base_url = "https://openrouter.ai/api/v1"

    def build_messages(self, market_data: str) -> List[Dict[str, str]]:
        """Build chat messages for the LLM."""
        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": market_data},
        ]

    def _parse_response(self, content: str) -> Dict[str, Any]:
        try:
            cleaned = content.strip().strip('`')
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {"decision": "hold"}

    def call_llm(self, market_data: str) -> Dict[str, Any]:
        """Call the LLM and return its decision."""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=self.build_messages(market_data),
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            content = response.choices[0].message.content
            return self._parse_response(content)
        except Exception:
            return {"decision": "hold"}

