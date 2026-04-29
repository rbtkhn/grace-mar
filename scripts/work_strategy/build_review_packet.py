#!/usr/bin/env python3
"""Work-strategy review packet: deterministic derived handoff JSON/Markdown (WORK-only, stdlib)."""

from __future__ import annotations

import argparse
import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packet_common import inspect_artifact, is_forbidden_record_path, safe_rel

SCHEMA_VERSION = "work-strategy-review-packet.v1"
LANE = "work-strategy"

# Mirror validate_strategy_packet.UNRESOLVED_MARKERS / CONTRADICTION_MARKERS (avoid circular imports).
UNRESOLVED_MARKERS = ["TODO", "TBD", "UNRESOLVED", "NEEDS REVIEW", "???"]
CONTRADICTION_MARKERS = ["contradiction", "conflict", "in tension", "uncertain"]

TASK_EXCERPT_MAX_WORDS = 120
NOTABLE_CHECKS_CAP = 24


def load_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def read_text_if_possible(path: Path) -> str | None:
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def extract_task_excerpt(text: str, max_words: int = TASK_EXCERPT_MAX_WORDS) -> str:
    t = text.strip()
    if not t:
        return ""
    parts = re.split(r"\s+", t)
    words = [p for p in parts if p]
    if len(words) <= max_words:
        return t
    return " ".join(words[:max_words]) + " …"


def scan_markers_simple(text: str, markers: list[str]) -> dict[str, int]:
    by_marker: dict[str, int] = {}
    lower = text.lower()
    for m in markers:
        if m == "???":
            by_marker[m] = text.count("???")
        else:
            by_marker[m] = lower.count(m.lower())
    return by_marker


def collect_input_paths(
    repo_root: Path,
    *,
    task_path_rel: str | None,
    sources: list[str],
    artifacts: list[str],
    carry_receipt_rel: str | None,
    validation_rel: str | None,
    task_shape_rel: str | None,
) -> tuple[dict[str, Any], dict[str, str]]:
    """Return inputs block and existence_notes keyed by relative path strings."""
    existence_notes: dict[str, str] = {}

    def note_for(rel: str, abs_path: Path) -> None:
        if abs_path.is_file():
            existence_notes[rel] = "exists"
        else:
            existence_notes[rel] = "missing or not a file"

    spaths = [str(Path(p).as_posix()) for p in sources]
    apaths = [str(Path(p).as_posix()) for p in artifacts]

    for rel in spaths:
        p = (repo_root / rel).resolve() if not Path(rel).is_absolute() else Path(rel).resolve()
        note_for(rel, p)
    for rel in apaths:
        p = (repo_root / rel).resolve() if not Path(rel).is_absolute() else Path(rel).resolve()
        note_for(rel, p)

    inputs: dict[str, Any] = {
        "task_path": task_path_rel,
        "source_paths": spaths,
        "artifact_paths": apaths,
        "carry_receipt_path": carry_receipt_rel,
        "validation_report_path": validation_rel,
        "task_shape_report_path": task_shape_rel,
        "existence_notes": existence_notes,
    }
    return inputs, existence_notes


def _validator_by_id(validators: list[dict[str, Any]], vid: str) -> dict[str, Any] | None:
    for v in validators:
        if v.get("id") == vid:
            return v
    return None


def derive_uncertainties(
    validation_report: dict[str, Any] | None,
    repo_root: Path,
    artifact_paths: list[str],
    *,
    artifact_text_when_no_validation: bool,
) -> list[str]:
    out: list[str] = []
    if validation_report:
        validators = validation_report.get("validators") or []
        for vid in ("unresolved_marker_scan", "task_shape_expectations"):
            row = _validator_by_id(validators, vid)
            if row and row.get("status") not in ("pass",):
                det = str(row.get("details") or "").strip()
                if det:
                    out.append(f"{vid}: {det}")
    if artifact_text_when_no_validation:
        chunks: list[str] = []
        for rel in artifact_paths:
            p = (repo_root / rel).resolve() if not Path(rel).is_absolute() else Path(rel).resolve()
            txt = read_text_if_possible(p)
            if not txt:
                continue
            hits = scan_markers_simple(txt, UNRESOLVED_MARKERS)
            total = sum(hits.values())
            if total:
                chunks.append(f"{rel}: unresolved-marker hits={total} ({hits})")
        out.extend(chunks)
    return out


