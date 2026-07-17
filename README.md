# Market Data Toolkit

[![Tests](https://github.com/weston-boyd/market-data-toolkit/actions/workflows/python-app.yml/badge.svg)](https://github.com/weston-boyd/market-data-toolkit/actions/workflows/python-app.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A tested Python toolkit for validating, normalizing, aggregating, and analyzing financial time-series data.

This repository contains reusable market-data engineering components extracted from the private WesB Algos research platform. It includes only generic data-processing infrastructure; no proprietary trading strategies, alpha models, broker integrations, or research datasets are included.

## Implemented Features

- Canonical tick and OHLCV bar models
- Vendor/broker tick-payload normalization
- UTC timestamp normalization
- Fixed-time OHLCV aggregation from ticks
- Required-column and numeric-value validation
- Duplicate and out-of-order timestamp detection
- OHLC price-integrity checks
- CSV integrity reports
- DataFrame quality summaries
- Higher-timeframe OHLCV resampling
- Automated pytest coverage
- Package-specific exception hierarchy
- Expanded quickstart and API documentation
- Working example using synthetic data

## Project Structure

```text
market-data-toolkit/
├── src/market_data_toolkit/
│   ├── models.py
│   ├── normalize.py
│   ├── aggregate.py
│   ├── validate.py
│   ├── integrity.py
│   └── resample.py
├── tests/
├── examples/
├── docs/
└── pyproject.toml
```

## Installation

```bash
git clone https://github.com/weston-boyd/market-data-toolkit.git
cd market-data-toolkit
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Run the Tests

```bash
pytest
```

## Documentation

- [Quickstart](docs/QUICKSTART.md)
- [Public API](docs/API.md)
- [Design Notes](docs/DESIGN.md)

## Run the Example

```bash
python examples/example_pipeline.py
```

## Quick Example

```python
import pandas as pd

from market_data_toolkit import validate_ohlcv_frame, resample_ohlcv

frame = pd.DataFrame(
    {
        "timestamp": pd.date_range("2026-01-01 09:30", periods=5, freq="1min", tz="UTC"),
        "open": [100, 101, 102, 103, 104],
        "high": [101, 102, 103, 104, 105],
        "low": [99, 100, 101, 102, 103],
        "close": [100.5, 101.5, 102.5, 103.5, 104.5],
        "volume": [10, 12, 8, 15, 11],
    }
)

report = validate_ohlcv_frame(frame)
bars_5m = resample_ohlcv(frame, "5min")

print(report)
print(bars_5m)
```

## Design Goals

- Deterministic behavior
- Clear validation failures
- Small, composable functions
- Strong typing and documentation
- No dependency on a specific broker or strategy
- Reusable in research, replay, and data-quality workflows

## License

MIT License
