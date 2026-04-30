#!/usr/bin/env python3
"""Route Recommendation Receipt — advisory lane hint (derived markdown only; stdlib + JSON)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPTS / "work_strategy"))
from packet_common import is_forbidden_record_path  # noqa: E402

SHAPES_ORDER = (
    "coding",
    "research_to_artifact",
    "recurring_workflow",
    "system_native_action",
    "governance_review",
)


def load_config(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    data = json.loads(raw)
    if not isinstance(data, dict) or "task_shapes" not in data:
        raise ValueError(f"Invalid route recommendation config: {path}")
    return data


def _slug_from_text(text: str, max_len: int = 40) -> str:
    line = (text.strip().splitlines() or [""])[0]
    s = re.sub(r"[^a-zA-Z0-9]+", "-", line.lower()).strip("-")
    if not s:
        s = "task"
    return s[:max_len].rstrip("-")


def score_shapes(
    description: str,
    config: dict[str, Any],
    lane_hint: str | None,
) -> dict[str, float]:
    """Score the five non-unclear shapes; governance overrides add to governance_review."""
    blob = description.lower()
    shapes_cfg = config["task_shapes"]
    scores: dict[str, float] = {}
    for name in SHAPES_ORDER:
        meta = shapes_cfg[name]
        s = 0.0
        for kw in meta.get("keywords") or []:
            s += blob.count(kw.lower())
        for ak in meta.get("anti_keywords") or []:
            s -= 2.0 * blob.count(ak.lower())
        scores[name] = max(0.0, s)

    if lane_hint:
        key = lane_hint.strip().lower()
        lb = config.get("lane_hint_bonuses", {}).get(key)
        if isinstance(lb, dict):
            for sh, bonus in lb.items():
                if sh in scores:
                    scores[sh] += float(bonus)

    gov_boost = 0.0
    for kw in config.get("governance_keyword_override", []):
        if kw.lower() in blob:
            gov_boost += 2.5
    if gov_boost:
        scores["governance_review"] = scores.get("governance_review", 0.0) + gov_boost

    # Strong Record-path signals even if wording is odd
    if any(x in blob for x in ("self.md", "self-archive.md", "recursion-gate.md", "gate candidate")):
        scores["governance_review"] = scores.get("governance_review", 0.0) + 4.0

    return scores


def _confidence_for(primary: str, top: float, second: float) -> str:
    if primary == "unclear":
        return "low"
    gap = top - second
    if top >= 8.0 and gap >= 4.0:
        return "high"
    if top >= 4.0 and gap >= 2.0:
        return "medium"
    if gap < 0.51:
        return "low"
    if top >= 2.0 and gap >= 1.0:
        return "medium"
    return "low"


def infer_recommendation(
    description: str,
    config: dict[str, Any],
    lane_hint: str | None,
) -> dict[str, Any]:
    """
    Return a structured recommendation dict (tests import this).

    Separate from work-strategy `classify_task_shape` taxonomy — this answers
    coarse repo-wide lanes (coding vs gate vs notebooks).
    """
    text = description.strip()
    words = text.split()

    unclear_words = int(config.get("unclear_max_words", 5))
    unclear_chars = int(config.get("unclear_short_char", 28))
    vague_phrases = ("something smart", "do something", "help me")

    shapes_cfg = config["task_shapes"]

    if (
        len(words) <= unclear_words
        and len(text) <= unclear_chars
        and not any(len(w) > 14 for w in words)
    ) or any(vp in text.lower() for vp in vague_phrases):
        uc = shapes_cfg["unclear"]
        return _build_unclear(uc, lane_hint, text, config)

    scores = score_shapes(text, config, lane_hint)
    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    primary, top = ranked[0]
    second = ranked[1][1] if len(ranked) > 1 else 0.0

    # Tie on top score → prefer abstention (unclear) when both are weak
    if len(ranked) > 1 and ranked[0][1] == ranked[1][1] and top < 3.0:
        uc = shapes_cfg["unclear"]
        return _build_unclear(uc, lane_hint, text, config)

    if top <= 0.0:
        uc = shapes_cfg["unclear"]
        return _build_unclear(uc, lane_hint, text, config)

    conf = _confidence_for(primary, top, second)
    if top < 2.0 and second > 0 and top - second < 0.01:
        conf = "low"

    meta = shapes_cfg[primary]
    runner_name = ranked[1][0] if len(ranked) > 1 else "unclear"
    runner_meta = shapes_cfg.get(runner_name, shapes_cfg["unclear"])

    blob_lc = text.lower()
    requires_gate = primary == "governance_review" or any(
        phrase in blob_lc
        for phrase in (
            "durable knowledge",
            "recursion-gate",
            "merge into " + "self",
            "promote to self",
            "should this candidate",
        )
    )
    if primary == "coding" and "self.md" in blob_lc:
        requires_gate = True

    suggested = (config.get("suggested_next_steps") or {}).get(primary, "")
    why_not = (
        f"Runner-up **{runner_name}**: {runner_meta.get('recommended_path', '')[:200]}"
        if runner_name != primary
        else ""
    )

    gov_note = (
        "This receipt is **advisory only** and does not stage or merge gate candidates. "
    )
    if requires_gate:
        gov_note += (
            "Any change to SELF, EVIDENCE, or `bot/prompt.py` requires "
            "`recursion-gate.md` staging and companion-approved merge per `AGENTS.md`."
        )
    else:
        gov_note += "If you later promote content into the Record, use the normal gate pipeline."

    return {
        "task_shape": primary,
        "confidence": conf,
        "recommended_path": meta.get("recommended_path", ""),
        "runner_up_shape": runner_name,
        "runner_up_path": meta.get("runner_up_path", ""),
        "why": meta.get("why_note", ""),
        "why_not": why_not,
        "requires_gate_review": bool(requires_gate),
        "advisory_only": True,
        "governance_note": gov_note,
        "suggested_next_step": suggested,
        "input_summary": text[:2000] + ("…" if len(text) > 2000 else ""),
        "lane_hint": lane_hint or "",
        "scores": {k: round(v, 2) for k, v in sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))},
    }


def _build_unclear(
    uc_meta: dict[str, Any],
    lane_hint: str | None,
    text: str,
    config: dict[str, Any],
) -> dict[str, Any]:
    suggested = (config.get("suggested_next_steps") or {}).get("unclear", "")
    gov_note = (
        "This receipt is **advisory only**. Task is too underspecified to route safely; "
        "clarify before any Record or gate action."
    )
    return {
        "task_shape": "unclear",
        "confidence": "low",
        "recommended_path": uc_meta.get("recommended_path", ""),
        "runner_up_shape": "n/a",
        "runner_up_path": uc_meta.get("runner_up_path", ""),
        "why": uc_meta.get("why_note", ""),
        "why_not": "No strong shape signal — prefer one clarifying round over a false lane pick.",
        "requires_gate_review": False,
        "advisory_only": True,
        "governance_note": gov_note,
        "suggested_next_step": suggested,
        "input_summary": text[:2000] + ("…" if len(text) > 2000 else ""),
        "lane_hint": lane_hint or "",
        "scores": {},
    }


def render_receipt_markdown(data: dict[str, Any], created_at: str) -> str:
    """YAML frontmatter + body per route-recommendation template."""
    ys = "---\n"
    ys += f"kind: route-recommendation\n"
    ys += f"created_at: {created_at}\n"
    ys += f"confidence: {data['confidence']}\n"
    ys += f"task_shape: {data['task_shape']}\n"
    ys += f"requires_gate_review: {str(data['requires_gate_review']).lower()}\n"
    ys += "recommended_path: |\n"
    rp_lines = data["recommended_path"].split("\n") if data["recommended_path"] else [""]
    for ln in rp_lines:
        ys += "  " + ln + "\n"
    ys += "---\n"

    md = ys
    md += "\n# Route Recommendation\n\n"
    md += "## Input summary\n\n"
    md += data.get("input_summary", "") + "\n\n"
    md += "## Inferred task shape\n\n"
    md += f"`{data['task_shape']}` (confidence **{data['confidence']}**)\n\n"
    md += "## Recommended path\n\n"
    md += data["recommended_path"] + "\n\n"
    md += "## Why this path\n\n"
    md += data.get("why", "") + "\n\n"
    md += "## Why not the runner-up\n\n"
    md += data.get("why_not", "") + "\n\n"
    md += "## Governance note\n\n"
    mg = "**Advisory only:** " + ("yes — " + data["governance_note"] if data.get("advisory_only") else "no.")
    mg += (
        "\n\n**Gate/review before durable Record change:** "
        + ("yes" if data["requires_gate_review"] else "not implied by this task shape alone — confirm before merging")
    )
    md += mg + "\n\n"
    md += "## Suggested next step\n\n"
    md += data.get("suggested_next_step", "") + "\n"

    lh = data.get("lane_hint", "").strip()
    if lh:
        md += f"\n*Lane hint used:* `{lh}`\n"

    scores = data.get("scores") or {}
    if scores:
        md += "\n## Diagnostics (scores)\n\n"
        md += "```\n" + json.dumps(scores, indent=2) + "\n```\n"

    return md


def parse_args(repo_root_default: Path, argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Emit a derived route-recommendation markdown receipt.")
    p.add_argument("-t", "--text", default=None, help="Task description (inline).")
    p.add_argument("--text-file", type=str, default=None, help="Read task description from UTF-8 file.")
    p.add_argument("--stdin", action="store_true", help="Read task description from stdin.")
    p.add_argument("--lane-hint", type=str, default=None, help="Optional lane hint (e.g. work-strategy, work-dev).")
    p.add_argument("--config", type=str, default=None, help="Path to route_recommendation.json.")
    p.add_argument("--repo-root", type=str, default=str(repo_root_default), dest="repo_root")
    p.add_argument("--out", type=str, default=None, help="Explicit output path (default: dated artifact).")
    p.add_argument(
        "--stdout",
        action="store_true",
        help="Print receipt to stdout (still writes file unless --no-write).",
    )
    p.add_argument(
        "--no-write",
        action="store_true",
        help="Do not write a file (implies meaningful use with --stdout).",
    )
    parsed = p.parse_args(argv if argv is not None else sys.argv[1:])
    return parsed


def main(argv: list[str] | None = None) -> int:
    repo_root = Path(__file__).resolve().parents[1]
    args = parse_args(repo_root, argv)
    root = Path(args.repo_root).resolve()

    parts: list[str] = []
    if args.text:
        parts.append(args.text)
    if args.text_file:
        tf = Path(args.text_file)
        if not tf.is_absolute():
            tf = root / tf
        parts.append(tf.read_text(encoding="utf-8", errors="replace"))
    if args.stdin:
        parts.append(sys.stdin.read())
    description = "\n\n".join(parts).strip()
    if not description:
        print("No task text: use --text, --text-file, or --stdin.", file=sys.stderr)
        return 2

    cfg_path = Path(args.config) if args.config else root / "config" / "route_recommendation.json"
    if not cfg_path.is_absolute():
        cfg_path = (root / cfg_path).resolve()
    config = load_config(cfg_path)

    data = infer_recommendation(description, config, args.lane_hint)
    created_at = datetime.now(timezone.utc).isoformat()
    body = render_receipt_markdown(data, created_at)

    out_path: Path | None = None
    if not args.no_write:
        if args.out:
            out_path = Path(args.out)
            if not out_path.is_absolute():
                out_path = (root / out_path).resolve()
        else:
            day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            ts = datetime.now(timezone.utc).strftime("%H%M%S")
            slug = _slug_from_text(description)
            out_path = root / "artifacts" / "route-recommendations" / day / f"{ts}-{slug}.md"

        if is_forbidden_record_path(out_path, root):
            print("Refused: output path is forbidden (users/, bot escapes, …).", file=sys.stderr)
            return 1
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(body, encoding="utf-8")

    if args.stdout or args.no_write:
        print(body, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

