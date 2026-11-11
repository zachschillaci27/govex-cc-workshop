from abc import ABC, abstractmethod

from service_metrics.metrics import DepartmentMetrics

REPORT_CONFIG = {
    "format": "text",
    "header": True,
    "separator": " | ",
    "precision": 1,
    "null_marker": "-",
}

_REGISTRY: dict[str, type["ReportStrategy"]] = {}


def register(name):
    def wrap(cls):
        _REGISTRY[name] = cls
        return cls

    return wrap


class ReportStrategy(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def render_row(self, m: DepartmentMetrics) -> str: ...

    def render_header(self) -> str:
        return self.config["separator"].join(
            ["department", "count", "closed%", "median_days"]
        )

    def render(self, rows: list[DepartmentMetrics]) -> str:
        lines = [self.render_header()] if self.config.get("header") else []
        for m in rows:
            lines.append(self.render_row(m))
        return "\n".join(lines)


@register("text")
class TextReportStrategy(ReportStrategy):
    def render_row(self, m: DepartmentMetrics) -> str:
        p = self.config["precision"]
        med = (
            self.config["null_marker"]
            if m.median_days_to_close is None
            else f"{m.median_days_to_close:.{p}f}"
        )
        return self.config["separator"].join(
            [m.department, str(m.count), f"{m.pct_closed:.{p}f}", med]
        )


class ReportFactory:
    @staticmethod
    def create(config=None) -> ReportStrategy:
        cfg = dict(REPORT_CONFIG)
        if config:
            cfg.update(config)
        cls = _REGISTRY.get(cfg["format"])
        if cls is None:
            raise ValueError(f"unknown report format: {cfg['format']}")
        return cls(cfg)


def build_report(rows: list[DepartmentMetrics], config=None) -> str:
    return ReportFactory.create(config).render(rows)