def derive_contradictions(
    validation_report: dict[str, Any] | None,
    repo_root: Path,
    artifact_paths: list[str],
    *,
    artifact_text_when_no_validation: bool,
) -> list[str]:
    out: list[str] = []
    if validation_report:
        validators = validation_report.get("validators") or []
        row = _validator_by_id(validators, "contradiction_marker_scan")
        if row and row.get("status") not in ("pass",):
            det = str(row.get("details") or "").strip()
            if det:
                out.append(det)
    if artifact_text_when_no_validation:
        for rel in artifact_paths:
            p = (repo_root / rel).resolve() if not Path(rel).is_absolute() else Path(rel).resolve()
            txt = read_text_if_possible(p)
            if not txt:
                continue
            hits = scan_markers_simple(txt, CONTRADICTION_MARKERS)
            total = sum(hits.values())
            if total:
                out.append(f"{rel}: contradiction/tension-marker hits={total}")
    return out


def notable_checks_from_validation(validation_report: dict[str, Any] | None) -> tuple[list[dict[str, str]], str]:
    notes = ""
    if not validation_report:
        return [], "Structural validation report was not loaded; hygiene unknown."
    validators = validation_report.get("validators") or []
    notable: list[dict[str, str]] = []
    for v in validators:
        st = v.get("status")
        if st in ("fail", "needs_review"):
            notable.append(
                {
                    "id": str(v.get("id", "")),
                    "status": str(st),
                    "details": str(v.get("details", ""))[:2000],
                }
            )
        if len(notable) >= NOTABLE_CHECKS_CAP:
            break
    summ = validation_report.get("summary") or {}
    notes = str(summ.get("notes", "") or "")
    return notable, notes


def derive_review_readiness(
    *,
    json_out_forbidden: bool,
    markdown_out_forbidden: bool,
    validation_report: dict[str, Any] | None,
    carry_receipt: dict[str, Any] | None,
    task_shape_report: dict[str, Any] | None,
    gate_snippet_arg: str | None,
    gate_snippet_present: bool,
    gate_snippet_nonempty: bool,
    uncertainties: list[str],
    contradictions: list[str],
) -> tuple[str, str]:
    """Return (status, reason) for review_readiness."""

    def fmt_parts(*parts: str) -> str:
        return "; ".join(p for p in parts if p)

    if json_out_forbidden or markdown_out_forbidden:
        return "fail", fmt_parts(
            "Review packet output path is under a forbidden root (users/ or blocked bot files)."
        )

    if carry_receipt and carry_receipt.get("result") == "fail":
        return "fail", "Carry receipt reports result=fail."

    v_status: str | None = None
    if validation_report:
        v_status = str((validation_report.get("summary") or {}).get("status") or "pass")
        if v_status == "fail":
            return "fail", "Validation summary status is fail."

    reasons_nr: list[str] = []

    if validation_report:
        if v_status == "needs_review":
            reasons_nr.append("validation summary needs_review")
    else:
        reasons_nr.append("structural validation report not loaded")

    cls = (task_shape_report or {}).get("classification") or {}
    conf = cls.get("confidence")
    if conf == "low":
        reasons_nr.append("task-shape confidence is low")

    if gate_snippet_arg:
        if not gate_snippet_present:
            reasons_nr.append("gate snippet path missing or unreadable")
        elif not gate_snippet_nonempty:
            reasons_nr.append("gate snippet file empty")

    if uncertainties:
        reasons_nr.append(f"uncertainties listed ({len(uncertainties)})")
    if contradictions:
        reasons_nr.append(f"contradictions/tension signals listed ({len(contradictions)})")

    if reasons_nr:
        return "needs_review", fmt_parts(*reasons_nr)

    return "pass", "No blocking signals from loaded reports and declared paths."


