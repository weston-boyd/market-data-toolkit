from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


REQUIRED_OHLCV_COLUMNS = ("timestamp", "open", "high", "low", "close", "volume")


@dataclass(frozen=True)
class FrameValidationReport:
    rows: int
    valid: bool
    missing_columns: tuple[str, ...]
    duplicate_timestamps: int
    out_of_order_timestamps: int
    missing_values: int
    invalid_price_rows: int
    nonpositive_volume_rows: int
    message: str


def validate_ohlcv_frame(frame: pd.DataFrame) -> FrameValidationReport:
    """Validate a canonical OHLCV DataFrame without mutating the input."""
    missing_columns = tuple(column for column in REQUIRED_OHLCV_COLUMNS if column not in frame.columns)
    if missing_columns:
        return FrameValidationReport(
            rows=len(frame),
            valid=False,
            missing_columns=missing_columns,
            duplicate_timestamps=0,
            out_of_order_timestamps=0,
            missing_values=0,
            invalid_price_rows=0,
            nonpositive_volume_rows=0,
            message=f"missing required columns: {list(missing_columns)}",
        )

    work = frame.loc[:, REQUIRED_OHLCV_COLUMNS].copy()
    work["timestamp"] = pd.to_datetime(work["timestamp"], errors="coerce", utc=True)

    numeric_columns = ["open", "high", "low", "close", "volume"]
    for column in numeric_columns:
        work[column] = pd.to_numeric(work[column], errors="coerce")

    missing_values = int(work.isna().sum().sum())
    duplicate_timestamps = int(work["timestamp"].duplicated().sum())
    out_of_order_timestamps = int((work["timestamp"].diff().dropna() < pd.Timedelta(0)).sum())

    invalid_price_mask = (
        (work["high"] < work["low"])
        | (work["high"] < work[["open", "close"]].max(axis=1))
        | (work["low"] > work[["open", "close"]].min(axis=1))
        | (work[["open", "high", "low", "close"]] <= 0).any(axis=1)
    )
    invalid_price_rows = int(invalid_price_mask.fillna(True).sum())
    nonpositive_volume_rows = int((work["volume"] < 0).fillna(False).sum())

    valid = all(
        value == 0
        for value in (
            duplicate_timestamps,
            out_of_order_timestamps,
            missing_values,
            invalid_price_rows,
            nonpositive_volume_rows,
        )
    )
    message = "ok" if valid else "one or more data-quality checks failed"

    return FrameValidationReport(
        rows=len(work),
        valid=valid,
        missing_columns=missing_columns,
        duplicate_timestamps=duplicate_timestamps,
        out_of_order_timestamps=out_of_order_timestamps,
        missing_values=missing_values,
        invalid_price_rows=invalid_price_rows,
        nonpositive_volume_rows=nonpositive_volume_rows,
        message=message,
    )


def summarize_frame_quality(frame: pd.DataFrame) -> dict[str, object]:
    """Return a compact, serializable data-quality summary."""
    report = validate_ohlcv_frame(frame)
    timestamps = (
        pd.to_datetime(frame["timestamp"], errors="coerce", utc=True)
        if "timestamp" in frame.columns
        else pd.Series(dtype="datetime64[ns, UTC]")
    )
    return {
        "rows": report.rows,
        "valid": report.valid,
        "message": report.message,
        "missing_columns": list(report.missing_columns),
        "duplicate_timestamps": report.duplicate_timestamps,
        "out_of_order_timestamps": report.out_of_order_timestamps,
        "missing_values": report.missing_values,
        "invalid_price_rows": report.invalid_price_rows,
        "nonpositive_volume_rows": report.nonpositive_volume_rows,
        "start_time": None if timestamps.empty or timestamps.isna().all() else timestamps.min().isoformat(),
        "end_time": None if timestamps.empty or timestamps.isna().all() else timestamps.max().isoformat(),
    }
