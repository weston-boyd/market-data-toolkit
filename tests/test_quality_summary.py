import pandas as pd

from market_data_toolkit import summarize_frame_quality


def test_quality_summary_is_serializable_and_reports_time_span():
    frame = pd.DataFrame(
        {
            "timestamp": pd.date_range("2026-01-01", periods=2, freq="1min", tz="UTC"),
            "open": [100, 101],
            "high": [101, 102],
            "low": [99, 100],
            "close": [100.5, 101.5],
            "volume": [1, 2],
        }
    )

    summary = summarize_frame_quality(frame)

    assert summary["valid"] is True
    assert summary["rows"] == 2
    assert summary["start_time"].startswith("2026-01-01")
    assert summary["end_time"].startswith("2026-01-01")
