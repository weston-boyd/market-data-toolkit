from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import pandas as pd

from .models import MarketTick


class TickNormalizer:
    """Convert loose broker/vendor payloads into canonical UTC MarketTick objects."""

    def __init__(self, source_name: str):
        source_name = source_name.strip()
        if not source_name:
            raise ValueError("source_name must not be empty")
        self.source_name = source_name

    def from_mapping(
        self,
        payload: dict[str, Any],
        *,
        default_symbol: str | None = None,
        sequence: int | None = None,
    ) -> MarketTick:
        timestamp = self._first(payload, "timestamp", "DateTime", "datetime", "time")
        symbol = self._first(payload, "symbol", "Symbol", "instrument", "contract") or default_symbol
        last = self._first(payload, "last", "Last", "price", "close")

        if timestamp is None or symbol is None or last is None:
            raise ValueError("payload must include timestamp, symbol, and last/price")

        return MarketTick(
            timestamp=self._parse_timestamp(timestamp),
            symbol=str(symbol).strip().upper(),
            last=float(last),
            bid=self._optional_float(self._first(payload, "bid", "Bid")),
            ask=self._optional_float(self._first(payload, "ask", "Ask")),
            volume=self._optional_float(self._first(payload, "volume", "Volume", "size", "Size")),
            source=self.source_name,
            sequence=sequence,
        )

    @staticmethod
    def _first(payload: dict[str, Any], *names: str) -> Any:
        for name in names:
            if name in payload:
                return payload[name]
        return None

    @staticmethod
    def _parse_timestamp(value: Any) -> datetime:
        if isinstance(value, datetime):
            timestamp = value
        else:
            timestamp = pd.to_datetime(value, errors="raise").to_pydatetime()

        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        return timestamp.astimezone(timezone.utc)

    @staticmethod
    def _optional_float(value: Any) -> float | None:
        if value is None or pd.isna(value):
            return None
        return float(value)
