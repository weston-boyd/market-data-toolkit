# Quickstart

## Install for Development

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Validate an OHLCV DataFrame

```python
import pandas as pd
from market_data_toolkit import validate_ohlcv_frame

frame = pd.read_csv("bars.csv")
report = validate_ohlcv_frame(frame)

if not report.valid:
    raise RuntimeError(report.message)
```

## Normalize a Vendor Tick

```python
from market_data_toolkit import TickNormalizer

normalizer = TickNormalizer("vendor_name")
tick = normalizer.from_mapping(
    {
        "DateTime": "2026-01-01T09:30:00Z",
        "Symbol": "MGC",
        "Last": 2100.5,
        "Volume": 2,
    }
)
```

## Aggregate Ticks into Bars

```python
from market_data_toolkit import TimeBarAggregator

aggregator = TimeBarAggregator("1m", 60)
completed_bars = aggregator.update(tick)
```
