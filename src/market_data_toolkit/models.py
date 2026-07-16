from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class MarketTick:
    """Canonical normalized market tick."""

    timestamp: datetime
    symbol: str
    last: float
    bid: float | None = None
    ask: float | None = None
    volume: float | None = None
    source: str = "unknown"
    sequence: int | None = None

    def __post_init__(self) -> None:
        if not self.symbol.strip():
            raise ValueError("symbol must not be empty")
        if self.last <= 0:
            raise ValueError("last price must be positive")


@dataclass(frozen=True)
class MarketBar:
    """Canonical fixed-time OHLCV bar."""

    timestamp: datetime
    symbol: str
    timeframe: str
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0
    tick_count: int = 0
    source: str = "unknown"

    def __post_init__(self) -> None:
        if self.high < self.low:
            raise ValueError("high must be greater than or equal to low")
        if self.high < max(self.open, self.close):
            raise ValueError("high must be greater than or equal to open and close")
        if self.low > min(self.open, self.close):
            raise ValueError("low must be less than or equal to open and close")

    @property
    def range(self) -> float:
        return self.high - self.low

    @property
    def is_bullish(self) -> bool:
        return self.close > self.open

    @property
    def is_bearish(self) -> bool:
        return self.close < self.open
