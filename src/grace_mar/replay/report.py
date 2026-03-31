"""Markdown harness replay report (CLI and operators)."""

from __future__ import annotations

import json
from pathlib import Path
from grace_mar.replay.correlate import (
    evidence_snippet,
    filter_harness,
    filter_merge_receipts,
    filter_pipeline_by_candidate,
    find_candidate_yaml,
    find_pipeline_row_by_event_id,
    harness_rows_for_event_id,
    transcript_hint,
)
from grace_mar.replay.loaders import (
    load_harness_events,
    load_merge_receipts,
    load_pipeline_events,
)


def _footer_block() -> list[str]:
    return [
        "",
        "---",
        "",
        "_Audit lane only. For identity truth, use approved Record files; for full prompt traces, see product logging policy._",
        "",
    ]


def build_report(
    user_dir: Path,
    *,
    candidate_id: str = "",
    bundle_id: str = "",
    event_id: str = "",
    evidence_id: str = "",
    transcript_snippet: bool = False,
) -> str:
    """Build markdown replay report for a user profile directory."""
    user_id = user_dir.name
    pl = load_pipeline_events(user_dir)
    hv = load_harness_events(user_dir)
    mr = load_merge_receipts(user_dir)

    gate_path = user_dir / "recursion-gate.md"
    evidence_path = user_dir / "self-archive.md"
    if not evidence_path.is_file():
        evidence_path = user_dir / "self-evidence.md"
    transcript_path = user_dir / "session-transcript.md"

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
        anchor = find_pipeline_row_by_event_id(pl, eid)
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
        hv_a = harness_rows_for_event_id(hv, eid)
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
        pl_f = filter_pipeline_by_candidate(pl, cid)
        hv_f = filter_harness(hv, cid, None)
        mr_f = filter_merge_receipts(mr, cid)

        gate_body = ""
        if gate_path.is_file():
            gate_body = gate_path.read_text(encoding="utf-8", errors="ignore")
        yaml_block = find_candidate_yaml(gate_body, cid) if gate_path.is_file() else None

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
            lines.extend(["", "## EVIDENCE / self-archive.md (hint line)", ""])
            snip = evidence_snippet(evidence_path, evidence_id.strip().upper())
            lines.append(snip or f"_No line containing `{evidence_id}` found._")

        if transcript_snippet:
            lines.extend(["", "## session-transcript.md (tail — runtime lane)", ""])
            hint = transcript_hint(transcript_path)
            if hint:
                lines.append("```")
                lines.append(hint)
                lines.append("```")
            else:
                lines.append("_Missing or empty._")

    if bid:
        lines.append(f"**Bundle id:** `{bid}`")
        hv_fb = filter_harness(hv, "", bid)
        lines.extend(["", "## harness-events.jsonl (bundle_id)", ""])
        if hv_fb:
            for r in hv_fb:
                lines.append(f"- `{r.get('ts')}` — `{json.dumps(r, ensure_ascii=True)}`")
        else:
            lines.append("_No matching lines._")

    lines.extend(_footer_block())
    return "\n".join(lines)


__all__ = ["build_report"]
