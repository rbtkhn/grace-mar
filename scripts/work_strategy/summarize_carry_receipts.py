#!/usr/bin/env python3
"""Aggregate work-strategy carry harness receipts and related JSON reports (WORK-only, stdlib)."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from packet_common import is_forbidden_record_path

SCHEMA_VERSION = "work-strategy-observability-report.v1"
LANE = "work-strategy"

DEFAULT_SUBDIRS = {
    "carry_receipt": "carry-receipts",
    "validation_report": "validation-reports",
    "task_shape_report": "task-shape-reports",
    "review_packet": "review-packets",
}


@dataclass
class ArtifactRecord:
    kind: str
    path: Path
    rel: str
    data: dict[str, Any]
    ts: datetime | None
    ts_src: str


def safe_repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def load_json_files(paths: list[Path]) -> tuple[list[tuple[Path, dict[str, Any]]], list[str]]:
    """Load JSON objects from paths; skip malformed with notes."""
    good: list[tuple[Path, dict[str, Any]]] = []
    notes: list[str] = []
    for p in paths:
        try:
            raw = p.read_text(encoding="utf-8")
            obj = json.loads(raw)
            if not isinstance(obj, dict):
                notes.append(f"{p}: skipped (root JSON is not an object)")
                continue
            good.append((p, obj))
        except OSError as e:
            notes.append(f"{p}: skipped ({e})")
        except json.JSONDecodeError as e:
            notes.append(f"{p}: skipped (malformed JSON: {e})")
    return good, notes


def parse_created_at(data: dict[str, Any]) -> tuple[datetime | None, str]:
    for key in ("created_at", "generatedAt"):
        val = data.get(key)
        if isinstance(val, str) and val.strip():
            s = val.strip().replace("Z", "+00:00")
            try:
                return datetime.fromisoformat(s), f"json:{key}"
            except ValueError:
                continue
    return None, "missing"


def collect_paths_for_kind(
    runtime_root: Path,
    kind: str,
    override: str | None,
) -> list[Path]:
    if override:
        p = Path(override)
        root = p.resolve() if p.is_absolute() else (runtime_root / p).resolve()
    else:
        root = (runtime_root / DEFAULT_SUBDIRS[kind]).resolve()
    if not root.is_dir():
        return []
    return sorted(root.glob("*.json"))


def collect_receipt_paths(
    *,
    runtime_root: Path,
    receipts_dir: str | None,
    validation_dir: str | None,
    task_shape_dir: str | None,
    review_packet_dir: str | None,
) -> dict[str, list[Path]]:
    """Discover *.json paths under configured dirs."""
    return {
        "carry_receipt": collect_paths_for_kind(runtime_root, "carry_receipt", receipts_dir),
        "validation_report": collect_paths_for_kind(runtime_root, "validation_report", validation_dir),
        "task_shape_report": collect_paths_for_kind(runtime_root, "task_shape_report", task_shape_dir),
        "review_packet": collect_paths_for_kind(runtime_root, "review_packet", review_packet_dir),
    }


def build_records(
    path_groups: dict[str, list[Path]],
    repo_root: Path,
    notes_out: list[str],
) -> list[ArtifactRecord]:
    records: list[ArtifactRecord] = []
    mtime_note_added = False
    for kind, paths in path_groups.items():
        loaded, skip_notes = load_json_files(paths)
        notes_out.extend(skip_notes)
        for path, data in loaded:
            rel = safe_repo_rel(path, repo_root)
            ts, ts_src = parse_created_at(data)
            if ts is None:
                try:
                    ts = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
                    ts_src = "mtime_fallback"
                    if not mtime_note_added:
                        notes_out.append(
                            "Some artifacts lacked JSON timestamps; file mtime (UTC) was used for sorting/filtering where needed."
                        )
                        mtime_note_added = True
                except OSError:
                    ts = None
                    ts_src = "missing"
            records.append(ArtifactRecord(kind=kind, path=path, rel=rel, data=data, ts=ts, ts_src=ts_src))
    return records


def artifact_sort_ts(rec: ArtifactRecord) -> datetime:
    """Comparable datetime for filtering/sorting (never None after normalization)."""
    if rec.ts is not None:
        return rec.ts
    try:
        return datetime.fromtimestamp(rec.path.stat().st_mtime, tz=timezone.utc)
    except OSError:
        return datetime.min.replace(tzinfo=timezone.utc)


def filter_by_window(
    records: list[ArtifactRecord],
    *,
    mode: str,
    last_n: int | None,
    since: date | None,
) -> list[ArtifactRecord]:
    if mode == "all":
        return list(records)
    if mode == "since" and since is not None:
        cutoff = datetime(since.year, since.month, since.day, tzinfo=timezone.utc)
        return [r for r in records if artifact_sort_ts(r) >= cutoff]
    if mode == "last_n" and last_n is not None and last_n > 0:
        by_kind: dict[str, list[ArtifactRecord]] = defaultdict(list)
        for r in records:
            by_kind[r.kind].append(r)
        out: list[ArtifactRecord] = []
        for _kind, lst in by_kind.items():
            lst_sorted = sorted(lst, key=artifact_sort_ts, reverse=True)
            out.extend(lst_sorted[:last_n])
        return out
    return list(records)


def summarize_results_carry(records: list[ArtifactRecord]) -> tuple[int, int, int]:
    """pass/fail/needs_review totals from carry receipt artifacts."""
    p = f = nr = 0
    for r in records:
        if r.kind != "carry_receipt":
            continue
        res = r.data.get("result")
        if isinstance(res, str):
            ls = res.lower()
            if ls == "pass":
                p += 1
            elif ls == "fail":
                f += 1
            elif ls == "needs_review":
                nr += 1
            continue
        summ = r.data.get("summary") or {}
        st = str(summ.get("status", "") or "").lower()
        if st == "pass":
            p += 1
        elif st == "fail":
            f += 1
        elif st == "needs_review":
            nr += 1
    return p, f, nr


def summarize_task_shapes(records: list[ArtifactRecord]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for r in records:
        if r.kind != "task_shape_report":
            continue
        cls = r.data.get("classification") or {}
        primary = cls.get("primary_shape")
        if isinstance(primary, str) and primary.strip():
            counts[primary.strip()] += 1
        else:
            counts["_unknown"] += 1
    return dict(sorted(counts.items(), key=lambda x: (-x[1], x[0])))


def summarize_validation_checks(records: list[ArtifactRecord]) -> tuple[Counter[str], Counter[str]]:
    fail_c: Counter[str] = Counter()
    nr_c: Counter[str] = Counter()
    for r in records:
        if r.kind != "validation_report":
            continue
        validators = r.data.get("validators") or []
        if not isinstance(validators, list):
            continue
        for row in validators:
            if not isinstance(row, dict):
                continue
            vid = str(row.get("id") or "")
            st = str(row.get("status") or "").lower()
            if not vid:
                continue
            if st == "fail":
                fail_c[vid] += 1
            elif st == "needs_review":
                nr_c[vid] += 1
    return fail_c, nr_c


def summarize_validation_reports_status(records: list[ArtifactRecord]) -> tuple[int, int, int]:
    p = f = nr = 0
    for r in records:
        if r.kind != "validation_report":
            continue
        summ = r.data.get("summary") or {}
        st = str(summ.get("status", "") or "").lower()
        if st == "pass":
            p += 1
        elif st == "fail":
            f += 1
        elif st == "needs_review":
            nr += 1
    return p, f, nr


def summarize_review_packets(records: list[ArtifactRecord]) -> tuple[int, int, int]:
    """with_validation, with_task_shape, with_gate_snippet (snippet_present)."""
    w_val = w_ts = w_gate = 0
    for r in records:
        if r.kind != "review_packet":
            continue
        inp = r.data.get("inputs") or {}
        vr = inp.get("validation_report_path")
        tsr = inp.get("task_shape_report_path")
        if vr is not None and str(vr).strip():
            w_val += 1
        if tsr is not None and str(tsr).strip():
            w_ts += 1
        gp = r.data.get("gate_prep") or {}
        if bool(gp.get("snippet_present")):
            w_gate += 1
    return w_val, w_ts, w_gate


def summarize_gate_prep(records: list[ArtifactRecord]) -> tuple[int, int]:
    """snippet_present_count, snippet_non_empty_count across carry receipts + review packets."""
    present = nonempty = 0
    for r in records:
        if r.kind == "carry_receipt":
            gs = r.data.get("gate_snippet") or {}
            if bool(gs.get("ready")):
                present += 1
            txt = str(gs.get("text") or "")
            if txt.strip():
                nonempty += 1
        elif r.kind == "review_packet":
            gp = r.data.get("gate_prep") or {}
            if bool(gp.get("snippet_present")):
                present += 1
            if bool(gp.get("snippet_non_empty")):
                nonempty += 1
    return present, nonempty


def top_checks_ctr(cnt: Counter[str], limit: int = 15) -> list[dict[str, Any]]:
    return [{"id": k, "count": v} for k, v in cnt.most_common(limit)]


def summarize_carry_stack(filtered: list[ArtifactRecord]) -> dict[str, Any]:
    p, f, nr = summarize_results_carry(filtered)
    vp, vf, vnr = summarize_validation_reports_status(filtered)

    fail_c, nrv_c = summarize_validation_checks(filtered)
    shapes = summarize_task_shapes(filtered)
    rv_val, rv_ts, rv_gate = summarize_review_packets(filtered)
    gp_pres, gp_non = summarize_gate_prep(filtered)

    by_kind = Counter(r.kind for r in filtered)

    rec_carry = sum(1 for r in filtered if r.kind == "carry_receipt")
    rec_val = sum(1 for r in filtered if r.kind == "validation_report")
    rec_ts = sum(1 for r in filtered if r.kind == "task_shape_report")
    rec_rp = sum(1 for r in filtered if r.kind == "review_packet")

    _ = by_kind  # retained if extending diagnostics

    return {
        "counts": {
            "carry_receipts_total": rec_carry,
            "validation_reports_total": rec_val,
            "task_shape_reports_total": rec_ts,
            "review_packets_total": rec_rp,
            "pass_total": p,
            "fail_total": f,
            "needs_review_total": nr,
            "validation_report_pass": vp,
            "validation_report_fail": vf,
            "validation_report_needs_review": vnr,
        },
        "task_shapes": shapes,
        "validation": {
            "top_failed_checks": top_checks_ctr(fail_c),
            "top_needs_review_checks": top_checks_ctr(nrv_c),
        },
        "review_packets": {
            "with_validation_count": rv_val,
            "with_task_shape_count": rv_ts,
            "with_gate_snippet_count": rv_gate,
        },
        "gate_prep": {
            "snippet_present_count": gp_pres,
            "snippet_non_empty_count": gp_non,
        },
    }


def render_observability_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Work-strategy carry-stack observability")
    lines.append("")
    lines.append(f"- **Generated:** `{report.get('created_at', '')}`")
    lines.append(f"- **Schema:** `{report.get('schema_version', '')}`")
    lines.append("")
    win = report.get("window") or {}
    lines.append("## Window")
    lines.append("")
    lines.append(f"- **mode:** `{win.get('mode')}`  ")
    lines.append(f"- **value:** `{win.get('value')}`")
    lines.append("")
    lines.append("## Totals")
    lines.append("")
    co = report.get("counts") or {}
    for k in (
        "carry_receipts_total",
        "validation_reports_total",
        "task_shape_reports_total",
        "review_packets_total",
    ):
        lines.append(f"- **{k}:** {co.get(k, 0)}")
    lines.append("")
    lines.append("## Carry receipt results")
    lines.append("")
    lines.append(f"- **pass_total:** {co.get('pass_total', 0)}")
    lines.append(f"- **fail_total:** {co.get('fail_total', 0)}")
    lines.append(f"- **needs_review_total:** {co.get('needs_review_total', 0)}")
    lines.append("")
    lines.append("## Validation report summaries")
    lines.append("")
    lines.append(f"- **validation_report_pass:** {co.get('validation_report_pass', 0)}")
    lines.append(f"- **validation_report_fail:** {co.get('validation_report_fail', 0)}")
    lines.append(f"- **validation_report_needs_review:** {co.get('validation_report_needs_review', 0)}")
    lines.append("")
    lines.append("## Task-shape distribution")
    lines.append("")
    shapes = report.get("task_shapes") or {}
    if shapes:
        for shape, n in shapes.items():
            lines.append(f"- `{shape}`: **{n}**")
    else:
        lines.append("_None scanned._")
    lines.append("")
    lines.append("## Common validator checks")
    lines.append("")
    val = report.get("validation") or {}
    lines.append("**Failed (top):**")
    for row in val.get("top_failed_checks") or []:
        lines.append(f"- `{row.get('id')}` — {row.get('count')}")
    if not val.get("top_failed_checks"):
        lines.append("- _none_")
    lines.append("")
    lines.append("**Needs review (top):**")
    for row in val.get("top_needs_review_checks") or []:
        lines.append(f"- `{row.get('id')}` — {row.get('count')}")
    if not val.get("top_needs_review_checks"):
        lines.append("- _none_")
    lines.append("")
    lines.append("## Review packet coverage")
    lines.append("")
    rp = report.get("review_packets") or {}
    lines.append(f"- **with_validation_count:** {rp.get('with_validation_count', 0)}")
    lines.append(f"- **with_task_shape_count:** {rp.get('with_task_shape_count', 0)}")
    lines.append(f"- **with_gate_snippet_count:** {rp.get('with_gate_snippet_count', 0)}")
    lines.append("")
    lines.append("## Gate prep coverage")
    lines.append("")
    gp = report.get("gate_prep") or {}
    lines.append(f"- **snippet_present_count:** {gp.get('snippet_present_count', 0)}")
    lines.append(f"- **snippet_non_empty_count:** {gp.get('snippet_non_empty_count', 0)}")
    lines.append("")
    lines.append("## Files scanned")
    lines.append("")
    fs = report.get("files_scanned") or {}
    for k, v in fs.items():
        lines.append(f"- **{k}:** {v}")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    for n in report.get("notes") or []:
        lines.append(f"- {n}")
    lines.append("")
    return "\n".join(lines)


def merge_summaries(agg: dict[str, Any]) -> dict[str, Any]:
    """Flatten summarize_carry_stack output for top-level report."""
    return {
        "counts": agg["counts"],
        "task_shapes": agg["task_shapes"],
        "validation": agg["validation"],
        "review_packets": agg["review_packets"],
        "gate_prep": agg["gate_prep"],
    }


def build_report(
    *,
    repo_root: Path,
    runtime_root: Path,
    receipts_dir: str | None,
    validation_dir: str | None,
    task_shape_dir: str | None,
    review_packet_dir: str | None,
    window_mode: str,
    last_n: int | None,
    since: date | None,
) -> dict[str, Any]:
    notes: list[str] = []
    groups = collect_receipt_paths(
        runtime_root=runtime_root,
        receipts_dir=receipts_dir,
        validation_dir=validation_dir,
        task_shape_dir=task_shape_dir,
        review_packet_dir=review_packet_dir,
    )
    records = build_records(groups, repo_root, notes)

    mode_eff = window_mode
    if mode_eff == "last_n":
        filt = filter_by_window(records, mode="last_n", last_n=last_n, since=None)
        win_val: Any = last_n
    elif mode_eff == "since":
        filt = filter_by_window(records, mode="since", last_n=None, since=since)
        win_val = since.isoformat() if since else None
    else:
        filt = records
        win_val = None

    agg = summarize_carry_stack(filt)
    merged = merge_summaries(agg)

    malformed_skipped = len([x for x in notes if "malformed JSON" in x])

    files_scanned_fs = {
        "carry_receipts": sum(1 for r in filt if r.kind == "carry_receipt"),
        "validation_reports": sum(1 for r in filt if r.kind == "validation_report"),
        "task_shape_reports": sum(1 for r in filt if r.kind == "task_shape_report"),
        "review_packets": sum(1 for r in filt if r.kind == "review_packet"),
        "malformed_skipped": malformed_skipped,
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "lane": LANE,
        "window": {"mode": mode_eff, "value": win_val},
        **merged,
        "files_scanned": files_scanned_fs,
        "notes": notes,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Summarize work-strategy carry-stack runtime JSON artifacts.")
    p.add_argument("--repo-root", type=str, default=None, dest="repo_root")
    p.add_argument(
        "--runtime-root",
        type=str,
        default="runtime/work-strategy",
        dest="runtime_root",
        help="Directory holding carry-receipts, validation-reports, etc. (repo-relative unless absolute).",
    )
    p.add_argument("--receipts-dir", type=str, default=None, dest="receipts_dir")
    p.add_argument("--validation-dir", type=str, default=None, dest="validation_dir")
    p.add_argument("--task-shape-dir", type=str, default=None, dest="task_shape_dir")
    p.add_argument("--review-packet-dir", type=str, default=None, dest="review_packet_dir")
    p.add_argument("--last", type=int, default=None, dest="last_n", metavar="N")
    p.add_argument("--since", type=str, default=None, help="YYYY-MM-DD inclusive UTC-day cutoff.")
    p.add_argument("--out", type=str, required=True, help="Output JSON report path.")
    p.add_argument("--markdown-out", type=str, default=None, dest="markdown_out")
    p.add_argument("--json", action="store_true", help="Print report JSON to stdout.")
    args = p.parse_args(argv)
    root = args.repo_root or Path(__file__).resolve().parent.parent.parent
    args.repo_root = str(Path(root).resolve())
    if args.last_n is not None and args.since:
        p.error("Use either --last N or --since YYYY-MM-DD, not both.")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    rr_arg = Path(args.runtime_root)
    runtime_root = rr_arg.resolve() if rr_arg.is_absolute() else (repo_root / rr_arg).resolve()

    win_mode = "all"
    last_n = None
    since_dt: date | None = None
    if args.last_n is not None:
        win_mode = "last_n"
        last_n = args.last_n
    elif args.since:
        win_mode = "since"
        since_dt = date.fromisoformat(args.since)

    out_path = Path(args.out)
    outp = out_path.resolve() if out_path.is_absolute() else (repo_root / out_path).resolve()
    if is_forbidden_record_path(outp, repo_root):
        print(f"Refusing forbidden output path: {outp}", file=sys.stderr)
        return 2

    md_path: Path | None = None
    if args.markdown_out:
        mp = Path(args.markdown_out)
        md_path = mp.resolve() if mp.is_absolute() else (repo_root / mp).resolve()
        if is_forbidden_record_path(md_path, repo_root):
            print(f"Refusing forbidden markdown output path: {md_path}", file=sys.stderr)
            return 2

    report = build_report(
        repo_root=repo_root,
        runtime_root=runtime_root,
        receipts_dir=args.receipts_dir,
        validation_dir=args.validation_dir,
        task_shape_dir=args.task_shape_dir,
        review_packet_dir=args.review_packet_dir,
        window_mode=win_mode,
        last_n=last_n,
        since=since_dt,
    )

    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if md_path:
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(render_observability_markdown(report), encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
