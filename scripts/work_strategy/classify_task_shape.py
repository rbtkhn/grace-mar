#!/usr/bin/env python3
"""Deterministic work-strategy task-shape classifier (WORK-only; stdlib + PyYAML)."""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from packet_common import is_forbidden_record_path, safe_rel

SCHEMA_VERSION = "work-strategy-task-shape-report.v1"
LANE = "work-strategy"

FRONTMATTER_PATTERN = re.compile(r"\A---\s*\r?\n(.*?)\r?\n---\s*", re.DOTALL)


def load_task_shape_config(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    data = yaml.safe_load(raw)
    if not isinstance(data, dict) or "task_shapes" not in data:
        raise ValueError(f"Invalid task shape config: {path}")
    return data


def read_task_text(task_path: Path | None, inline_text: str | None) -> str:
    parts: list[str] = []
    if task_path and task_path.is_file():
        try:
            parts.append(task_path.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            pass
    if inline_text:
        parts.append(inline_text)
    return "\n\n".join(parts).strip()


def extract_frontmatter_hint(text: str) -> str | None:
    if not text.strip():
        return None
    m = FRONTMATTER_PATTERN.match(text.strip())
    if m:
        try:
            fm = yaml.safe_load(m.group(1))
            if isinstance(fm, dict):
                ts = fm.get("task_shape")
                if ts is not None and str(ts).strip():
                    return str(ts).strip()
        except yaml.YAMLError:
            pass
    # Fallback: first lines task_shape: foo
    for line in text.splitlines()[:20]:
        stripped = line.strip()
        if stripped.lower().startswith("task_shape:"):
            return stripped.split(":", 1)[1].strip().strip("\"'")
    return None


def _first_heading_line(text: str) -> str:
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#"):
            return re.sub(r"^#+\s*", "", s).strip().lower()
    return ""


def score_task_shapes(text: str, config: dict[str, Any], task_path: Path | None) -> dict[str, float]:
    shapes_cfg = config["task_shapes"]
    heading = _first_heading_line(text)
    blob = " ".join([text.lower(), heading])
    scores: dict[str, float] = {}
    for name, meta in shapes_cfg.items():
        s = 0.0
        for kw in meta.get("keywords") or []:
            k = kw.lower()
            s += blob.count(k)
        for ak in meta.get("anti_keywords") or []:
            s -= 2.0 * blob.count(ak.lower())
        scores[name] = max(0.0, s)

    if task_path:
        stem = task_path.stem.lower().replace("-", " ").replace("_", " ")
        for name, meta in shapes_cfg.items():
            bonus = 0.0
            for kw in meta.get("keywords") or []:
                k = kw.lower()
                if k in stem or k in stem.replace(" ", ""):
                    bonus += 1.5
                parts = stem.split()
                if k in parts:
                    bonus += 1.0
            scores[name] = scores.get(name, 0.0) + bonus
    return scores


def classify_from_scores(
    scores: dict[str, float],
    frontmatter_hint: str | None,
    valid_shapes: list[str],
) -> tuple[str, str, list[dict[str, Any]], list[str], str]:
    """Return primary_shape, confidence, secondary_candidates, matched_signals, notes."""
    notes_parts: list[str] = []
    matched_signals: list[str] = []

    if frontmatter_hint:
        key = frontmatter_hint.lower().replace(" ", "_").replace("-", "_")
        alias = {
            "gate_candidate": "gate_candidate_prep",
            "notebook": "notebook_synthesis",
        }
        key = alias.get(key, key)
        if key in valid_shapes:
            matched_signals.append(f"frontmatter:{key}")
            secondary = sorted(
                [{"shape": n, "score": scores.get(n, 0.0)} for n in valid_shapes if n != key],
                key=lambda x: (-x["score"], x["shape"]),
            )[:5]
            return key, "high", secondary, matched_signals, "Primary shape taken from YAML frontmatter hint."
        notes_parts.append(f"Ignored invalid frontmatter task_shape: {frontmatter_hint!r}.")

    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    primary, top = ranked[0]
    others_excl = sorted(
        [(n, s) for n, s in scores.items() if n != primary],
        key=lambda kv: (-kv[1], kv[0]),
    )

    if top <= 0.0:
        primary = "decision_point"
        top = scores.get(primary, 0.0)
        notes_parts.append("No keyword signal; defaulting primary to decision_point.")
        matched_signals.append("default:no_keyword_signal")
        others_excl = sorted(
            [(n, s) for n, s in scores.items() if n != primary],
            key=lambda kv: (-kv[1], kv[0]),
        )

    second_score = others_excl[0][1] if others_excl else 0.0
    gap = top - second_score

    if gap < 0.01 and len(ranked) > 1 and ranked[0][1] == ranked[1][1]:
        notes_parts.append("Top shapes tied on score; ambiguity elevated.")
        conf = "low"
    elif top >= 10.0 and gap >= 5.0:
        conf = "high"
    elif top >= 6.0 and gap >= 3.0:
        conf = "medium"
    elif top >= 4.0 and gap >= 2.0:
        conf = "medium"
    else:
        conf = "low"
        notes_parts.append("Low separation between candidates or weak keyword signal.")

    ordered = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    secondary = [{"shape": n, "score": float(s)} for n, s in ordered if n != primary][:5]
    note_txt = " ".join(notes_parts).strip()
    return primary, conf, secondary, matched_signals, note_txt


def build_task_shape_report(
    *,
    repo_root: Path,
    task_arg: str | None,
    inline_text: str | None,
    source_paths: list[str],
    config: dict[str, Any],
    config_path: Path,
    run_id: str,
    created_at: str,
    shape_out_path: Path | None,
) -> dict[str, Any]:
    root = repo_root.resolve()
    task_path: Path | None = None
    if task_arg:
        tp = Path(task_arg)
        task_path = (root / tp).resolve() if not tp.is_absolute() else tp.resolve()

    full_text = read_task_text(task_path, inline_text)
    hint = extract_frontmatter_hint(full_text)
    valid_shapes = sorted(config["task_shapes"].keys())
    scores = score_task_shapes(full_text, config, task_path)
    primary, confidence, secondary, signals, cls_notes = classify_from_scores(scores, hint, valid_shapes)

    shape_meta = dict(config["task_shapes"][primary])
    shape_contract = {
        "required_inputs": shape_meta.get("required_inputs", []),
        "expected_outputs": shape_meta.get("expected_outputs", []),
        "validator_emphasis": shape_meta.get("validator_emphasis", []),
        "review_posture": shape_meta.get("review_posture", ""),
    }

    sig_lines = list(signals)
    for name, sc in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))[:3]:
        if sc > 0:
            sig_lines.append(f"score:{name}={sc:.1f}")
    matched_signals = sig_lines

    out_forbidden = bool(shape_out_path and is_forbidden_record_path(shape_out_path, root))
    rb_notes = "Task-shape reports are derived WORK artifacts only."
    if shape_out_path and out_forbidden:
        rb_notes += " Forbidden output path."

    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "created_at": created_at,
        "lane": LANE,
        "input": {
            "task_path": safe_rel(task_path, root) if task_path and task_path.is_file() else task_arg,
            "inline_text_provided": bool(inline_text and inline_text.strip()),
            "source_paths": list(source_paths),
            "config_path": safe_rel(config_path, root) if config_path.is_file() else str(config_path),
        },
        "classification": {
            "primary_shape": primary,
            "confidence": confidence,
            "matched_signals": matched_signals,
            "secondary_candidates": secondary,
            "notes": cls_notes,
        },
        "shape_contract": shape_contract,
        "record_boundary": {
            "canonical_paths_written": [],
            "canonical_write_violation": out_forbidden,
            "notes": rb_notes,
        },
    }