def render_review_packet_markdown(packet: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# Review packet ({packet.get('schema_version', SCHEMA_VERSION)})")
    lines.append("")
    lines.append(f"- **run_id:** {packet.get('run_id', '')}")
    lines.append(f"- **created_at:** {packet.get('created_at', '')}")
    lines.append("")

    task = packet.get("task") or {}
    lines.append("## A — Task statement")
    lines.append("")
    lines.append(f"- **Title:** {task.get('title', '')}")
    lines.append(f"- **Task path:** `{task.get('task_path')}`")
    lines.append("")
    lines.append(task.get("task_excerpt", ""))
    lines.append("")

    ts = packet.get("task_shape")
    lines.append("## B — Task shape")
    lines.append("")
    if isinstance(ts, dict):
        lines.append(f"- **Primary:** {ts.get('primary')}")
        lines.append(f"- **Confidence:** {ts.get('confidence')}")
        sc = ts.get("secondary_candidates") or []
        lines.append(f"- **Secondary candidates:** {len(sc)} row(s).")
        lines.append("")
        lines.append(ts.get("notes", ""))
    else:
        lines.append("_No task-shape report loaded._")
    lines.append("")

    inp = packet.get("inputs") or {}
    lines.append("## C — Inputs")
    lines.append("")
    lines.append(f"- **carry_receipt_path:** `{inp.get('carry_receipt_path')}`")
    lines.append(f"- **validation_report_path:** `{inp.get('validation_report_path')}`")
    lines.append(f"- **task_shape_report_path:** `{inp.get('task_shape_report_path')}`")
    lines.append("")
    lines.append("**Sources:**")
    for p in inp.get("source_paths") or []:
        lines.append(f"- `{p}`")
    lines.append("")
    lines.append("**Artifacts:**")
    for p in inp.get("artifact_paths") or []:
        lines.append(f"- `{p}`")
    notes = inp.get("existence_notes") or {}
    if notes:
        lines.append("")
        lines.append("**Existence notes:**")
        for k, v in sorted(notes.items()):
            lines.append(f"- `{k}`: {v}")
    lines.append("")

    hs = packet.get("handoff_summary") or {}
    lines.append("## D — Handoff summary")
    lines.append("")
    lines.append(hs.get("text", ""))
    lines.append("")

    lines.append("## E — Uncertainties")
    lines.append("")
    un = packet.get("uncertainties") or []
    if un:
        for u in un:
            lines.append(f"- {u}")
    else:
        lines.append("_None surfaced._")
    lines.append("")

    lines.append("## F — Contradictions / tension")
    lines.append("")
    co = packet.get("contradictions") or []
    if co:
        for c in co:
            lines.append(f"- {c}")
    else:
        lines.append("_None surfaced._")
    lines.append("")

    val = packet.get("validation") or {}
    lines.append("## G — Validator summary")
    lines.append("")
    lines.append(f"- **status:** `{val.get('status')}`")
    lines.append(f"- **notes:** {val.get('notes', '')}")
    lines.append("")
    for row in val.get("notable_checks") or []:
        lines.append(f"- `{row.get('id')}` [{row.get('status')}]: {row.get('details', '')[:500]}")
    lines.append("")

    gp = packet.get("gate_prep") or {}
    lines.append("## H — Gate prep")
    lines.append("")
    lines.append(f"- **snippet_present:** {gp.get('snippet_present')}")
    lines.append(f"- **snippet_non_empty:** {gp.get('snippet_non_empty')}")
    lines.append(f"- **notes:** {gp.get('notes', '')}")
    lines.append("")

    rr = packet.get("review_readiness") or {}
    lines.append("## I — Review readiness")
    lines.append("")
    lines.append(f"- **status:** `{rr.get('status')}`")
    lines.append(f"- **reason:** {rr.get('reason', '')}")
    lines.append("")

    rb = packet.get("record_boundary") or {}
    lines.append("## J — Why this is not canonical")
    lines.append("")
    lines.append(f"- **canonical_write_violation:** {rb.get('canonical_write_violation')}")
    lines.append(f"- **canonical_paths_written:** {rb.get('canonical_paths_written')}")
    lines.append("")
    lines.append(rb.get("notes", ""))
    lines.append("")
    return "\n".join(lines)


def build_review_packet_dict(
    *,
    repo_root: Path,
    run_id: str,
    created_at: str,
    task_arg: str | None,
    sources: list[str],
    artifacts: list[str],
    gate_snippet_arg: str | None,
    carry_receipt_arg: str | None,
    carry_receipt_data: dict[str, Any] | None = None,
    validation_report_arg: str | None,
    task_shape_report_arg: str | None,
    title_override: str | None,
    json_out: Path | None,
    markdown_out: Path | None,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()

    task_path_resolved: Path | None = None
    task_text = ""
    if task_arg:
        task_path_resolved = (
            (repo_root / task_arg).resolve() if not Path(task_arg).is_absolute() else Path(task_arg).resolve()
        )
        task_text = read_text_if_possible(task_path_resolved) or ""

    title = title_override or ""
    if not title and task_text:
        title = task_text.splitlines()[0][:500] if task_text else ""
    elif not title:
        title = "(no task title)"

    task_excerpt = extract_task_excerpt(task_text)

    carry_rel: str | None = None
    carry_loaded: dict[str, Any] | None = None
    if carry_receipt_data is not None:
        carry_loaded = carry_receipt_data
        carry_rel = carry_receipt_arg
    elif carry_receipt_arg:
        cr = (repo_root / carry_receipt_arg).resolve() if not Path(carry_receipt_arg).is_absolute() else Path(carry_receipt_arg).resolve()
        carry_rel = safe_rel(cr, repo_root) if cr.is_file() else str(Path(carry_receipt_arg).as_posix())
        carry_loaded = load_json_if_exists(cr)

    val_rel: str | None = None
    validation_loaded: dict[str, Any] | None = None
    if validation_report_arg:
        vp = (
            (repo_root / validation_report_arg).resolve()
            if not Path(validation_report_arg).is_absolute()
            else Path(validation_report_arg).resolve()
        )
        val_rel = safe_rel(vp, repo_root) if vp.is_file() else str(Path(validation_report_arg).as_posix())
        validation_loaded = load_json_if_exists(vp)

    ts_rel: str | None = None
    task_shape_loaded: dict[str, Any] | None = None
    if task_shape_report_arg:
        tp = (
            (repo_root / task_shape_report_arg).resolve()
            if not Path(task_shape_report_arg).is_absolute()
            else Path(task_shape_report_arg).resolve()
        )
        ts_rel = safe_rel(tp, repo_root) if tp.is_file() else str(Path(task_shape_report_arg).as_posix())
        task_shape_loaded = load_json_if_exists(tp)

    gate_present = False
    gate_nonempty = False
    gate_text = ""
    if gate_snippet_arg:
        gp = (
            (repo_root / gate_snippet_arg).resolve()
            if not Path(gate_snippet_arg).is_absolute()
            else Path(gate_snippet_arg).resolve()
        )
        gate_present = gp.is_file()
        gate_text = read_text_if_possible(gp) or ""
        gate_nonempty = bool(gate_text.strip())

    task_path_rel: str | None = (
        safe_rel(task_path_resolved, repo_root) if task_path_resolved and task_path_resolved.is_file() else None
    )
    inputs, _ = collect_input_paths(
        repo_root,
        task_path_rel=task_path_rel,
        sources=list(sources),
        artifacts=list(artifacts),
        carry_receipt_rel=carry_rel,
        validation_rel=val_rel,
        task_shape_rel=ts_rel,
    )

    # Enrich existence_notes with inspect_artifact for declared artifacts
    ex_notes = dict(inputs["existence_notes"])
    for rel in inputs["artifact_paths"]:
        p = (repo_root / rel).resolve() if not Path(rel).is_absolute() else Path(rel).resolve()
        obs = inspect_artifact(p, repo_root)
        bits = []
        if obs.get("exists"):
            bits.append("exists")
            if "size_bytes" in obs:
                bits.append(f"{obs['size_bytes']} bytes")
            if "word_count" in obs:
                bits.append(f"{obs['word_count']} words")
        if obs.get("notes"):
            bits.append(str(obs["notes"]))
        ex_notes[rel] = "; ".join(bits) if bits else ex_notes.get(rel, "")
    inputs["existence_notes"] = ex_notes

    artifact_scan_supplement = validation_loaded is None
    uncertainties = derive_uncertainties(
        validation_loaded,
        repo_root,
        list(inputs["artifact_paths"]),
        artifact_text_when_no_validation=artifact_scan_supplement,
    )
    contradictions = derive_contradictions(
        validation_loaded,
        repo_root,
        list(inputs["artifact_paths"]),
        artifact_text_when_no_validation=artifact_scan_supplement,
    )

    val_status = "absent"
    notable, val_notes_extra = notable_checks_from_validation(validation_loaded)
    if validation_loaded:
        val_status = str((validation_loaded.get("summary") or {}).get("status") or "pass")
        val_notes = val_notes_extra
    else:
        val_notes = "Structural validation was not run or report missing."

    task_shape_obj: dict[str, Any] | None = None
    if task_shape_loaded:
        cls = task_shape_loaded.get("classification") or {}
        task_shape_obj = {
            "primary": cls.get("primary_shape"),
            "confidence": cls.get("confidence"),
            "secondary_candidates": list(cls.get("secondary_candidates") or []),
            "notes": str(cls.get("notes") or ""),
        }
    elif validation_report_arg or task_shape_report_arg:
        task_shape_obj = {
            "primary": None,
            "confidence": None,
            "secondary_candidates": [],
            "notes": "Task-shape report path declared but file missing or unreadable.",
        }

    handoff_lines = [
        f"run_id={run_id}",
        f"task_path={inputs.get('task_path')}",
        f"sources={len(inputs['source_paths'])} artifact_paths={len(inputs['artifact_paths'])}",
    ]
    if carry_rel:
        handoff_lines.append(f"carry_receipt={carry_rel} result={carry_loaded.get('result') if carry_loaded else 'n/a'}")
    if val_rel:
        handoff_lines.append(f"validation_report={val_rel} summary.status={val_status}")
    if ts_rel:
        ts_note = (
            (task_shape_loaded.get("classification") or {}).get("primary_shape")
            if task_shape_loaded
            else "missing"
        )
        handoff_lines.append(f"task_shape_report={ts_rel} primary={ts_note}")
    handoff_lines.append(f"gate_snippet_requested={bool(gate_snippet_arg)} present={gate_present} non_empty={gate_nonempty}")
    handoff_text = "\n".join(f"- {h}" for h in handoff_lines)

    json_forbidden = bool(json_out and is_forbidden_record_path(json_out, repo_root))
    md_forbidden = bool(markdown_out and is_forbidden_record_path(markdown_out, repo_root))

    rr_status, rr_reason = derive_review_readiness(
        json_out_forbidden=json_forbidden,
        markdown_out_forbidden=md_forbidden,
        validation_report=validation_loaded,
        carry_receipt=carry_loaded,
        task_shape_report=task_shape_loaded,
        gate_snippet_arg=gate_snippet_arg,
        gate_snippet_present=gate_present,
        gate_snippet_nonempty=gate_nonempty,
        uncertainties=uncertainties,
        contradictions=contradictions,
    )

    rb_written: list[str] = []
    if json_out and not json_forbidden:
        rb_written.append(safe_rel(json_out, repo_root))
    if markdown_out and not md_forbidden:
        rb_written.append(safe_rel(markdown_out, repo_root))

    packet: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "created_at": created_at,
        "lane": LANE,
        "task": {
            "title": title,
            "task_path": inputs["task_path"],
            "task_excerpt": task_excerpt,
        },
        "inputs": inputs,
        "handoff_summary": {"text": handoff_text},
        "uncertainties": uncertainties,
        "contradictions": contradictions,
        "validation": {
            "status": val_status,
            "notable_checks": notable,
            "notes": val_notes,
        },
        "gate_prep": {
            "snippet_present": gate_present,
            "snippet_non_empty": gate_nonempty,
            "notes": "Paste-only reminder: snippets are not staged or approved via this packet."
            if gate_snippet_arg
            else "No gate snippet path provided.",
        },
        "review_readiness": {"status": rr_status, "reason": rr_reason},
        "record_boundary": {
            "canonical_paths_written": rb_written,
            "canonical_write_violation": json_forbidden or md_forbidden,
            "notes": "Derived WORK artifact only; not SELF/EVIDENCE. Companion gate governs Record merges.",
        },
    }
    if task_shape_obj is not None:
        packet["task_shape"] = task_shape_obj
    return packet


def exit_code_for_readiness(status: str, mode: str) -> int:
    if mode == "never":
        return 0
    if mode == "fail":
        return 1 if status == "fail" else 0
    # needs_review
    return 1 if status in ("fail", "needs_review") else 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Work-strategy review packet builder (WORK-only).")
    p.add_argument("--task", type=str, default=None, help="Path to task intake markdown.")
    p.add_argument("--source", action="append", default=[], help="Source path (repeatable).")
    p.add_argument("--artifact", action="append", default=[], help="Artifact path (repeatable).")
    p.add_argument("--gate-snippet", type=str, default=None, dest="gate_snippet")
    p.add_argument("--carry-receipt", type=str, default=None, dest="carry_receipt")
    p.add_argument("--validation-report", type=str, default=None, dest="validation_report")
    p.add_argument("--task-shape-report", type=str, default=None, dest="task_shape_report")
    p.add_argument("--title", type=str, default=None)
    p.add_argument("--run-id", type=str, default=None, dest="run_id")
    p.add_argument("--repo-root", type=str, default=None, dest="repo_root")
    p.add_argument("--out", type=str, default=None, help="Write review packet JSON path.")
    p.add_argument("--markdown-out", type=str, default=None, dest="markdown_out")
    p.add_argument("--json", action="store_true", help="Print review packet JSON to stdout.")
    p.add_argument(
        "--fail-on-readiness",
        choices=("fail", "needs_review", "never"),
        default="fail",
        dest="fail_on_readiness",
        help="Exit nonzero policy vs review_readiness.status (default: nonzero only on fail).",
    )
    args = p.parse_args(argv)
    root = args.repo_root or Path(__file__).resolve().parent.parent.parent
    args.repo_root = str(Path(root).resolve())
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    run_id = args.run_id or str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    json_out: Path | None = None
    if args.out:
        json_out = (repo_root / args.out).resolve() if not Path(args.out).is_absolute() else Path(args.out).resolve()

    md_out: Path | None = None
    if args.markdown_out:
        md_out = (
            (repo_root / args.markdown_out).resolve()
            if not Path(args.markdown_out).is_absolute()
            else Path(args.markdown_out).resolve()
        )

    if not args.out and not args.json:
        print("Provide --out and/or --json.", file=sys.stderr)
        return 2

    packet = build_review_packet_dict(
        repo_root=repo_root,
        run_id=run_id,
        created_at=created_at,
        task_arg=args.task,
        sources=list(args.source or []),
        artifacts=list(args.artifact or []),
        gate_snippet_arg=args.gate_snippet,
        carry_receipt_arg=args.carry_receipt,
        carry_receipt_data=None,
        validation_report_arg=args.validation_report,
        task_shape_report_arg=args.task_shape_report,
        title_override=args.title,
        json_out=json_out,
        markdown_out=md_out,
    )

    rr = packet["review_readiness"]["status"]
    exit_c = exit_code_for_readiness(rr, args.fail_on_readiness)

    j_forbid = bool(json_out and is_forbidden_record_path(json_out, repo_root))
    m_forbid = bool(md_out and is_forbidden_record_path(md_out, repo_root))

    if args.out and not j_forbid:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.markdown_out and not m_forbid:
        md_out.parent.mkdir(parents=True, exist_ok=True)
        md_out.write_text(render_review_packet_markdown(packet), encoding="utf-8")

    if args.json:
        print(json.dumps(packet, indent=2, ensure_ascii=False))

    return exit_c


if __name__ == "__main__":
    raise SystemExit(main())
