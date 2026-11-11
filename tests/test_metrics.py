"""Tests for per-department 311 metrics."""

from datetime import date

from service_metrics.load import Request, load_requests
from service_metrics.metrics import by_department, days_to_close, pct_closed


def req(dept, opened, closed=None):
    return Request(
        id="x",
        department=dept,
        opened_at=date.fromisoformat(opened),
        closed_at=date.fromisoformat(closed) if closed else None,
        status="closed" if closed else "open",
    )


def test_load_requests_parses_dates_and_open_rows():
    rows = load_requests("data/sample_311.csv")
    assert len(rows) == 25
    assert rows[0].opened_at == date(2024, 3, 1)
    assert rows[3].closed_at is None


def test_days_to_close_for_closed_request():
    assert days_to_close(req("Parks", "2024-03-01", "2024-03-04")) == 3


def test_pct_closed_rounds_to_one_decimal():
    rows = [req("Parks", "2024-03-01", "2024-03-02")] * 2 + [req("Parks", "2024-03-01")]
    assert pct_closed(rows) == 66.7


def test_pct_closed_empty_is_zero():
    assert pct_closed([]) == 0.0


def test_by_department_groups_and_sorts():
    rows = [
        req("Water", "2024-03-01", "2024-03-02"),
        req("Parks", "2024-03-01", "2024-03-05"),
        req("Parks", "2024-03-02", "2024-03-04"),
    ]
    result = by_department(rows)
    assert [m.department for m in result] == ["Parks", "Water"]
    assert result[0].count == 2
    assert result[0].median_days_to_close == 3.0


def test_median_days_for_all_closed_requests():
    rows = [
        req("Parks", "2024-03-01", "2024-03-02"),
        req("Parks", "2024-03-01", "2024-03-04"),
        req("Parks", "2024-03-01", "2024-03-10"),
    ]
    assert by_department(rows)[0].median_days_to_close == 3.0
