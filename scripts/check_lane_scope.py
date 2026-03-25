#!/usr/bin/env python3
"""
Verify changed files stay within a declared lane (see lanes.yaml).

Usage:
  python scripts/check_lane_scope.py --lane work-dev --diff origin/main...HEAD
  python scripts/check_lane_scope.py --lane work-dev --files a.md b.py
  python scripts/check_lane_scope.py --lane work-dev --diff ... --allow-cross-lane \\
      --justification "OpenClaw + gate wiring per issue 123"
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
LANES_PATH = REPO_ROOT / "lanes.yaml"


def _norm(p: str) -> str:
    return p.replace("\\", "/").lstrip("./")


def path_matches_glob(path: str, pattern: str) -> bool:
    """Match path against pattern with / separators; ** matches zero or more segments."""
    path = _norm(path)
    pattern = _norm(pattern)
    if pattern == "**":
        return True
    parts = path.split("/") if path else []
    pat_segs: list[str | None] = []
    for seg in pattern.split("/"):
        if seg == "**":
            if not pat_segs or pat_segs[-1] is not None:
                pat_segs.append(None)
        elif seg != "":
            pat_segs.append(seg)
    if not pat_segs:
        return len(parts) == 0

    def ok(pi: int, pj: int) -> bool:
        if pj >= len(pat_segs):
            return pi >= len(parts)
        seg = pat_segs[pj]
        if seg is None:
            if ok(pi, pj + 1):
                return True
            for k in range(pi + 1, len(parts) + 1):
                if ok(k, pj + 1):
                    return True
            return False
        if pi >= len(parts):
            return False
        if not fnmatch.fnmatch(parts[pi], seg):
            return False
        return ok(pi + 1, pj + 1)

    return ok(0, 0)


def _any_match(path: str, patterns: list[str]) -> bool:
    return any(path_matches_glob(path, p) for p in patterns)


def _forbidden_hit(path: str, patterns: list[str]) -> bool:
    return _any_match(path, patterns)


def load_lanes(path: Path | None = None) -> dict[str, Any]:
    p = path or LANES_PATH
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "lanes" not in data:
        raise ValueError("lanes.yaml must contain top-level 'lanes'")
    return data


def changed_files_from_diff(spec: str, repo_root: Path) -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMRT", spec],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "git diff failed")
    return [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]


def check_lane(
    lane: str,
    files: list[str],
    lanes_doc: dict[str, Any],
    *,
    allow_cross_lane: bool,
    justification: str,
) -> tuple[int, list[str]]:
    lanes = lanes_doc.get("lanes") or {}
    if lane not in lanes:
        return 1, [f"unknown lane: {lane!r} (known: {sorted(lanes.keys())})"]
    cfg = lanes[lane]
    owned = list(cfg.get("owned_paths") or [])
    shared = list(cfg.get("allowed_shared_paths") or [])
    forbidden = list(cfg.get("forbidden_paths") or [])
    errors: list[str] = []
    for f in files:
        nf = _norm(f)
        if _forbidden_hit(nf, forbidden):
            errors.append(f"FORBIDDEN for lane {lane}: {nf}")
            continue
        if _any_match(nf, owned) or _any_match(nf, shared):
            continue
        errors.append(f"OUT_OF_SCOPE for lane {lane}: {nf}")

    if errors and allow_cross_lane:
        j = (justification or "").strip()
        if not j:
            return 1, errors + ["--allow-cross-lane requires non-empty --justification"]
        return 0, [f"cross-lane override accepted: {j!r}"] + [f"  (would have blocked: {e})" for e in errors]

    if errors:
        return 1, errors
    return 0, [f"lane-scope OK: {lane} ({len(files)} file(s))"]


def check_any_lane(files: list[str], lanes_doc: dict[str, Any]) -> tuple[int, list[str], str | None]:
    """Return success if at least one lane accepts every file (forbidden rules still apply).

    Third tuple value is the matched lane id when code == 0.
    """
    names = sorted((lanes_doc.get("lanes") or {}).keys())
    for lane in names:
        code, msgs = check_lane(lane, files, lanes_doc, allow_cross_lane=False, justification="")
        if code == 0:
            return 0, [f"lane-scope OK: matched lane `{lane}` ({len(files)} file(s))"] + msgs[1:], lane
    return 1, ["no single lane owns all changed files; split the PR or use --allow-cross-lane"], None


def _observability_enabled(append_flag: bool) -> bool:
    if append_flag:
        return True
    v = (os.getenv("GRACE_MAR_LOG_LANE_VIOLATIONS") or "").strip().lower()
    return v in ("1", "true", "yes")


def append_lane_violation_event(repo_root: Path, *, lane: str | None, files: list[str], detail: str) -> None:
    p = repo_root / "runtime" / "observability" / "lane_scope.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "event": "lane_violation",
        "lane": lane,
        "files": list(files),
        "detail": detail,
        "ts": datetime.now(timezone.utc).isoformat(),
    }
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="Enforce lane scope for changed paths.")
    ap.add_argument("--lane", default="", help="Lane name from lanes.yaml (omit with --accept-any-lane)")
    ap.add_argument("--accept-any-lane", action="store_true", help="Pass if any lane fully accepts the diff")
    ap.add_argument("--diff", default="", help="git diff range (e.g. origin/main...HEAD)")
    ap.add_argument("--files", nargs="*", default=[], help="Explicit paths (repo-relative)")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument("--lanes-yaml", type=Path, default=LANES_PATH)
    ap.add_argument("--allow-cross-lane", action="store_true")
    ap.add_argument("--justification", default=os.getenv("LANE_CROSS_JUSTIFICATION", ""))
    ap.add_argument(
        "--require-lane-env",
        action="store_true",
        help="If --lane is empty and not --accept-any-lane, require PR_LANE env var",
    )
    ap.add_argument(
        "--append-observability",
        action="store_true",
        help="Append lane_violation events to runtime/observability/lane_scope.jsonl on failure "
        "(also enabled by GRACE_MAR_LOG_LANE_VIOLATIONS=1)",
    )
    args = ap.parse_args()

    if args.require_lane_env and not args.accept_any_lane:
        if not (args.lane or "").strip():
            env_lane = (os.getenv("PR_LANE") or "").strip()
            if not env_lane:
                print("error: PR_LANE env var is required (--require-lane-env)", file=sys.stderr)
                return 2
            args.lane = env_lane

    try:
        doc = load_lanes(args.lanes_yaml)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if args.diff:
        try:
            files = changed_files_from_diff(args.diff, args.repo_root)
        except RuntimeError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
    else:
        files = [_norm(f) for f in args.files]

    if not files:
        print("lane-scope: no files to check (empty diff or --files)")
        return 0

    matched_any: str | None = None
    if args.accept_any_lane:
        code, msgs, matched_any = check_any_lane(files, doc)
    else:
        if not args.lane.strip():
            print("error: --lane is required unless --accept-any-lane", file=sys.stderr)
            return 2
        code, msgs = check_lane(
            args.lane,
            files,
            doc,
            allow_cross_lane=args.allow_cross_lane,
            justification=args.justification,
        )
    if args.accept_any_lane and code == 0 and matched_any:
        print(
            f"warning: permissive --accept-any-lane; matched lane: {matched_any} "
            "(prefer declared --lane in CI)",
            file=sys.stderr,
        )

    if _observability_enabled(args.append_observability) and code != 0:
        if args.accept_any_lane:
            append_lane_violation_event(
                args.repo_root,
                lane=None,
                files=files,
                detail="accept_any_lane_failed",
            )
        else:
            append_lane_violation_event(
                args.repo_root,
                lane=args.lane.strip() or None,
                files=files,
                detail="declared_lane_failed",
            )

    for m in msgs:
        print(m)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
