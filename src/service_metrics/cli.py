"""Command line entry point: print a per-department metrics table."""

import sys

from service_metrics.load import load_requests
from service_metrics.metrics import by_department


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("usage: python -m service_metrics <requests.csv>", file=sys.stderr)
        return 2
    rows = by_department(load_requests(args[0]))
    print(f"{'department':<12} {'count':>5} {'closed%':>8} {'median_days':>12}")
    for m in rows:
        med = "-" if m.median_days_to_close is None else f"{m.median_days_to_close:.1f}"
        print(f"{m.department:<12} {m.count:>5} {m.pct_closed:>8.1f} {med:>12}")
    return 0
