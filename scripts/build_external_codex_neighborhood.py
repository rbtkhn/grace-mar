#!/usr/bin/env python3
"""Build a structural neighborhood report for a path inside an external codex checkout.

WORK-only — derived receipt; not Record truth. See docs/skill-work/work-dev/external-codex-explorer.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from external_codex_common import (
    civilization_token_from_path,
    compute_neighbor_edges,
    extract_markdown_title,
    infer_file_class,
    is_governance_template_path,
    is_index_core_scholar_path,
    resolve_subject_under_checkout,
)

BUILDER_VERSION = "1.1.0"
DEFAULT_NEIGHBOR_LIMIT = 250
_SUGGESTED_K = 5

_EDGE_WEIGHT = {"same_directory": 3, "parent_directory": 1}


def compute_neighbors(
    checkout: Path,
    subject: Path,
    *,
    neighbor_limit: int,
) -> tuple[list[dict[str, str]], bool, list[str]]:
    """Return (neighbor dicts with path_relative + edge, truncated flag, warnings)."""
    deduped, warnings = compute_neighbor_edges(checkout, subject)
    truncated = len(deduped) > neighbor_limit
    slice_ = deduped[:neighbor_limit]
    neighbors = [{"path_relative": pr, "edge": ed} for pr, ed in slice_]
    return neighbors, truncated, warnings


def mechanical_reason(edge: str, section: str, neighbor_civ: str | None, subject_civ: str | None) -> str:
    _ = neighbor_civ, subject_civ
    if section == "same_civilization":
        return (
            f"same civilization folder cluster as subject"
            + (f" (`{subject_civ}`)" if subject_civ else "")
            + f"; edge={edge}"
        )
    if section == "same_file_class":
        return f"same inferred filename class as subject; edge={edge}"
    if section == "index_core_scholar":
        return f"path/filename matches index-memory-state-minds heuristic; edge={edge}"
    if section == "governance_template":
        return f"path/filename matches template-or-templates heuristic; edge={edge}"
    return f"filesystem structural neighbor; edge={edge}"


def assign_section(
    subject_civ: str | None,
    subject_class: str,
    neigh_path: str,
    neigh_edge: str,
) -> str:
    _ = neigh_edge
    nb = Path(neigh_path).name
    nciv = civilization_token_from_path(neigh_path)
    nclass = infer_file_class(nb)

    if subject_civ and nciv == subject_civ:
        return "same_civilization"
    if subject_class != "other" and nclass == subject_class:
        return "same_file_class"
    if is_index_core_scholar_path(neigh_path, nb):
        return "index_core_scholar"
    if is_governance_template_path(neigh_path, nb):
        return "governance_template"
    return "other_structural"


def enrich_neighbor_rows(
    neighbors: list[dict[str, str]],
    subject_rel: str,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    sub_norm = subject_rel.replace("\\", "/")
    sub_base = Path(sub_norm).name
    subject_civ = civilization_token_from_path(sub_norm)
    subject_class = infer_file_class(sub_base)

    rows: list[dict[str, object]] = []
    edge_counts: dict[str, int] = {}
    for n in neighbors:
        pr = n["path_relative"]
        ed = n["edge"]
        edge_counts[ed] = edge_counts.get(ed, 0) + 1
        nb = Path(pr).name
        nciv = civilization_token_from_path(pr)
        nclass = infer_file_class(nb)
        sec = assign_section(subject_civ, subject_class, pr, ed)
        reason = mechanical_reason(ed, sec, nciv, subject_civ)
        rows.append(
            {
                "path_relative": pr,
                "edge": ed,
                "reason": reason,
                "section": sec,
                "file_class": nclass,
                "civilization_token": nciv,
            }
        )

    dominant_edge = max(edge_counts.items(), key=lambda x: (x[1], x[0]))[0] if edge_counts else "same_directory"

    likely_family: dict[str, object] = {
        "subject_civilization_guess": subject_civ,
        "subject_file_class_guess": subject_class,
        "dominant_edge_among_neighbors": dominant_edge,
        "notes": [
            "Heuristic labels only — non-authoritative.",
            "Same civilization cluster when path contains content/civilizations/<ID>/...",
        ],
    }
    return rows, likely_family


def inspection_score(
    subject_civ: str | None,
    subject_class: str,
    row: dict[str, object],
) -> int:
    sc = _EDGE_WEIGHT.get(str(row["edge"]), 0)
    nciv = row.get("civilization_token")
    if subject_civ and nciv == subject_civ:
        sc += 4
    if subject_class != "other" and row.get("file_class") == subject_class:
        sc += 2
    elif subject_class == "other" and row.get("file_class") == "other":
        sc += 1
    sec = str(row.get("section", ""))
    if sec in ("index_core_scholar", "governance_template"):
        sc += 1
    return sc


def suggested_inspection_targets(
    rows: list[dict[str, object]],
    subject_rel: str,
    *,
    k: int = _SUGGESTED_K,
) -> list[dict[str, object]]:
    sub_norm = subject_rel.replace("\\", "/")
    subject_civ = civilization_token_from_path(sub_norm)
    subject_class = infer_file_class(Path(sub_norm).name)
    ranked = sorted(
        rows,
        key=lambda r: (-inspection_score(subject_civ, subject_class, r), str(r["path_relative"])),
    )
    out: list[dict[str, object]] = []
    seen: set[str] = set()
    for r in ranked:
        if len(out) >= k:
            break
        pr = str(r["path_relative"])
        if pr in seen:
            continue
        seen.add(pr)
        score = inspection_score(subject_civ, subject_class, r)
        why = (
            f"deterministic score={score} (edge weight + civ/class/section bonuses); "
            f"compare with subject `{sub_norm}`."
        )
        out.append({"path_relative": pr, "reason": why, "score": score})
    return out


def render_companion_markdown(report: dict[str, object]) -> str:
    sub_rel = str(report["subject_relative"])
    sub_norm = sub_rel.replace("\\", "/")
    sub_base = Path(sub_rel).name
    subject_civ = civilization_token_from_path(sub_norm)
    subject_class = infer_file_class(sub_base)

    lines: list[str] = [
        "# External Codex Neighborhood Report",
        "",
        "## Subject",
        "",
        f"- **path:** `{sub_rel}`",
    ]
    st = report.get("subject_title")
    lines.append(f"- **title (first `#` line if present):** {st if st else '*none*'}")
    if subject_civ:
        lines.append(f"- **civilization (path heuristic):** `{subject_civ}`")
    else:
        lines.append("- **civilization (path heuristic):** *not inferred*")
    lines.extend(
        [
            f"- **file_class (filename heuristic):** `{subject_class}`",
            "",
            "## Likely family",
            "",
            "Compact mechanical summary (non-authoritative):",
            "",
        ]
    )
    lf = report.get("likely_family")
    if isinstance(lf, dict):
        for key in ("subject_civilization_guess", "subject_file_class_guess", "dominant_edge_among_neighbors"):
            if key in lf and lf[key] is not None:
                lines.append(f"- **{key}:** `{lf[key]}`")
        notes = lf.get("notes")
        if isinstance(notes, list):
            for note in notes:
                lines.append(f"- {note}")

    lines.extend(
        [
            "",
            "## Structural neighbors",
            "",
            "Grouped by deterministic rules (each neighbor appears once under first matching heading).",
            "",
        ]
    )

    section_order = [
        ("same_civilization", "Same civilization"),
        ("same_file_class", "Same file class"),
        ("index_core_scholar", "Nearby index / core / scholar files"),
        ("governance_template", "Governance / template neighbors"),
        ("other_structural", "Other structural neighbors"),
    ]
    nrows = report.get("neighbors")
    if not isinstance(nrows, list):
        nrows = []
    by_sec: dict[str, list[dict[str, object]]] = {k: [] for k, _ in section_order}
    for nr in nrows:
        if not isinstance(nr, dict):
            continue
        sec = str(nr.get("section", "other_structural"))
        by_sec.setdefault(sec, []).append(nr)

    for key, heading in section_order:
        items = sorted(by_sec.get(key, []), key=lambda x: str(x.get("path_relative", "")))
        lines.append(f"### {heading}")
        lines.append("")
        if not items:
            lines.append("*No neighbors in this bucket.*")
            lines.append("")
            continue
        for nr in items:
            pr = nr.get("path_relative", "")
            edge = nr.get("edge", "")
            reason = nr.get("reason", "")
            lines.append(f"- **path:** `{pr}`")
            lines.append(f"  - **title:** *(not extracted here — open file for `#` heading)*")
            lines.append(f"  - **edge:** `{edge}`")
            lines.append(f"  - **reason:** {reason}")
            lines.append("")

    sug_raw = report.get("suggested_next_inspection")
    nsug = len(sug_raw) if isinstance(sug_raw, list) else 0
    lines.extend(
        [
            "## Suggested next inspection targets",
            "",
            f"Top {min(_SUGGESTED_K, nsug)} paths "
            "by deterministic score (ties broken by path sort).",
            "",
        ]
    )
    sug = report.get("suggested_next_inspection")
    if isinstance(sug, list) and sug:
        for item in sug:
            if isinstance(item, dict):
                lines.append(f"- `{item.get('path_relative')}` — {item.get('reason')}")
        lines.append("")
    else:
        lines.append("*No suggestions (empty neighborhood).*")
        lines.append("")

    lines.extend(
        [
            "## Notes",
            "",
            "- **Derived report** — not canonical for the external checkout.",
            "- **Does not modify** upstream `civilization_memory` or any external repo files.",
            "- Relationships are **filesystem / naming heuristics only**, not doctrinal entailment.",
            "- Use the target repo's governance and primary sources for authoritative decisions.",
            "",
            f"- **Machine-readable JSON:** same run; **report_id:** `{report.get('report_id')}`",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def build_report(
    repo_root: Path,
    checkout_relative: str,
    subject_relative: str,
    *,
    generated_at: datetime | None = None,
    neighbor_limit: int = DEFAULT_NEIGHBOR_LIMIT,
    include_checkout_absolute: bool = True,
) -> dict[str, object]:
    checkout = (repo_root / checkout_relative).resolve()
    subject_path = resolve_subject_under_checkout(checkout, subject_relative)
    generated_at = generated_at or datetime.now(timezone.utc)
    ts = generated_at.isoformat().replace("+00:00", "Z")
    neighbors, truncated, warnings = compute_neighbors(
        checkout, subject_path, neighbor_limit=neighbor_limit
    )
    subject_kind = "directory" if subject_path.is_dir() else "file"
    rid_src = f"{checkout_relative}|{subject_relative}|{ts}".encode()
    report_id = hashlib.sha256(rid_src).hexdigest()[:24]

    sub_norm = subject_relative.replace("\\", "/")
    nrow, likely_family = enrich_neighbor_rows(neighbors, sub_norm)
    suggested = suggested_inspection_targets(nrow, sub_norm)
    subject_title = extract_markdown_title(subject_path) if subject_path.is_file() else None

    report: dict[str, object] = {
        "report_type": "external_codex_neighborhood_report",
        "schema_version": "v1",
        "report_id": report_id,
        "generated_at": ts,
        "checkout_relative": checkout_relative.replace("\\", "/"),
        "subject_relative": Path(subject_relative).as_posix(),
        "subject_kind": subject_kind,
        "subject_title": subject_title,
        "builder_version": BUILDER_VERSION,
        "neighbor_limit": neighbor_limit,
        "truncated": truncated,
        "neighbors": nrow,
        "likely_family": likely_family,
        "suggested_next_inspection": suggested,
    }
    if include_checkout_absolute:
        report["checkout_absolute"] = str(checkout)
    if warnings:
        report["warnings"] = warnings
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="External codex structural neighborhood report.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Grace-mar repository root",
    )
    parser.add_argument(
        "--checkout",
        default="research/repos/civilization_memory",
        help="Checkout path relative to repo root",
    )
    parser.add_argument("--subject", required=True, help="Path relative to checkout")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("artifacts/external-codex"),
        help="Output directory (relative to repo root unless absolute)",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=None,
        help="Explicit JSON output path (default: out-dir/<stem>.json)",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=None,
        help="Explicit Markdown companion path (requires --write-md)",
    )
    parser.add_argument(
        "--write-md",
        action="store_true",
        help="Write human-readable Markdown companion report (.neighborhood.md)",
    )
    parser.add_argument("--neighbor-limit", type=int, default=DEFAULT_NEIGHBOR_LIMIT)
    args = parser.parse_args(argv)

    repo_root = args.repo_root.resolve()
    out_dir = args.out_dir if args.out_dir.is_absolute() else (repo_root / args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        report = build_report(
            repo_root,
            args.checkout,
            args.subject,
            neighbor_limit=args.neighbor_limit,
        )
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    stem = Path(args.subject.replace("\\", "/")).as_posix().replace("/", "__").replace(":", "_")
    if len(stem) > 120:
        stem = stem[:120]

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
        md_body = render_companion_markdown(report)
        md_path = args.output_md
        if md_path is None:
            md_path = out_dir / f"{stem}.neighborhood.md"
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
