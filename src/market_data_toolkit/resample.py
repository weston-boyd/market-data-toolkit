from __future__ import annotations

import pandas as pd

from .exceptions import ValidationError
from .validate import REQUIRED_OHLCV_COLUMNS, validate_ohlcv_frame


def resample_ohlcv(frame: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """Resample canonical OHLCV data to a higher fixed timeframe."""
    report = validate_ohlcv_frame(frame)
    if not report.valid:
        raise ValidationError(f"cannot resample invalid OHLCV data: {report}")

    work = frame.loc[:, REQUIRED_OHLCV_COLUMNS].copy()
    work["timestamp"] = pd.to_datetime(work["timestamp"], utc=True)
    work = work.sort_values("timestamp").set_index("timestamp")

    result = (
        work.resample(timeframe, label="left", closed="left")
        .agg(
            {
                "open": "first",
                "high": "max",
                "low": "min",
                "close": "last",
                "volume": "sum",
            }
        )
        .dropna(subset=["open", "high", "low", "close"])
        .reset_index()
    )
    return result
