#!/usr/bin/env python3
"""Build a cluster-level structural summary for files matching a selector inside an external codex checkout.

WORK-only — derived receipt; not Record truth. See docs/skill-work/work-dev/external-codex-explorer.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from external_codex_common import (
    checkout_relative_to_repo,
    civilization_token_from_path,
    compute_neighbor_relative_paths,
    extract_markdown_title,
    infer_file_class,
    posix_relative,
    resolve_repo_path,
)

BUILDER_VERSION = "1.0.0"
DEFAULT_MEMBER_LIMIT = 5000
_SUGGESTED_K = 5
_MOST_CONNECTED_K = 10
_LOW_LINK_NOTE_CAP = 25


def passes_selector(rel_posix: str, basename: str, selector_type: str, selector_value: str) -> bool:
    norm = rel_posix.replace("\\", "/")
    if selector_type == "civilization":
        needle = f"content/civilizations/{selector_value}/"
        return needle in norm
    if selector_type == "file_class":
        return infer_file_class(basename) == selector_value
    raise ValueError(f"unsupported selector type: {selector_type}")


def iter_files_under_checkout(checkout: Path) -> list[Path]:
    ck = checkout.resolve()
    out: list[Path] = []
    for p in ck.rglob("*"):
        if not p.is_file():
            continue
        try:
            rel = p.relative_to(ck)
        except ValueError:
            continue
        if ".git" in rel.parts:
            continue
        if any(part.startswith(".") for part in rel.parts):
            continue
        out.append(p)
    return sorted(out, key=lambda x: x.as_posix())


def filter_members(
    all_files: list[Path],
    checkout: Path,
    selector_type: str,
    selector_value: str,
) -> list[Path]:
    ck = checkout.resolve()
    matched: list[Path] = []
    for p in all_files:
        rel = posix_relative(ck, p.resolve())
        if passes_selector(rel, p.name, selector_type, selector_value):
            matched.append(p)
    return matched


def output_stem(selector_type: str, selector_value: str) -> str:
    raw = f"{selector_type}__{selector_value}"
    safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in raw.replace("/", "_"))
    return safe[:120] if len(safe) > 120 else safe


def connection_counts_for_members(
    checkout: Path,
    member_abs: list[Path],
) -> tuple[list[int], list[str]]:
    """Parallel list of counts + accumulated warnings (may contain duplicates)."""
    ck_res = checkout.resolve()
    member_rel_set = {posix_relative(ck_res, p.resolve()) for p in member_abs}
    counts: list[int] = []
    warnings: list[str] = []
    for abs_f in member_abs:
        rel_self = posix_relative(ck_res, abs_f.resolve())
        peers, w = compute_neighbor_relative_paths(checkout, abs_f)
        warnings.extend(w)
        cnt = sum(1 for n in peers if n in member_rel_set and n != rel_self)
        counts.append(cnt)
    return counts, warnings


def dominant_rows_from_members(member_paths_posix: list[str]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    fc = Counter(infer_file_class(Path(p).name) for p in member_paths_posix)
    civ_raw = [civilization_token_from_path(p) for p in member_paths_posix]
    cc = Counter(civ_raw)
    dom_fc = sorted(({"class": k, "count": v} for k, v in fc.items()), key=lambda x: (-int(x["count"]), str(x["class"])))
    dom_civ = sorted(({"civilization": k, "count": v} for k, v in cc.items()), key=lambda x: (-int(x["count"]), "" if x["civilization"] is None else str(x["civilization"])))
    return dom_fc, dom_civ


def suggested_entry_points_from_members(
    rows: list[tuple[str, int]],
    *,
    k: int,
) -> list[dict[str, object]]:
    """rows: (path, connection_count); deterministic (-cnt, path)."""
    ranked = sorted(rows, key=lambda x: (-x[1], x[0]))
    out: list[dict[str, object]] = []
    seen: set[str] = set()
    for path, cnt in ranked:
        if len(out) >= k:
            break
        if path in seen:
            continue
        seen.add(path)
        why = (
            f"deterministic rank by (-connection_count, path); connection_count={cnt}; "
            "filesystem structural peers intersect cluster members only."
        )
        out.append({"path": path, "reason": why, "connection_count": cnt})
    return out


def render_family_markdown(report: dict[str, object]) -> str:
    sel = report.get("selector")
    sel_type = sel.get("type") if isinstance(sel, dict) else ""
    sel_val = sel.get("value") if isinstance(sel, dict) else ""

    lines: list[str] = [
        "# External Codex Family Report",
        "",
        "## Selector",
        "",
        f"- **type:** `{sel_type}`",
        f"- **value:** `{sel_val}`",
        f"- **checkout_relative:** `{report.get('checkout_relative')}`",
        f"- **target_ref:** `{report.get('target_ref')}`",
        "",
        "## Summary",
        "",
        f"- **member_count:** {report.get('member_count')}",
        f"- **truncated:** {report.get('truncated')}",
        f"- **member_limit:** {report.get('member_limit')}",
        "",
    ]

    dom_fc = report.get("dominant_file_classes")
    lines.append("### Dominant file classes (filename heuristic)")
    lines.append("")
    if isinstance(dom_fc, list) and dom_fc:
        for row in dom_fc:
            if isinstance(row, dict):
                lines.append(f"- `{row.get('class')}` — **count** {row.get('count')}")
    else:
        lines.append("*None.*")
    lines.extend(["", "### Dominant civilizations (path heuristic)", ""])

    dom_ci = report.get("dominant_civilizations")
    if isinstance(dom_ci, list) and dom_ci:
        for row in dom_ci:
            if isinstance(row, dict):
                c = row.get("civilization")
                lab = "(none)" if c is None else f"`{c}`"
                lines.append(f"- {lab} — **count** {row.get('count')}")
    else:
        lines.append("*None.*")

    lines.extend(["", "## Suggested entry points", "", "Top paths by (-connection_count, lexicographic path).", ""])

    sug = report.get("suggested_entry_points")
    if isinstance(sug, list) and sug:
        for item in sug:
            if isinstance(item, dict):
                lines.append(f"- `{item.get('path')}` — {item.get('reason')}")
        lines.append("")
    else:
        lines.extend(["*No members in cluster.*", ""])

    lines.extend(["## Most connected members", "", "Highest intra-cluster structural linkage (same metric).", ""])

    mc = report.get("most_connected_members")
    if isinstance(mc, list) and mc:
        for item in mc:
            if isinstance(item, dict):
                lines.append(
                    f"- `{item.get('path')}` — connection_count={item.get('connection_count')}"
                )
        lines.append("")
    else:
        lines.extend(["*None.*", ""])

    lines.extend(["## Members", "", "| path | file_class | connection_count | title |", "|------|------------|------------------|-------|"])

    members = report.get("members")
    if isinstance(members, list) and members:
        for m in sorted(members, key=lambda x: str(x.get("path", "")) if isinstance(x, dict) else ""):
            if not isinstance(m, dict):
                continue
            title = m.get("title")
            tcell = title if title else "—"
            if isinstance(tcell, str) and len(tcell) > 60:
                tcell = tcell[:57] + "..."
            lines.append(
                f"| `{m.get('path')}` | `{m.get('file_class')}` | {m.get('connection_count')} | {tcell} |"
            )
    else:
        lines.append("| *empty cluster* | — | — | — |")

    lines.extend(["", "## Notes", ""])

    notes = report.get("notes")
    if isinstance(notes, list) and notes:
        for n in notes:
            lines.append(f"- {n}")
    else:
        lines.append("- *(no notes)*")

    lines.extend(
        [
            "",
            "## Receipt",
            "",
            f"- **report_id:** `{report.get('report_id')}`",
            "- **Derived report** — not canonical for the external checkout.",
            "- **Does not modify** upstream repos or external checkout files.",
            "- Relationships are **filesystem / naming heuristics only**, not doctrinal entailment.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def build_family_report(
    repo_root: Path,
    repo_path: str | Path,
    selector_type: str,
    selector_value: str,
    *,
    generated_at: datetime | None = None,
    member_limit: int = DEFAULT_MEMBER_LIMIT,
    include_checkout_absolute: bool = True,
) -> dict[str, object]:
    if selector_type not in ("civilization", "file_class"):
        raise ValueError("selector_type must be civilization or file_class")

    repo_root = repo_root.resolve()
    checkout = resolve_repo_path(repo_root, repo_path)
    generated_at = generated_at or datetime.now(timezone.utc)
    ts = generated_at.isoformat().replace("+00:00", "Z")

    checkout_rel = checkout_relative_to_repo(repo_root, checkout)

    all_files = iter_files_under_checkout(checkout)
    matched = filter_members(all_files, checkout, selector_type, selector_value)
    truncated = len(matched) > member_limit
    warnings: list[str] = []
    if truncated:
        warnings.append(f"member enumeration truncated at member_limit={member_limit}")
        matched = matched[:member_limit]

    checkout_for_neighbors = checkout.resolve()

    ck_res = checkout_for_neighbors
    member_abs = matched
    counts: list[int] = []
    neighbor_warns: list[str] = []
    if member_abs:
        counts, neighbor_warns = connection_counts_for_members(checkout_for_neighbors, member_abs)

    warnings.extend(neighbor_warns)
    warnings = sorted(set(warnings))

    member_paths_posix = [posix_relative(ck_res, p.resolve()) for p in member_abs]
    rows_pairs = list(zip(member_paths_posix, counts, strict=True))

    member_rows: list[dict[str, object]] = []
    for abs_f, cnt in zip(member_abs, counts, strict=True):
        rel = posix_relative(ck_res, abs_f.resolve())
        member_rows.append(
            {
                "path": rel,
                "title": extract_markdown_title(abs_f),
                "civilization": civilization_token_from_path(rel),
                "file_class": infer_file_class(abs_f.name),
                "connection_count": cnt,
            }
        )

    dom_fc, dom_civ = dominant_rows_from_members(member_paths_posix)

    sug = suggested_entry_points_from_members(rows_pairs, k=_SUGGESTED_K)
    most_conn = suggested_entry_points_from_members(rows_pairs, k=_MOST_CONNECTED_K)

    notes: list[str] = [
        "Heuristic cluster summary — non-authoritative.",
        "Connections count structural peers (same_directory / parent_directory) that are also cluster members.",
    ]
    if not member_paths_posix:
        notes.append("Empty cluster after selector filter — broaden selector or verify checkout layout.")

    low_links = sorted([p for p, c in rows_pairs if c == 0])
    if low_links:
        sample = low_links[:_LOW_LINK_NOTE_CAP]
        extra = len(low_links) - len(sample)
        frag = ", ".join(f"`{x}`" for x in sample)
        msg = f"Members with zero intra-cluster structural peers (sample): {frag}"
        if extra > 0:
            msg += f" (+{extra} more)"
        notes.append(msg)

    rid_src = f"{checkout_rel}|{selector_type}|{selector_value}|{ts}".encode()
    report_id = hashlib.sha256(rid_src).hexdigest()[:24]

    report: dict[str, object] = {
        "report_type": "external_codex_family_report",
        "schema_version": "v1",
        "report_id": report_id,
        "generated_at": ts,
        "checkout_relative": checkout_rel.replace("\\", "/"),
        "target_ref": "working_tree",
        "selector": {"type": selector_type, "value": selector_value},
        "builder_version": BUILDER_VERSION,
        "member_limit": member_limit,
        "truncated": truncated,
        "member_count": len(member_rows),
        "members": sorted(member_rows, key=lambda x: str(x["path"])),
        "dominant_file_classes": dom_fc,
        "dominant_civilizations": dom_civ,
        "suggested_entry_points": sug,
        "most_connected_members": most_conn,
        "notes": notes,
    }
    if include_checkout_absolute:
        report["checkout_absolute"] = str(checkout.resolve())
    if warnings:
        report["warnings"] = warnings
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="External codex family / cluster structural summary.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Grace-mar repository root",
    )
    parser.add_argument(
        "--repo-path",
        required=True,
        help="Checkout directory path (relative to repo root or absolute)",
    )
    parser.add_argument(
        "--selector-type",
        required=True,
        choices=["civilization", "file_class"],
        help="Cluster selector",
    )
    parser.add_argument("--selector-value", required=True, help="e.g. ROME or memory_spine")
    parser.add_argument(
        "--output-json",
        type=Path,
        default=None,
        help="JSON output path (default: artifacts/external-codex/families/<stem>.json)",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=None,
        help="Markdown companion path (requires --write-md)",
    )
    parser.add_argument(
        "--write-md",
        action="store_true",
        help="Write companion Markdown (.family.md)",
    )
    parser.add_argument(
        "--member-limit",
        type=int,
        default=DEFAULT_MEMBER_LIMIT,
        help=f"Cap member enumeration (default {DEFAULT_MEMBER_LIMIT})",
    )
    args = parser.parse_args(argv)

    repo_root = args.repo_root.resolve()

    try:
        report = build_family_report(
            repo_root,
            args.repo_path,
            args.selector_type,
            args.selector_value,
            member_limit=args.member_limit,
        )
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    stem = output_stem(args.selector_type, args.selector_value)
    out_dir = repo_root / "artifacts" / "external-codex" / "families"
    json_path = args.output_json
    if json_path is None:
        json_path = out_dir / f"{stem}.json"
    elif not json_path.is_absolute():
        json_path = repo_root / json_path
    json_path = json_path.resolve()
    json_path.parent.mkdir(parents=True, exist_ok=True)

    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json_path.as_posix())

    if args.write_md:
        md_body = render_family_markdown(report)
        md_path = args.output_md
        if md_path is None:
            md_path = out_dir / f"{stem}.family.md"
        elif not md_path.is_absolute():
            md_path = repo_root / md_path
        md_path = md_path.resolve()
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(md_body, encoding="utf-8")
        print(md_path.as_posix())
    elif args.output_md is not None:
        print("error: --output-md requires --write-md", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
