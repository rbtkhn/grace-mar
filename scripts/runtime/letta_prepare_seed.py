#!/usr/bin/env python3
"""Convert a Grace-Mar runtime_complement_export bundle to a Letta-style seed JSON (stdlib only).

Does not read Record trees except what is already embedded in the bundle.
Writes only the output path given (default under runtime/runtime-complements/exports/).
"""

from __future__ import annotations

import argparse
import json
import re
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EXPORTS = REPO_ROOT / "runtime" / "runtime-complements" / "exports"

GRACE_MAR_CONTEXT_CAP = 24_000

# Explicit \n in source keeps string boundaries visible (no accidental line breaks in literals).
MEMBRANE = (
    "This seed is non-canonical runtime context.\n"
    "Durable Grace-Mar state changes require the gate; import summaries only via "
    "import_runtime_observation.py."
)

DEFAULT_BOUNDARY_FALLBACK = (
    "Letta may remember inside Letta. "
    "Grace-Mar remembers only through the gate."
)

OPERATOR_INSTRUCTIONS_VALUE = (
    "Operator rules: (1) Do not treat Letta memory as Grace-Mar Record. "
    "(2) Stage any durable change through recursion-gate and companion-approved merge. "
    "(3) Use letta_import_summary.py or import_runtime_observation.py for inbound JSON only."
)

RUNTIME_NOTES_PLACEHOLDER = (
    "Letta-local session notes (fill in outside Grace-Mar). Not SELF, EVIDENCE, SKILLS, or SELF-LIBRARY."
)


def _ts_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _rel_to_repo(p: Path) -> str:
    return p.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def _sanitize_name(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_.-]+", "-", (name or "bundle").strip())
    return s[:80] if s else "bundle"


def _build_context_from_included(
    included_files: list[dict[str, Any]],
) -> tuple[str, list[str]]:
    """Return (concatenated text, list of inline skip messages)."""
    parts: list[str] = []
    skips: list[str] = []
    for item in included_files:
        p = str(item.get("path", ""))
        if item.get("missing"):
            if p:
                skips.append(f"[omitted: missing] {p}")
            continue
        if "error" in item and "content" not in item:
            if p:
                skips.append(f"[omitted: read error] {p}: {item.get('error', '')}")
            continue
        content = item.get("content")
        if not isinstance(content, str):
            if p:
                skips.append(f"[omitted: not text content] {p}")
            continue
        block = f"--- {p} ---\n{content}\n"
        parts.append(block)
    for sk in skips:
        parts.append(sk + "\n")
    return "".join(parts), skips


def _maybe_truncate(s: str, cap: int) -> str:
    if len(s) <= cap:
        return s
    note = f"\n\n[Truncated from {len(s)} to {cap} characters for grace_mar_context cap.]"
    return s[: max(0, cap - len(note))] + note


def main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Build a Letta seed JSON from a runtime_complement_export bundle."
        )
    )
    ap.add_argument(
        "--bundle",
        type=Path,
        required=True,
        help="Path to export bundle JSON (repo-relative or absolute).",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output JSON (default: exports/letta-seed_<ts>_<name>_<id>.json).",
    )
    args = ap.parse_args()

    bundle_path = args.bundle
    if not bundle_path.is_absolute():
        s = str(bundle_path)
        if ".." in s or not s.strip():
            print("error: invalid --bundle path", file=sys.stderr)
            return 1
        bundle_path = (REPO_ROOT / bundle_path).resolve()
    else:
        bps = str(bundle_path)
        try:
            bundle_path.relative_to(REPO_ROOT)
        except ValueError:
            if ".." in bps:
                print("error: invalid --bundle path", file=sys.stderr)
                return 1

    if not bundle_path.is_file():
        print(f"error: bundle is not a file: {bundle_path}", file=sys.stderr)
        return 1
    try:
        raw = bundle_path.read_text(encoding="utf-8", errors="strict")
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    try:
        data: Any = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 1
    if not isinstance(data, dict):
        print("error: bundle must be a JSON object", file=sys.stderr)
        return 1
    if str(data.get("kind", "")) != "runtime_complement_export":
        print("error: bundle kind must be runtime_complement_export", file=sys.stderr)
        return 1

    bundle_id = str(data.get("bundle_id", ""))
    name = str(data.get("name", ""))
    gen_at = str(data.get("generated_at", ""))
    boundary = str(data.get("boundary_notice", DEFAULT_BOUNDARY_FALLBACK))
    included: list[dict[str, Any]] = data.get("included_files")
    if not isinstance(included, list):
        included = []
    clean_included = [x for x in included if isinstance(x, dict)]
    ctx_text, _ = _build_context_from_included(clean_included)
    ctx_value = _maybe_truncate(ctx_text, GRACE_MAR_CONTEXT_CAP)

    blocks: list[dict[str, str]] = [
        {
            "label": "grace_mar_boundary",
            "description": "Rules that keep Letta runtime memory separate from Grace-Mar canonical Record.",
            "value": boundary + "\n\n" + MEMBRANE,
        },
        {
            "label": "grace_mar_context",
            "description": "Concatenated included bundle files (capped) from the export bundle.",
            "value": ctx_value if ctx_value.strip() else "(no text content in bundle included_files)",
        },
        {
            "label": "operator_instructions",
            "description": "Review-first; no automatic merge into Record.",
            "value": OPERATOR_INSTRUCTIONS_VALUE,
        },
        {
            "label": "runtime_session_notes",
            "description": "Letta-local session notes; non-canonical.",
            "value": RUNTIME_NOTES_PLACEHOLDER,
        },
    ]
    out_obj: dict[str, Any] = {
        "adapter": "letta",
        "kind": "letta_seed_context",
        "status": "runtime_only_noncanonical",
        "source_bundle_id": bundle_id,
        "source_bundle_name": name,
        "generated_at": gen_at,
        "boundary_notice": boundary,
        "suggested_memory_blocks": blocks,
        "promotion_path": (
            "Letta summary -> runtime complement inbox + receipt -> human review -> "
            "optional recursion-gate candidate -> approved merge (normal Grace-Mar gate)."
        ),
    }

    if args.out is None:
        EXPORTS.mkdir(parents=True, exist_ok=True)
        uniq = secrets.token_hex(4)
        fn = f"letta-seed_{_ts_compact()}_{_sanitize_name(name)}_{uniq}.json"
        out_path = EXPORTS / fn
    else:
        out_path = args.out
        if not out_path.is_absolute():
            s = str(args.out)
            if ".." in s or not s.strip():
                print("error: invalid --out path", file=sys.stderr)
                return 1
            out_path = (REPO_ROOT / out_path).resolve()
        else:
            if ".." in str(out_path):
                print("error: invalid --out path", file=sys.stderr)
                return 1
        out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        out_path.resolve().relative_to(REPO_ROOT.resolve())
    except ValueError:
        print("error: --out must be inside the repository", file=sys.stderr)
        return 1

    out_path.write_text(
        json.dumps(out_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(_rel_to_repo(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
