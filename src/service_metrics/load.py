"""Read 311 service requests from a CSV file into plain dataclass rows."""

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class Request:
    id: str
    department: str
    opened_at: date
    closed_at: date | None
    status: str


def load_requests(path: str | Path) -> list[Request]:
    """Parse the CSV at `path`. An empty closed_at means the request is open."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = []
        for row in csv.DictReader(f):
            closed = row["closed_at"].strip()
            rows.append(
                Request(
                    id=row["id"],
                    department=row["department"],
                    opened_at=date.fromisoformat(row["opened_at"]),
                    closed_at=date.fromisoformat(closed) if closed else None,
                    status=row["status"],
                )
            )
    return rows
