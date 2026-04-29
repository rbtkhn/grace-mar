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

BUILDER_VERSION = "1.0.0"
DEFAULT_NEIGHBOR_LIMIT = 250


def _posix_relative(base: Path, target: Path) -> str:
    rel = target.relative_to(base)
    return rel.as_posix()


def _reject_dotgit(path: Path) -> None:
    if ".git" in path.parts:
        raise ValueError(f"path resolves under .git (forbidden): {path}")


def _is_inside_checkout(checkout_res: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(checkout_res)
        return True
    except ValueError:
        return False


def resolve_subject_under_checkout(checkout: Path, subject_rel: str) -> Path:
    """Return absolute Path to subject; raise ValueError if traversal or outside checkout."""
    if not checkout.is_dir():
        raise ValueError(f"checkout is not a directory: {checkout}")
    rel = Path(subject_rel.replace("\\", "/"))
    if rel.is_absolute():
        raise ValueError("subject must be relative to checkout")
    if ".." in rel.parts:
        raise ValueError("subject must not contain path traversal (..)")
    full = (checkout / rel).resolve()
    checkout_res = checkout.resolve()
    try:
        full.relative_to(checkout_res)
    except ValueError as e:
        raise ValueError("subject escapes checkout root") from e
    _reject_dotgit(full)
    if not full.exists():
        raise ValueError(f"subject path does not exist: {full}")
    return full


def compute_neighbors(
    checkout: Path,
    subject: Path,
    *,
    neighbor_limit: int,
) -> tuple[list[dict[str, str]], bool, list[str]]:
    """Return (neighbor dicts with path_relative + edge, truncated flag, warnings)."""
    warnings: list[str] = []
    checkout_res = checkout.resolve()
    subject = subject.resolve()
    raw: list[tuple[str, str]] = []

    def list_visible(directory: Path) -> list[Path]:
        out: list[Path] = []
        if not directory.is_dir():
            return out
        try:
            for entry in sorted(directory.iterdir(), key=lambda p: p.name.lower()):
                if entry.name.startswith("."):
                    continue
                ent_res = entry.resolve()
                try:
                    ent_res.relative_to(checkout_res)
                except ValueError:
                    continue
                if ".git" in ent_res.parts:
                    continue
                out.append(entry)
        except OSError as e:
            warnings.append(f"listdir failed for {directory}: {e}")
        return out

    if subject.is_file():
        container = subject.parent
        sub_name = subject.name
        peers = list_visible(container)
        for p in peers:
            if p.name == sub_name:
                continue
            raw.append((_posix_relative(checkout_res, p.resolve()), "same_directory"))
        parent = container.parent
        if _is_inside_checkout(checkout_res, parent):
            for p in list_visible(parent):
                raw.append((_posix_relative(checkout_res, p.resolve()), "parent_directory"))
    elif subject.is_dir():
        for p in list_visible(subject):
            raw.append((_posix_relative(checkout_res, p.resolve()), "same_directory"))
        parent = subject.parent
        if _is_inside_checkout(checkout_res, parent):
            subj_name = subject.name
            for p in list_visible(parent):
                if p.name == subj_name:
                    continue
                raw.append((_posix_relative(checkout_res, p.resolve()), "parent_directory"))
    else:
        raise ValueError(f"subject is neither file nor directory: {subject}")

    seen: set[str] = set()
    deduped: list[tuple[str, str]] = []
    for path_rel, edge in sorted(raw, key=lambda x: (x[0], x[1])):
        if path_rel in seen:
            continue
        seen.add(path_rel)
        deduped.append((path_rel, edge))

    truncated = len(deduped) > neighbor_limit
    slice_ = deduped[:neighbor_limit]
    neighbors = [{"path_relative": pr, "edge": ed} for pr, ed in slice_]
    return neighbors, truncated, warnings


def build_report(
    repo_root: Path,
    checkout_relative: str,
    subject_relative: str,
    *,
    generated_at: datetime | None = None,
    neighbor_limit: int = DEFAULT_NEIGHBOR_LIMIT,
    include_checkout_absolute: bool = True,
) -> dict:
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

    report: dict = {
        "report_type": "external_codex_neighborhood_report",
        "schema_version": "v1",
        "report_id": report_id,
        "generated_at": ts,
        "checkout_relative": checkout_relative.replace("\\", "/"),
        "subject_relative": Path(subject_relative).as_posix(),
        "subject_kind": subject_kind,
        "builder_version": BUILDER_VERSION,
        "neighbor_limit": neighbor_limit,
        "truncated": truncated,
        "neighbors": neighbors,
    }
    if include_checkout_absolute:
        report["checkout_absolute"] = str(checkout)
    if warnings:
        report["warnings"] = warnings
    return report


def write_summary_md(report: dict, path: Path) -> None:
    lines = [
        "# External codex neighborhood (derived)",
        "",
        f"- **report_id:** `{report['report_id']}`",
        f"- **generated_at:** {report['generated_at']}",
        f"- **checkout:** `{report['checkout_relative']}`",
        f"- **subject:** `{report['subject_relative']}`",
        f"- **truncated:** {report['truncated']}",
        "",
        "## Neighbors (structural only)",
        "",
    ]
    for n in report["neighbors"]:
        lines.append(f"- `{n['path_relative']}` ({n['edge']})")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


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
    parser.add_argument("--write-md", action="store_true", help="Also write .summary.md")
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
    json_path = out_dir / f"{stem}.json"
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json_path.as_posix())
    if args.write_md:
        md_path = out_dir / f"{stem}.summary.md"
        write_summary_md(report, md_path)
        print(md_path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
