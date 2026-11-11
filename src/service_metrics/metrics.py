"""Pure functions that compute per-department metrics from Request rows."""

from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from statistics import median

from service_metrics.load import Request


@dataclass(frozen=True)
class DepartmentMetrics:
    department: str
    count: int
    pct_closed: float
    median_days_to_close: float | None


def days_to_close(request: Request, today: date | None = None) -> int:
    """Days between opening and closing. Open requests are measured to today."""
    end = request.closed_at or (today or date.today())
    return (end - request.opened_at).days


def pct_closed(requests: list[Request]) -> float:
    if not requests:
        return 0.0
    closed = sum(1 for r in requests if r.closed_at is not None)
    return round(100.0 * closed / len(requests), 1)


def median_days_to_close(
    requests: list[Request], today: date | None = None
) -> float | None:
    durations = [days_to_close(r, today) for r in requests]
    return float(median(durations)) if durations else None


def by_department(
    requests: list[Request], today: date | None = None
) -> list[DepartmentMetrics]:
    groups: dict[str, list[Request]] = defaultdict(list)
    for r in requests:
        groups[r.department].append(r)
    return [
        DepartmentMetrics(
            department=dept,
            count=len(rows),
            pct_closed=pct_closed(rows),
            median_days_to_close=median_days_to_close(rows, today),
        )
        for dept, rows in sorted(groups.items())
    ]