def run_classify_cli(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    repo_root = Path(args.repo_root).resolve()
    cfg_arg = args.config or str(repo_root / "config" / "work_strategy_task_shapes.yaml")
    config_path = Path(cfg_arg)
    if not config_path.is_absolute():
        config_path = (repo_root / config_path).resolve()
    config = load_task_shape_config(config_path)

    run_id = args.run_id or str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    out_resolved: Path | None = None
    if args.out:
        out_resolved = (
            (repo_root / args.out).resolve()
            if not Path(args.out).is_absolute()
            else Path(args.out).resolve()
        )

    report = build_task_shape_report(
        repo_root=repo_root,
        task_arg=args.task,
        inline_text=args.text,
        source_paths=list(args.source or []),
        config=config,
        config_path=config_path,
        run_id=run_id,
        created_at=created_at,
        shape_out_path=out_resolved,
    )

    ambiguous_fail = bool(args.fail_on_ambiguous and report["classification"]["confidence"] == "low")
    exit_code = 1 if ambiguous_fail else 0

    if out_resolved and not report["record_boundary"]["canonical_write_violation"]:
        out_resolved.parent.mkdir(parents=True, exist_ok=True)
        rel_out = safe_rel(out_resolved, repo_root)
        report["record_boundary"]["canonical_paths_written"] = [rel_out]
        report["record_boundary"]["canonical_write_violation"] = False
        out_resolved.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    elif out_resolved and report["record_boundary"]["canonical_write_violation"]:
        exit_code = max(exit_code, 1)

    return report, exit_code


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Work-strategy task-shape classifier (WORK-only).")
    p.add_argument("--task", type=str, default=None, help="Path to task markdown (repo-relative or absolute).")
    p.add_argument("--text", type=str, default=None, help="Optional inline text appended to task body.")
    p.add_argument("--source", action="append", default=[], help="Source path (recorded in report input only).")
    p.add_argument("--config", type=str, default=None, help="Task shapes YAML (default: config/work_strategy_task_shapes.yaml).")
    p.add_argument("--out", type=str, default=None, help="Classification JSON output path.")
    p.add_argument("--run-id", type=str, default=None, dest="run_id")
    p.add_argument("--repo-root", type=str, default=None, dest="repo_root")
    p.add_argument("--json", action="store_true", help="Print classification JSON to stdout.")
    p.add_argument(
        "--fail-on-ambiguous",
        action="store_true",
        help="Exit nonzero when confidence is low.",
    )
    args = p.parse_args(argv)
    root = args.repo_root or Path(__file__).resolve().parent.parent.parent
    args.repo_root = str(Path(root).resolve())
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report, exit_code = run_classify_cli(args)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif report["record_boundary"].get("canonical_write_violation"):
        print("Classifier refused forbidden --out path.", file=sys.stderr)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
