from datetime import datetime, timezone

import pytest

from market_data_toolkit import MarketBar, MarketTick


def test_market_tick_normalizes_valid_data():
    tick = MarketTick(
        timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
        symbol="MGC",
        last=2100.5,
    )
    assert tick.symbol == "MGC"
    assert tick.last == 2100.5


def test_market_bar_rejects_impossible_ohlc():
    with pytest.raises(ValueError):
        MarketBar(
            timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
            symbol="MGC",
            timeframe="1m",
            open=100,
            high=99,
            low=98,
            close=100,
        )
