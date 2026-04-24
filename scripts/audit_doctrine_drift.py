#!/usr/bin/env python3
"""
Read-only doctrine drift audit.

Checks a small set of high-leverage doctrine invariants declared in
config/doctrine-rules.v1.json and reports violations with file context.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = REPO_ROOT / "config" / "doctrine-rules.v1.json"


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _get_nested(data: Any, dotted_path: str) -> Any:
    cur = data
    for part in dotted_path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _iter_target_files(repo_root: Path, patterns: list[str]) -> list[Path]:
    out: set[Path] = set()
    for pattern in patterns:
        for path in repo_root.glob(pattern):
            if path.is_file():
                out.add(path.resolve())
    return sorted(out)


def _line_number(text: str, needle: str) -> int | None:
    for idx, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return idx
    return None


def _applies_when(data: dict[str, Any], clause: dict[str, Any] | None) -> bool:
    if not clause:
        return True
    all_keys = clause.get("allKeys", [])
    for key in all_keys:
        if _get_nested(data, key) is None:
            return False
    field_equals = clause.get("fieldEquals", {})
    for key, expected in field_equals.items():
        if _get_nested(data, key) != expected:
            return False
    return True


def _violation(rule_id: str, path: Path, message: str, *, line: int | None = None) -> dict[str, Any]:
    payload = {
        "ruleId": rule_id,
        "path": path.as_posix(),
        "message": message,
    }
    if line is not None:
        payload["line"] = line
    return payload


def _protected_target_from_expr(
    expr: str, protected_names: set[str], protected_exact_paths: set[str]
) -> str | None:
    normalized = expr.replace("\\", "/")
    for exact in protected_exact_paths:
        if exact in normalized:
            return exact
    for name in protected_names:
        quoted = f'"{name}"'
        squoted = f"'{name}'"
        if quoted in expr or squoted in expr:
            return name
    return None


def _audit_python_canonical_writer_allowlist(
    repo_root: Path, rule: dict[str, Any]
) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    approved = set(rule.get("approvedWriters", []))
    protected_names = set(rule.get("protectedNames", []))
    protected_exact_paths = set(rule.get("protectedExactPaths", []))

    assign_re = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$")
    write_re_template = r"\b{var}\.write_text\("
    open_re_template = r"open\(\s*{var}\s*,\s*['\"](?:w|a|x)['\"]"

    for path in _iter_target_files(repo_root, rule["targets"]):
        rel = path.relative_to(repo_root).as_posix()
        if rel in approved:
            continue
        text = path.read_text(encoding="utf-8")
        var_targets: dict[str, tuple[str, int]] = {}
        lines = text.splitlines()
        for idx, line in enumerate(lines, start=1):
            match = assign_re.match(line)
            if match:
                var_name, expr = match.groups()
                target = _protected_target_from_expr(
                    expr, protected_names, protected_exact_paths
                )
                if target is not None:
                    var_targets[var_name] = (target, idx)
                elif var_name in var_targets:
                    del var_targets[var_name]

            for var_name, (target, assigned_at) in var_targets.items():
                if re.search(write_re_template.format(var=re.escape(var_name)), line):
                    violations.append(
                        _violation(
                            rule["id"],
                            path.relative_to(repo_root),
                            f"non-approved script writes protected Record target via {var_name} -> {target} (assigned line {assigned_at})",
                            line=idx,
                        )
                    )
                if re.search(open_re_template.format(var=re.escape(var_name)), line):
                    violations.append(
                        _violation(
                            rule["id"],
                            path.relative_to(repo_root),
                            f"non-approved script opens protected Record target for write via {var_name} -> {target} (assigned line {assigned_at})",
                            line=idx,
                        )
                    )
    return violations


def _audit_json_field_const(repo_root: Path, rule: dict[str, Any]) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    for path in _iter_target_files(repo_root, rule["targets"]):
        rel = path.relative_to(repo_root)
        try:
            data = _load_json(path)
        except json.JSONDecodeError as exc:
            violations.append(
                _violation(rule["id"], rel, f"invalid JSON while auditing rule: {exc}")
            )
            continue
        if not _applies_when(data, rule.get("appliesWhen")):
            continue
        for dotted_path, expected in rule.get("expected", {}).items():
            actual = _get_nested(data, dotted_path)
            if actual != expected:
                violations.append(
                    _violation(
                        rule["id"],
                        rel,
                        f"{dotted_path} must be {expected!r}, got {actual!r}",
                    )
                )
    return violations


def _audit_json_forbidden_text(repo_root: Path, rule: dict[str, Any]) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    forbidden = [item.lower() for item in rule.get("forbiddenSubstrings", [])]
    for path in _iter_target_files(repo_root, rule["targets"]):
        rel = path.relative_to(repo_root)
        try:
            data = _load_json(path)
        except json.JSONDecodeError:
            continue
        if not _applies_when(data, rule.get("appliesWhen")):
            continue
        payload = json.dumps(data, ensure_ascii=False).lower()
        for needle in forbidden:
            if needle in payload:
                violations.append(
                    _violation(
                        rule["id"],
                        rel,
                        f"forbidden workbench receipt claim found: {needle!r}",
                    )
                )
    return violations


def _audit_text_forbidden_regex(repo_root: Path, rule: dict[str, Any]) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    pattern = re.compile(rule["forbiddenRegex"], re.IGNORECASE)
    ignore_needles = [item.lower() for item in rule.get("ignoreIfLineContainsAny", [])]
    for path in _iter_target_files(repo_root, rule["targets"]):
        rel = path.relative_to(repo_root)
        text = path.read_text(encoding="utf-8")
        for idx, line in enumerate(text.splitlines(), start=1):
            if not pattern.search(line):
                continue
            lowered = line.lower()
            if any(needle in lowered for needle in ignore_needles):
                continue
            violations.append(
                _violation(
                    rule["id"],
                    rel,
                    "line appears to claim canonical merge authority inside WORK docs",
                    line=idx,
                )
            )
    return violations


def _audit_text_required_regex(repo_root: Path, rule: dict[str, Any]) -> list[dict[str, Any]]:
    violations: list[dict[str, Any]] = []
    required_patterns = [re.compile(item, re.IGNORECASE) for item in rule.get("requiredAllRegex", [])]
    for path in _iter_target_files(repo_root, rule["targets"]):
        rel = path.relative_to(repo_root)
        text = path.read_text(encoding="utf-8")
        for pattern in required_patterns:
            if pattern.search(text):
                continue
            violations.append(
                _violation(
                    rule["id"],
                    rel,
                    f"required doctrine phrase missing: {pattern.pattern!r}",
                )
            )
    return violations


RULE_DISPATCH = {
    "python_canonical_writer_allowlist": _audit_python_canonical_writer_allowlist,
    "json_field_const": _audit_json_field_const,
    "json_forbidden_text": _audit_json_forbidden_text,
    "text_forbidden_regex": _audit_text_forbidden_regex,
    "text_required_regex": _audit_text_required_regex,
}


def audit_repo(repo_root: Path, config_path: Path) -> dict[str, Any]:
    config = _load_json(config_path)
    violations: list[dict[str, Any]] = []
    for rule in config.get("rules", []):
        kind = rule.get("kind")
        handler = RULE_DISPATCH.get(kind)
        if handler is None:
            violations.append(
                _violation(
                    rule.get("id", "unknown-rule"),
                    config_path.relative_to(repo_root),
                    f"unsupported rule kind: {kind!r}",
                )
            )
            continue
        violations.extend(handler(repo_root, rule))
    return {
        "ok": not violations,
        "violationCount": len(violations),
        "violations": violations,
    }


def _render_text(report: dict[str, Any]) -> str:
    if report["ok"]:
        return "ok: doctrine drift radar found no violations"
    lines = [f"violations: {report['violationCount']}"]
    for item in report["violations"]:
        loc = item["path"]
        if "line" in item:
            loc = f"{loc}:{item['line']}"
        lines.append(f"- [{item['ruleId']}] {loc} — {item['message']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only doctrine drift audit")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root to audit (default: current repo)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Rule config path (default: config/doctrine-rules.v1.json)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    config_path = args.config.resolve()
    report = audit_repo(repo_root, config_path)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(_render_text(report))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
