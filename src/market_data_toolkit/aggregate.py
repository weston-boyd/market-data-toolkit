from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from .exceptions import AggregationError
from .models import MarketBar, MarketTick


@dataclass
class _WorkingBar:
    start: datetime
    symbol: str
    timeframe: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    tick_count: int
    source: str

    def update(self, tick: MarketTick) -> None:
        self.high = max(self.high, tick.last)
        self.low = min(self.low, tick.last)
        self.close = tick.last
        self.volume += tick.volume or 0.0
        self.tick_count += 1

    def freeze(self) -> MarketBar:
        return MarketBar(
            timestamp=self.start,
            symbol=self.symbol,
            timeframe=self.timeframe,
            open=self.open,
            high=self.high,
            low=self.low,
            close=self.close,
            volume=self.volume,
            tick_count=self.tick_count,
            source=self.source,
        )


class TimeBarAggregator:
    """Build deterministic fixed-time OHLCV bars from normalized ticks."""

    def __init__(self, timeframe: str, seconds: int):
        if seconds < 1:
            raise AggregationError("seconds must be >= 1")
        self.timeframe = timeframe
        self.seconds = int(seconds)
        self._working: dict[str, _WorkingBar] = {}

    def update(self, tick: MarketTick) -> list[MarketBar]:
        bucket_start = self._bucket_start(tick.timestamp)
        current = self._working.get(tick.symbol)

        if current is None:
            self._working[tick.symbol] = self._new_working_bar(tick, bucket_start)
            return []

        if bucket_start < current.start:
            raise AggregationError("ticks must arrive in nondecreasing timestamp order")

        if bucket_start == current.start:
            current.update(tick)
            return []

        completed = current.freeze()
        self._working[tick.symbol] = self._new_working_bar(tick, bucket_start)
        return [completed]

    def flush(self) -> list[MarketBar]:
        completed = [working.freeze() for working in self._working.values()]
        self._working.clear()
        return sorted(completed, key=lambda bar: (bar.timestamp, bar.symbol))

    def _bucket_start(self, timestamp: datetime) -> datetime:
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        utc_timestamp = timestamp.astimezone(timezone.utc)
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
        elapsed = int((utc_timestamp - epoch).total_seconds())
        bucket_seconds = elapsed - (elapsed % self.seconds)
        return epoch + timedelta(seconds=bucket_seconds)

    def _new_working_bar(self, tick: MarketTick, start: datetime) -> _WorkingBar:
        return _WorkingBar(
            start=start,
            symbol=tick.symbol,
            timeframe=self.timeframe,
            open=tick.last,
            high=tick.last,
            low=tick.last,
            close=tick.last,
            volume=tick.volume or 0.0,
            tick_count=1,
            source=tick.source,
        )
