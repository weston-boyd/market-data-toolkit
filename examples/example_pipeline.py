from datetime import datetime, timedelta, timezone

import pandas as pd

from market_data_toolkit import (
    MarketTick,
    TimeBarAggregator,
    resample_ohlcv,
    summarize_frame_quality,
)


def main() -> None:
    aggregator = TimeBarAggregator("1m", 60)
    start = datetime(2026, 1, 1, 9, 30, tzinfo=timezone.utc)

    completed = []
    for offset, price in enumerate([100.0, 100.5, 101.0, 100.75, 101.25, 101.5]):
        tick = MarketTick(
            timestamp=start + timedelta(seconds=offset * 30),
            symbol="DEMO",
            last=price,
            volume=1,
            source="synthetic",
        )
        completed.extend(aggregator.update(tick))

    completed.extend(aggregator.flush())

    frame = pd.DataFrame(
        {
            "timestamp": [bar.timestamp for bar in completed],
            "open": [bar.open for bar in completed],
            "high": [bar.high for bar in completed],
            "low": [bar.low for bar in completed],
            "close": [bar.close for bar in completed],
            "volume": [bar.volume for bar in completed],
        }
    )

    print("Data quality:")
    print(summarize_frame_quality(frame))
    print("\nResampled bars:")
    print(resample_ohlcv(frame, "2min"))


if __name__ == "__main__":
    main()
