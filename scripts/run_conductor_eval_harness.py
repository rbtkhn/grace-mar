#!/usr/bin/env python3
"""Replay harness: emit conductor-session-metrics JSON from fixture or markdown file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SRC = REPO_ROOT / "src"
_WS = REPO_ROOT / "scripts" / "work_strategy"

for p in (_SRC, _WS):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from packet_common import is_forbidden_record_path  # noqa: E402

from grace_mar.conductor_metrics import build_metrics_payload  # noqa: E402

_ALLOWED_ORIGINS = frozenset({"coffee", "conductor_only", "inferred"})


def _load_fixture(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("fixture root must be an object")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Conductor eval replay harness (derived metrics JSON)")
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--fixture", type=Path, metavar="PATH", help="JSON with body_markdown and optional fields")
    src.add_argument("--text-file", type=Path, metavar="PATH", help="Markdown file used as body_markdown")
    parser.add_argument("--slug", required=True, help="Conductor slug (toscanini, …)")
    parser.add_argument("--user", required=True, metavar="ID", help="Operator / instance user id label")
    parser.add_argument(
        "--origin",
        required=True,
        choices=sorted(_ALLOWED_ORIGINS),
        help="Session origin label",
    )
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT, help="Repository root (default: inferred)")
    parser.add_argument("--out", type=Path, metavar="PATH", help="Write metrics JSON here")
    parser.add_argument("--continuity", type=float, default=None, help="Optional continuity_signal stub")
    parser.add_argument("--recommendation", type=float, default=None, help="Optional recommendation_signal stub")
    parser.add_argument("--json", action="store_true", help="Also print JSON to stdout")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    body_markdown = ""
    warnings: list[str] | None = None

    if args.fixture is not None:
        fx = _load_fixture(args.fixture)
        body_markdown = str(fx.get("body_markdown") or "")
        raw_w = fx.get("warnings")
        if isinstance(raw_w, list):
            warnings = [str(x) for x in raw_w]
    else:
        body_markdown = args.text_file.read_text(encoding="utf-8")

    try:
        payload = build_metrics_payload(
            body_markdown=body_markdown,
            conductor_slug=args.slug,
            session_origin=args.origin,
            user=args.user,
            continuity_signal=args.continuity,
            recommendation_signal=args.recommendation,
            warnings=warnings,
            repo_root=repo_root,
        )
    except ValueError as e:
        raise SystemExit(str(e)) from e

    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"

    if args.out is not None:
        out_p = args.out.resolve()
        if is_forbidden_record_path(out_p, repo_root):
            raise SystemExit(f"refusing forbidden output path: {out_p}")
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(text, encoding="utf-8")

    if args.json or args.out is None:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
