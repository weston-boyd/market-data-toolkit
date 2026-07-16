from market_data_toolkit import check_tick_csv


def test_tick_csv_integrity_passes(tmp_path):
    path = tmp_path / "ticks.csv"
    path.write_text(
        "timestamp,symbol,last,source\n"
        "2026-01-01T09:30:00+00:00,MGC,2100.0,test\n"
        "2026-01-01T09:30:01+00:00,MGC,2100.5,test\n",
        encoding="utf-8",
    )

    report = check_tick_csv(path)
    assert report.valid is True
    assert report.rows == 2


def test_tick_csv_integrity_detects_missing_columns(tmp_path):
    path = tmp_path / "ticks.csv"
    path.write_text("timestamp,symbol\n2026-01-01T09:30:00+00:00,MGC\n", encoding="utf-8")
    report = check_tick_csv(path)
    assert report.valid is False
    assert "missing columns" in report.message
