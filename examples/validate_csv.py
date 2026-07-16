from pathlib import Path

import pandas as pd

from market_data_toolkit import summarize_frame_quality


def main() -> None:
    path = Path("sample_bars.csv")
    if not path.exists():
        frame = pd.DataFrame(
            {
                "timestamp": pd.date_range("2026-01-01", periods=3, freq="1min", tz="UTC"),
                "open": [100, 101, 102],
                "high": [101, 102, 103],
                "low": [99, 100, 101],
                "close": [100.5, 101.5, 102.5],
                "volume": [10, 20, 30],
            }
        )
    else:
        frame = pd.read_csv(path)

    for key, value in summarize_frame_quality(frame).items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
