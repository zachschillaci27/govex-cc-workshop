"""Command line entry point: print a per-department metrics table, optionally write dashboard.html."""

import json
import sys
from pathlib import Path

from service_metrics.load import Request, load_requests
from service_metrics.metrics import (
    DepartmentMetrics,
    by_department,
    median_days_to_close,
)

TEMPLATE = Path(__file__).with_name("dashboard_template.html")


def dashboard_html(requests: list[Request], rows: list[DepartmentMetrics]) -> str:
    """Fill the dashboard template with computed metrics as a JSON object."""
    open_count = sum(1 for r in requests if r.closed_at is None)
    metrics = {
        "total": len(requests),
        "open": open_count,
        "median_days": median_days_to_close(requests),
        "departments": [
            {
                "department": m.department,
                "count": m.count,
                "open": m.count - round(m.count * m.pct_closed / 100),
                "pct_closed": m.pct_closed,
                "median_days": m.median_days_to_close,
            }
            for m in rows
        ],
    }
    return TEMPLATE.read_text().replace("__METRICS__", json.dumps(metrics))


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    html_out = None
    if "--html" in args:
        i = args.index("--html")
        html_out = args[i + 1] if i + 1 < len(args) else None
        args = args[:i] + args[i + 2 :]
    if len(args) != 1:
        print(
            "usage: python -m service_metrics <requests.csv> [--html out.html]",
            file=sys.stderr,
        )
        return 2
    requests = load_requests(args[0])
    rows = by_department(requests)
    print(f"{'department':<12} {'count':>5} {'closed%':>8} {'median_days':>12}")
    for m in rows:
        med = "-" if m.median_days_to_close is None else f"{m.median_days_to_close:.1f}"
        print(f"{m.department:<12} {m.count:>5} {m.pct_closed:>8.1f} {med:>12}")
    if html_out:
        Path(html_out).write_text(dashboard_html(requests, rows))
        print(f"wrote {html_out}")
    return 0
