# Design Notes

## Scope

Market Data Toolkit is intentionally broker-agnostic and strategy-agnostic. It provides small components for normalizing and validating financial time-series data before that data enters research, replay, or machine-learning workflows.

## Package Boundaries

- `models.py`: immutable canonical market-data objects
- `normalize.py`: vendor payload conversion and UTC handling
- `aggregate.py`: deterministic fixed-time bar construction
- `validate.py`: DataFrame-level OHLCV quality checks
- `integrity.py`: lightweight file-level CSV checks
- `resample.py`: higher-timeframe OHLCV construction

## Excluded by Design

- Trading strategies
- Signal generation
- Broker credentials
- Order submission
- Position sizing
- Proprietary research results
