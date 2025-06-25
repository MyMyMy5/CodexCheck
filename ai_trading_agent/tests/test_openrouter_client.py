from __future__ import annotations

import sys, types
openai_stub = types.SimpleNamespace(ChatCompletion=types.SimpleNamespace(create=lambda *a, **k: None))
sys.modules.setdefault("openai", openai_stub)
import json
from unittest.mock import patch

from ai_trading_agent.src.ai_modules.openrouter_client import OpenRouterClient


def test_call_llm_parsing(monkeypatch):
    client = OpenRouterClient()

    fake_response = {
        "choices": [
            {"message": {"content": json.dumps({"decision": "buy", "reason": "test", "adjustments": {}})}}
        ]
    }

    with patch("openai.ChatCompletion.create", return_value=fake_response):
        result = client.call_llm("data")
        assert result["decision"] == "buy"

