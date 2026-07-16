import pandas as pd

from market_data_toolkit import resample_ohlcv


def test_resample_ohlcv_to_five_minutes():
    frame = pd.DataFrame(
        {
            "timestamp": pd.date_range("2026-01-01 09:30", periods=5, freq="1min", tz="UTC"),
            "open": [100, 101, 102, 103, 104],
            "high": [101, 102, 103, 104, 105],
            "low": [99, 100, 101, 102, 103],
            "close": [100.5, 101.5, 102.5, 103.5, 104.5],
            "volume": [1, 2, 3, 4, 5],
        }
    )

    result = resample_ohlcv(frame, "5min")
    assert len(result) == 1
    assert result.iloc[0]["open"] == 100
    assert result.iloc[0]["high"] == 105
    assert result.iloc[0]["low"] == 99
    assert result.iloc[0]["close"] == 104.5
    assert result.iloc[0]["volume"] == 15
