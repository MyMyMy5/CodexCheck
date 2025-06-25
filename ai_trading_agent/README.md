# AI Trading Agent

This project integrates an OpenRouter-hosted LLM with the Freqtrade engine using MCP-style prompts. It gathers market data, consults the LLM for trading decisions, and executes those decisions within safe bounds.

## Installation
```bash
pip install -r requirements.txt
```

## Freqtrade Configuration
Add the following snippet to your `config.json`:
```json
{
  "max_open_trades": 1,
  "timeframe": "5m",
  "stake_currency": "USDT",
  "dry_run": true,
  "strategy": "AITradingStrategy",
  "api_server": { "enabled": true, "listen_ip": "127.0.0.1", "listen_port": 8181 }
}
```
Export your OpenRouter key before running:
```bash
export OPENROUTER_API_KEY="sk-..."
```

## Usage
```bash
freqtrade create-userdir --userdir ft_bot && \
freqtrade new-config -c ft_bot/config.json

cp src/strategies/ai_trading_strategy.py ft_bot/user_data/strategies/

freqtrade trade --config ft_bot/config.json --strategy AITradingStrategy
```
The console will display messages like:
```yaml
[LLM Decision] Action: buy | Reason: "Uptrend..." | Adjustments: {'stop_loss_pct': 0.03}
```
confirming LLM interaction.
