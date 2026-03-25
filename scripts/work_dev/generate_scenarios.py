#!/usr/bin/env python3
"""
Expand baseline scenarios × runtimes × dimensions into a scenario matrix.

Backwards compatible with the existing simple baseline format:
- scenario_id
- failure_family
- required_checks
- severity

New supported fields per baseline YAML:
- description: str
- expected_failure_mode: str
- runtimes: [openclaw, cursor, ...]              # optional per-scenario override
- dimensions:
    receipt_state: [valid, missing, stale]
    topology: [local, remote]
- fixed:
    source: browser_extension
- exclude:
    - {runtime: cursor, topology: remote}
- variations:
    - id: stale_remote
      values: {receipt_state: stale, topology: remote}
      severity: high
      expected_failure_mode: stale continuity receipt on remote runtime
      required_checks: [continuity_required]
- tags: [continuity, boundary]
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BASE = REPO_ROOT / "docs" / "skill-work" / "work-dev" / "scenarios" / "baseline_scenarios"


@dataclass(frozen=True)
class ScenarioRow:
    scenario_id: str
    runtime: str
    variation: str
    expected_failure_mode: str
    required_checks: list[str]
    severity: str
    tags: list[str]
    values: dict[str, Any]

    def sort_key(self) -> tuple[str, str, str]:
        return (self.scenario_id, self.runtime, self.variation)


def _load_yaml(path: Path) -> dict[str, Any]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: scenario file must decode to a mapping")
    return raw


def _normalize_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _runtime_list(raw: dict[str, Any], default_runtimes: list[str]) -> list[str]:
    runtimes = _normalize_list(raw.get("runtimes"))
    if not runtimes:
        return default_runtimes
    out = [str(x).strip() for x in runtimes if str(x).strip()]
    return out or default_runtimes


def _dimensions(raw: dict[str, Any]) -> dict[str, list[Any]]:
    dims = raw.get("dimensions") or {}
    if not isinstance(dims, dict):
        raise ValueError("dimensions must be a mapping")
    out: dict[str, list[Any]] = {}
    for k, v in dims.items():
        vals = _normalize_list(v)
        if not vals:
            raise ValueError(f"dimension {k!r} must have at least one value")
        out[str(k)] = vals
    return out


def _fixed_values(raw: dict[str, Any]) -> dict[str, Any]:
    fixed = raw.get("fixed") or {}
    if not isinstance(fixed, dict):
        raise ValueError("fixed must be a mapping")
    return {str(k): v for k, v in fixed.items()}


def _exclude_rules(raw: dict[str, Any]) -> list[dict[str, Any]]:
    ex = raw.get("exclude") or []
    if not isinstance(ex, list):
        raise ValueError("exclude must be a list of mappings")
    out: list[dict[str, Any]] = []
    for item in ex:
        if not isinstance(item, dict):
            raise ValueError("exclude entries must be mappings")
        out.append({str(k): v for k, v in item.items()})
    return out


def _matches_rule(values: dict[str, Any], rule: dict[str, Any]) -> bool:
    for k, v in rule.items():
        if values.get(k) != v:
            return False
    return True


def _cartesian_rows(
    *,
    scenario_id: str,
    runtime: str,
    dims: dict[str, list[Any]],
    fixed: dict[str, Any],
) -> list[dict[str, Any]]:
    if not dims:
        values = dict(fixed)
        values["runtime"] = runtime
        return [values]

    keys = sorted(dims.keys())
    rows: list[dict[str, Any]] = []
    for combo in itertools.product(*(dims[k] for k in keys)):
        values = dict(fixed)
        values.update(dict(zip(keys, combo)))
        values["runtime"] = runtime
        rows.append(values)
    return rows


def _variation_id(values: dict[str, Any]) -> str:
    keys = [k for k in sorted(values.keys()) if k != "runtime"]
    if not keys:
        return "default"
    return "__".join(f"{k}={values[k]}" for k in keys)


def _base_failure_mode(raw: dict[str, Any]) -> str:
    return str(
        raw.get("expected_failure_mode")
        or raw.get("failure_family")
        or "scenario-triggered failure"
    ).strip()


def _base_required_checks(raw: dict[str, Any]) -> list[str]:
    return [str(x).strip() for x in _normalize_list(raw.get("required_checks")) if str(x).strip()]


def _base_tags(raw: dict[str, Any]) -> list[str]:
    return [str(x).strip() for x in _normalize_list(raw.get("tags")) if str(x).strip()]


def _expanded_variations(raw: dict[str, Any]) -> list[dict[str, Any]]:
    vars_ = raw.get("variations") or []
    if not vars_:
        return []
    if not isinstance(vars_, list):
        raise ValueError("variations must be a list")
    out: list[dict[str, Any]] = []
    for item in vars_:
        if not isinstance(item, dict):
            raise ValueError("variation entries must be mappings")
        values = item.get("values") or {}
        if not isinstance(values, dict):
            raise ValueError("variation.values must be a mapping")
        out.append(item)
    return out


def _build_rows_for_file(raw: dict[str, Any], default_runtimes: list[str]) -> list[ScenarioRow]:
    scenario_id = str(raw.get("scenario_id") or "").strip()
    if not scenario_id:
        raise ValueError("scenario_id is required")

    severity = str(raw.get("severity") or "medium").strip()
    base_mode = _base_failure_mode(raw)
    base_checks = _base_required_checks(raw)
    base_tags = _base_tags(raw)

    runtimes = _runtime_list(raw, default_runtimes)
    dims = _dimensions(raw)
    fixed = _fixed_values(raw)
    excludes = _exclude_rules(raw)
    explicit_variations = _expanded_variations(raw)

    rows: list[ScenarioRow] = []

    if explicit_variations:
        for rt in runtimes:
            for item in explicit_variations:
                values = dict(fixed)
                values.update(item.get("values") or {})
                values["runtime"] = rt
                if any(_matches_rule(values, rule) for rule in excludes):
                    continue
                row = ScenarioRow(
                    scenario_id=scenario_id,
                    runtime=rt,
                    variation=str(item.get("id") or _variation_id(values)),
                    expected_failure_mode=str(item.get("expected_failure_mode") or base_mode),
                    required_checks=[
                        str(x).strip()
                        for x in _normalize_list(item.get("required_checks") or base_checks)
                        if str(x).strip()
                    ],
                    severity=str(item.get("severity") or severity),
                    tags=sorted(
                        set(
                            base_tags
                            + [str(x).strip() for x in _normalize_list(item.get("tags")) if str(x).strip()]
                        )
                    ),
                    values={k: v for k, v in values.items() if k != "runtime"},
                )
                rows.append(row)
        return sorted(rows, key=lambda r: r.sort_key())

    for rt in runtimes:
        for values in _cartesian_rows(scenario_id=scenario_id, runtime=rt, dims=dims, fixed=fixed):
            if any(_matches_rule(values, rule) for rule in excludes):
                continue
            rows.append(
                ScenarioRow(
                    scenario_id=scenario_id,
                    runtime=rt,
                    variation=_variation_id(values),
                    expected_failure_mode=base_mode,
                    required_checks=base_checks,
                    severity=severity,
                    tags=base_tags,
                    values={k: v for k, v in values.items() if k != "runtime"},
                )
            )

    return sorted(rows, key=lambda r: r.sort_key())


def build_matrix(
    *,
    scenario_filter: str = "",
    runtimes: list[str],
    base_dir: Path = BASE,
) -> list[ScenarioRow]:
    rows: list[ScenarioRow] = []
    for path in sorted(base_dir.glob("*.yaml")):
        raw = _load_yaml(path)
        sid = str(raw.get("scenario_id") or path.stem)
        if scenario_filter and not sid.startswith(scenario_filter):
            continue
        rows.extend(_build_rows_for_file(raw, runtimes))
    return sorted(rows, key=lambda r: r.sort_key())


def render_markdown(rows: list[ScenarioRow]) -> str:
    lines = [
        "# Scenario Matrix\n\n",
        f"- Rows: **{len(rows)}**\n\n",
    ]
    last_sid = None
    for row in rows:
        if row.scenario_id != last_sid:
            lines.append(f"## {row.scenario_id}\n\n")
            last_sid = row.scenario_id
        vals = ", ".join(f"{k}={v}" for k, v in sorted(row.values.items())) or "default"
        checks = ", ".join(row.required_checks) or "_none_"
        tags = ", ".join(row.tags) or "_none_"
        lines.append(
            f"- **{row.runtime}** / `{row.variation}`"
            f" — {row.expected_failure_mode}"
            f" | severity={row.severity}"
            f" | values: {vals}"
            f" | checks: {checks}"
            f" | tags: {tags}\n"
        )
    return "".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate factorial scenario matrix rows.")
    ap.add_argument("--scenario", default="", help="Filter by scenario_id prefix")
    ap.add_argument(
        "--runtimes",
        default="openclaw,cursor,claude-code",
        help="Comma-separated runtime labels",
    )
    ap.add_argument("--format", default="json", choices=["json", "markdown"])
    args = ap.parse_args()

    runtimes = [x.strip() for x in args.runtimes.split(",") if x.strip()]
    rows = build_matrix(scenario_filter=args.scenario.strip(), runtimes=runtimes)

    if args.format == "markdown":
        sys.stdout.write(render_markdown(rows))
    else:
        payload = {
            "version": 2,
            "rows": [asdict(r) for r in rows],
        }
        sys.stdout.write(json.dumps(payload, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
