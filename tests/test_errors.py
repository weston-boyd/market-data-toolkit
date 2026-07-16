from datetime import datetime, timezone

import pandas as pd
import pytest

from market_data_toolkit import (
    AggregationError,
    MarketTick,
    NormalizationError,
    TickNormalizer,
    TimeBarAggregator,
    ValidationError,
    resample_ohlcv,
)


def test_normalizer_rejects_incomplete_payload():
    with pytest.raises(NormalizationError):
        TickNormalizer("vendor").from_mapping({"symbol": "MGC"})


def test_aggregator_rejects_out_of_order_ticks():
    aggregator = TimeBarAggregator("1m", 60)
    later = MarketTick(datetime(2026, 1, 1, 9, 31, tzinfo=timezone.utc), "MGC", 2101.0)
    earlier = MarketTick(datetime(2026, 1, 1, 9, 30, tzinfo=timezone.utc), "MGC", 2100.0)

    aggregator.update(later)
    with pytest.raises(AggregationError):
        aggregator.update(earlier)


def test_resample_rejects_invalid_frame():
    frame = pd.DataFrame({"timestamp": ["2026-01-01T09:30:00Z"], "open": [100]})
    with pytest.raises(ValidationError):
        resample_ohlcv(frame, "5min")
