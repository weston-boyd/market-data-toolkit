from datetime import timezone

from market_data_toolkit import TickNormalizer


def test_normalizer_accepts_vendor_aliases():
    normalizer = TickNormalizer("example_vendor")
    tick = normalizer.from_mapping(
        {
            "DateTime": "2026-01-01 09:30:00-05:00",
            "Symbol": "mgc",
            "Last": "2100.5",
            "Bid": "2100.4",
            "Ask": "2100.6",
            "Volume": "2",
        }
    )

    assert tick.symbol == "MGC"
    assert tick.last == 2100.5
    assert tick.timestamp.tzinfo == timezone.utc
    assert tick.bid == 2100.4
