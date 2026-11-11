# service-metrics

Per-department metrics for city 311 service requests: request count, percent closed, median days to close.

    make install
    make run
    make test
    make lint

Input is a CSV with columns `id, department, opened_at, closed_at, status`. Dates are ISO (YYYY-MM-DD); `closed_at` is empty for open requests.

Open `dashboard.html` in a browser for a per-department view of the same data.
