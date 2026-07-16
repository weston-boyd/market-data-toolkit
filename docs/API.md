# Public API

## Models

- `MarketTick`: immutable normalized tick record.
- `MarketBar`: immutable OHLCV bar record.

## Normalization

- `TickNormalizer.from_mapping(...)`: converts loose vendor payloads to `MarketTick`.

## Aggregation

- `TimeBarAggregator.update(...)`: consumes ticks and emits completed bars.
- `TimeBarAggregator.flush()`: emits remaining working bars.

## Validation

- `validate_ohlcv_frame(...)`: returns a structured validation report.
- `summarize_frame_quality(...)`: returns a serializable summary.

## File Integrity

- `check_tick_csv(...)`: performs lightweight CSV replay-readiness checks.

## Resampling

- `resample_ohlcv(...)`: creates higher-timeframe OHLCV bars.

## Exceptions

- `MarketDataToolkitError`
- `NormalizationError`
- `AggregationError`
- `ValidationError`
