from datetime import datetime, timezone

from market_data_toolkit import MarketTick, TimeBarAggregator


def test_time_bar_aggregator_builds_completed_bar():
    aggregator = TimeBarAggregator("1s", 1)
    first = MarketTick(
        datetime(2026, 1, 1, 9, 30, 0, tzinfo=timezone.utc),
        "MGC",
        2100.0,
        volume=1,
    )
    second = MarketTick(
        datetime(2026, 1, 1, 9, 30, 0, 500000, tzinfo=timezone.utc),
        "MGC",
        2101.0,
        volume=2,
    )
    third = MarketTick(
        datetime(2026, 1, 1, 9, 30, 1, tzinfo=timezone.utc),
        "MGC",
        2102.0,
        volume=3,
    )

    assert aggregator.update(first) == []
    assert aggregator.update(second) == []
    completed = aggregator.update(third)

    assert len(completed) == 1
    bar = completed[0]
    assert bar.open == 2100.0
    assert bar.high == 2101.0
    assert bar.low == 2100.0
    assert bar.close == 2101.0
    assert bar.volume == 3
    assert bar.tick_count == 2
