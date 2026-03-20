#!/usr/bin/env python3
"""
Harness Event Replay — correlate audit-lane JSONL + gate YAML for a candidate or bundle.

Does not reconstruct full LLM prompts unless logged elsewhere. See docs/harness-replay.md.

  python scripts/replay_harness_event.py -u grace-mar --candidate CANDIDATE-0089
  python scripts/replay_harness_event.py -u grace-mar --bundle-id abc123
  python scripts/replay_harness_event.py -u grace-mar --event-id evt_20260320_120000_a1b2c3d4
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

try:
    from repo_io import profile_dir
except ImportError:
    from scripts.repo_io import profile_dir


def _read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    out: list[dict] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict):
            out.append(row)
    return out


def _filter_pipeline(rows: list[dict], candidate_id: str) -> list[dict]:
    cid = candidate_id.strip().upper()
    return [r for r in rows if str(r.get("candidate_id") or "").upper() == cid]


def _filter_harness(rows: list[dict], candidate_id: str, bundle_id: str | None) -> list[dict]:
    cid = candidate_id.strip().upper() if candidate_id else ""
    out: list[dict] = []
    for r in rows:
        if bundle_id and str(r.get("bundle_id") or "") == bundle_id:
            out.append(r)
            continue
        if cid:
            if str(r.get("candidate_id") or "").upper() == cid:
                out.append(r)
                continue
            cids = r.get("candidate_ids")
            if isinstance(cids, list) and any(str(x).upper() == cid for x in cids):
                out.append(r)
    return out


def _filter_merge_receipts(rows: list[dict], candidate_id: str) -> list[dict]:
    cid = candidate_id.strip().upper()
    out: list[dict] = []
    for r in rows:
        ids = r.get("candidate_ids")
        if isinstance(ids, list) and any(str(x).upper() == cid for x in ids):
            out.append(r)
    return out


def _find_pipeline_row_by_event_id(rows: list[dict], event_id: str) -> dict | None:
    want = event_id.strip()
    for r in rows:
        if str(r.get("event_id") or "") == want:
            return r
    return None


def _harness_rows_for_event_id(hv: list[dict], eid: str) -> list[dict]:
    """Harness rows whose event_id matches or that list this id in merge correlation fields."""
    want = eid.strip()
    out: list[dict] = []
    for r in hv:
        if str(r.get("event_id") or "") == want:
            out.append(r)
            continue
        apl = r.get("applied_pipeline_event_ids")
        if isinstance(apl, list) and want in [str(x) for x in apl]:
            out.append(r)
            continue
        spl = r.get("staged_parent_event_ids")
        if isinstance(spl, list) and want in [str(x) for x in spl]:
            out.append(r)
    return out


def _find_candidate_yaml(gate_text: str, candidate_id: str) -> str | None:
    """Match `### CANDIDATE-nnn` blocks in active or Processed sections (full file)."""
    want = candidate_id.strip().upper()
    for m in re.finditer(
        r"### (CANDIDATE-\d+)(?:\s*\(([^)]*)\))?\s*\n```yaml\n(.*?)```",
        gate_text,
        re.DOTALL,
    ):
        if m.group(1).upper() == want:
            return m.group(3).strip()
    return None


def _evidence_snippet(evidence_path: Path, evidence_id: str) -> str | None:
    if not evidence_path.is_file():
        return None
    text = evidence_path.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        if evidence_id.upper() in line.upper() and "ACT-" in line:
            return line.strip()[:500]
    return None


def _transcript_hint(transcript_path: Path, max_lines: int = 40) -> str:
    if not transcript_path.is_file():
        return ""
    lines = transcript_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    tail = lines[-max_lines:] if len(lines) > max_lines else lines
    return "\n".join(tail)


def _footer_block() -> list[str]:
    return [
        "",
        "---",
        "",
        "_Audit lane only. For identity truth, use approved Record files; for full prompt traces, see product logging policy._",
        "",
    ]


def build_report(
    user_id: str,
    *,
    candidate_id: str = "",
    bundle_id: str = "",
    event_id: str = "",
    evidence_id: str = "",
    transcript_snippet: bool = False,
) -> str:
    prof = profile_dir(user_id)
    pipeline_path = prof / "pipeline-events.jsonl"
    harness_path = prof / "harness-events.jsonl"
    merge_path = prof / "merge-receipts.jsonl"
    gate_path = prof / "recursion-gate.md"
    evidence_path = prof / "self-evidence.md"
    transcript_path = prof / "session-transcript.md"

    pl = _read_jsonl(pipeline_path)
    hv = _read_jsonl(harness_path)
    mr = _read_jsonl(merge_path)

    lines: list[str] = [
        "# Harness replay report",
        "",
        f"**User:** `{user_id}`",
        "",
    ]

    cid = (candidate_id or "").strip()
    bid = (bundle_id or "").strip()
    eid = (event_id or "").strip()

    if not eid and not cid and not bid:
        lines.append("_Specify `--candidate`, `--bundle-id`, or `--event-id`._")
        lines.extend(_footer_block())
        return "\n".join(lines)

    if eid:
        anchor = _find_pipeline_row_by_event_id(pl, eid)
        if not anchor:
            lines.append(f"_No pipeline row with `event_id` `{eid}`._")
            lines.extend(_footer_block())
            return "\n".join(lines)
        lines.append(f"**Lookup:** `event_id` = `{eid}`")
        lines.extend(
            [
                "",
                "## Anchored pipeline row",
                "",
                "```json",
                json.dumps(anchor, indent=2, ensure_ascii=True),
                "```",
            ]
        )
        hv_a = _harness_rows_for_event_id(hv, eid)
        lines.extend(["", "## harness-events.jsonl (rows referencing this event_id)", ""])
        if hv_a:
            for r in hv_a:
                lines.append(f"- `{r.get('ts')}` — `{json.dumps(r, ensure_ascii=True)}`")
        else:
            lines.append("_No matching lines._")
        if not cid and anchor.get("candidate_id"):
            cid = str(anchor.get("candidate_id") or "").strip()

    if cid:
        lines.append(f"**Candidate:** `{cid.upper()}`")
        pl_f = _filter_pipeline(pl, cid)
        hv_f = _filter_harness(hv, cid, None)
        mr_f = _filter_merge_receipts(mr, cid)

        gate_body = ""
        if gate_path.is_file():
            gate_body = gate_path.read_text(encoding="utf-8", errors="ignore")
        yaml_block = _find_candidate_yaml(gate_body, cid) if gate_path.is_file() else None

        env_rows = [r for r in pl_f if r.get("event_id")]
        if env_rows:
            lines.extend(["", "## Audit envelope (pipeline rows with `event_id`)", ""])
            for r in env_rows:
                rm = r.get("replay_mode")
                rm_s = f" — replay_mode=`{rm}`" if rm else ""
                par = r.get("parent_event_id")
                par_s = f" — parent=`{par}`" if par else ""
                lines.append(
                    f"- `{r.get('event_id')}` — **{r.get('event')}**{rm_s}{par_s} — envelope v{r.get('envelope_version', '?')}"
                )
                rr = r.get("record_refs")
                if isinstance(rr, list) and rr:
                    lines.append(f"  - record_refs: {', '.join(str(x) for x in rr[:16])}")

        lines.extend(
            [
                "",
                "## recursion-gate.md (YAML block if present)",
                "",
            ]
        )
        if yaml_block:
            lines.append("```yaml")
            lines.append(yaml_block[:12000] + ("…\n(truncated)" if len(yaml_block) > 12000 else ""))
            lines.append("```")
        else:
            lines.append(
                "_No matching `### CANDIDATE-…` block in current `recursion-gate.md` "
                "(may be only under **Processed** with different shape, or removed). "
                "Check git history for the gate file._"
            )

        lines.extend(["", "## pipeline-events.jsonl (matching candidate_id)", ""])
        if pl_f:
            for r in pl_f:
                lines.append(f"- `{r.get('ts')}` — **{r.get('event')}** — `{json.dumps(r, ensure_ascii=True)}`")
        else:
            lines.append("_No matching lines._")

        lines.extend(["", "## harness-events.jsonl (matching candidate / merge batch)", ""])
        if hv_f:
            for r in hv_f:
                lines.append(f"- `{r.get('ts')}` — `{json.dumps(r, ensure_ascii=True)}`")
        else:
            lines.append("_No matching lines._")

        lines.extend(["", "## merge-receipts.jsonl (batches containing candidate)", ""])
        if mr_f:
            for r in mr_f:
                lines.append(f"- `{json.dumps(r, ensure_ascii=True)}`")
        else:
            lines.append("_No matching lines._")

        if evidence_id:
            lines.extend(["", "## self-evidence.md (hint line)", ""])
            snip = _evidence_snippet(evidence_path, evidence_id.strip().upper())
            lines.append(snip or f"_No line containing `{evidence_id}` found._")

        if transcript_snippet:
            lines.extend(["", "## session-transcript.md (tail — runtime lane)", ""])
            hint = _transcript_hint(transcript_path)
            if hint:
                lines.append("```")
                lines.append(hint)
                lines.append("```")
            else:
                lines.append("_Missing or empty._")

    if bid:
        lines.append(f"**Bundle id:** `{bid}`")
        hv_fb = _filter_harness(hv, "", bid)
        lines.extend(["", "## harness-events.jsonl (bundle_id)", ""])
        if hv_fb:
            for r in hv_fb:
                lines.append(f"- `{r.get('ts')}` — `{json.dumps(r, ensure_ascii=True)}`")
        else:
            lines.append("_No matching lines._")

    lines.extend(_footer_block())
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Replay harness/pipeline audit context for a candidate or bundle.")
    ap.add_argument("-u", "--user", default="grace-mar", help="User id")
    ap.add_argument("--candidate", default="", help="CANDIDATE-nnnn")
    ap.add_argument("--bundle-id", default="", help="Harness bundle_id")
    ap.add_argument(
        "--event-id",
        default="",
        help="Single pipeline event_id (evt_…); optional candidate follow-on from row",
    )
    ap.add_argument("--evidence", default="", metavar="ACT-nnnn", help="Optional: show hint line from self-evidence.md")
    ap.add_argument(
        "--transcript-snippet",
        action="store_true",
        help="Append tail of session-transcript.md (runtime; may be large)",
    )
    ap.add_argument("-o", "--output", default="", help="Write markdown to this path")
    args = ap.parse_args()
    if not args.candidate.strip() and not args.bundle_id.strip() and not args.event_id.strip():
        print("Provide --candidate, --bundle-id, or --event-id", file=sys.stderr)
        return 1
    text = build_report(
        args.user.strip(),
        candidate_id=args.candidate.strip(),
        bundle_id=args.bundle_id.strip(),
        event_id=args.event_id.strip(),
        evidence_id=args.evidence.strip(),
        transcript_snippet=args.transcript_snippet,
    )
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(out)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
