from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CsvIntegrityReport:
    path: Path
    rows: int
    first_timestamp: str | None
    last_timestamp: str | None
    valid: bool
    message: str


def check_tick_csv(
    path: str | Path,
    *,
    required_columns: set[str] | None = None,
) -> CsvIntegrityReport:
    """Perform lightweight replay-readiness checks on a tick CSV."""
    file_path = Path(path)
    columns = required_columns or {"timestamp", "symbol", "last", "source"}

    if not file_path.exists():
        return CsvIntegrityReport(file_path, 0, None, None, False, "file does not exist")

    rows = 0
    first_timestamp: str | None = None
    last_timestamp: str | None = None
    previous_timestamp: str | None = None

    try:
        with file_path.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            missing = columns.difference(reader.fieldnames or [])
            if missing:
                return CsvIntegrityReport(
                    file_path, 0, None, None, False, f"missing columns: {sorted(missing)}"
                )

            for row in reader:
                timestamp = (row.get("timestamp") or "").strip()
                if not timestamp:
                    return CsvIntegrityReport(
                        file_path, rows, first_timestamp, last_timestamp, False, "empty timestamp"
                    )
                if previous_timestamp is not None and timestamp < previous_timestamp:
                    return CsvIntegrityReport(
                        file_path, rows, first_timestamp, last_timestamp, False, "timestamps out of order"
                    )
                if first_timestamp is None:
                    first_timestamp = timestamp
                last_timestamp = timestamp
                previous_timestamp = timestamp
                rows += 1
    except (OSError, csv.Error, UnicodeError) as error:
        return CsvIntegrityReport(
            file_path, rows, first_timestamp, last_timestamp, False, f"read error: {error}"
        )

    if rows == 0:
        return CsvIntegrityReport(file_path, 0, None, None, False, "file contains no data rows")
    return CsvIntegrityReport(file_path, rows, first_timestamp, last_timestamp, True, "ok")
