import pandas as pd

from market_data_toolkit import validate_ohlcv_frame


def valid_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2026-01-01 09:30", periods=3, freq="1min", tz="UTC"),
            "open": [100, 101, 102],
            "high": [101, 102, 103],
            "low": [99, 100, 101],
            "close": [100.5, 101.5, 102.5],
            "volume": [10, 20, 30],
        }
    )


def test_valid_ohlcv_frame_passes():
    report = validate_ohlcv_frame(valid_frame())
    assert report.valid is True
    assert report.message == "ok"


def test_duplicate_timestamp_is_detected():
    frame = valid_frame()
    frame.loc[2, "timestamp"] = frame.loc[1, "timestamp"]
    report = validate_ohlcv_frame(frame)
    assert report.valid is False
    assert report.duplicate_timestamps == 1


def test_invalid_high_low_is_detected():
    frame = valid_frame()
    frame.loc[1, "high"] = 99
    report = validate_ohlcv_frame(frame)
    assert report.valid is False
    assert report.invalid_price_rows == 1
