#!/usr/bin/env python3
"""
Load alpha-school-benchmarks.yaml for use by export_curriculum and other tools.

Returns target_market, success_metrics, benchmarks, and derived fields (e.g. screen_time_target_minutes).

Usage:
    from scripts.load_alpha_school_benchmarks import load_alpha_school_benchmarks
    data = load_alpha_school_benchmarks()
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ALPHA_SCHOOL_YAML = REPO_ROOT / "docs" / "skill-work" / "skill-work-alpha-school" / "alpha-school-benchmarks.yaml"


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _yaml_list(content: str, key: str) -> list[str]:
    """Extract YAML list: key: \\n  - item."""
    pattern = rf"{key}:\s*\n((?:\s+-\s+[^\n]+\n?)+)"
    m = re.search(pattern, content)
    if not m:
        return []
    lines = m.group(1).strip().split("\n")
    return [re.sub(r"^\s*-\s+", "", ln).split("#")[0].strip().strip('"\'') for ln in lines if ln.strip()]


def _yaml_value(content: str, key: str) -> str | int | None:
    """Extract YAML scalar (string or int)."""
    pattern = rf"{key}:\s*(.+?)(?:\n|$)"
    m = re.search(pattern, content)
    if not m:
        return None
    val = m.group(1).split("#")[0].strip().strip('"\'')
    if val.isdigit():
        return int(val)
    return val


def _benchmark_value(content: str, benchmark: str, key: str) -> str | int | None:
    """Extract value from benchmarks.benchmark.key (e.g. screen_time_daily.minutes)."""
    pattern = rf"{re.escape(benchmark)}:\s*\n\s+{re.escape(key)}:\s*(.+?)(?:\n|$)"
    m = re.search(pattern, content)
    if not m:
        return None
    val = m.group(1).split("#")[0].strip().strip('"\'')
    if val.isdigit():
        return int(val)
    return val


def _benchmark_description(content: str, benchmark: str) -> str | None:
    """Extract description from a benchmark section."""
    pattern = rf"{re.escape(benchmark)}:.*?description:\s*[\"']?([^\"'\n]+)[\"']?(?:\n|$)"
    m = re.search(pattern, content, re.DOTALL)
    return m.group(1).strip().strip('"\'') if m else None


def load_alpha_school_benchmarks() -> dict:
    """
    Load alpha-school-benchmarks.yaml. Returns dict with target_market, success_metrics,
    benchmarks (raw), screen_time_target_minutes, value_creation_description, etc.
    """
    content = _read(ALPHA_SCHOOL_YAML)
    if not content:
        return {}

    target_market = _yaml_list(content, "target_market")
    success_metrics = _yaml_list(content, "success_metrics")

    # Extract screen_time_daily.minutes
    screen_minutes = _benchmark_value(content, "screen_time_daily", "minutes") or 120

    # Extract value_creation.description
    value_desc = _benchmark_description(content, "value_creation")

    return {
        "target_market": target_market or ["alpha_school_families", "cant_afford_alpha", "homeschool", "self_motivated_adults"],
        "success_metrics": success_metrics or ["screen_time_daily", "sat_metrics", "state_tests", "engagement", "value_creation"],
        "screen_time_target_minutes": screen_minutes or 120,
        "value_creation_description": value_desc,
        "id": _yaml_value(content, "id"),
        "confidence": _yaml_value(content, "confidence"),
    }


if __name__ == "__main__":
    import json
    data = load_alpha_school_benchmarks()
    print(json.dumps(data, indent=2))
