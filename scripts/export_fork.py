#!/usr/bin/env python3
"""
Export the cognitive fork to a single portable JSON file.

Reads self.md, skills.md, self-evidence.md, and self-library.md for the given user and optionally
fork-manifest.json / manifest.json, then writes a structured JSON export for backup, portability,
or external tooling.

Usage:
    python scripts/export_fork.py
    python scripts/export_fork.py --user grace-mar --output fork-export.json
    python scripts/export_fork.py --user grace-mar --format obsidian --output obsidian-vault
    python scripts/export_fork.py --user grace-mar --format json-ld --output grace-mar.jsonld
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _parse_self_summary(content: str) -> dict:
    """Minimal summary: name, age, lexile, IX counts."""
    data = {"name": "?", "age": 0, "lexile_output": "?", "ix_a_count": 0, "ix_b_count": 0, "ix_c_count": 0}
    if m := re.search(r"name:\s*(\S+)", content):
        data["name"] = m.group(1)
    if m := re.search(r"age:\s*(\d+)", content):
        data["age"] = int(m.group(1))
    if m := re.search(r'lexile_output:\s*["\']?([^"\'\n]+)', content):
        data["lexile_output"] = m.group(1).strip()
    data["ix_a_count"] = len(re.findall(r"id:\s+LEARN-\d+", content))
    data["ix_b_count"] = len(re.findall(r"id:\s+CUR-\d+", content))
    data["ix_c_count"] = len(re.findall(r"id:\s+PER-\d+", content))
    return data


def _parse_evidence_summary(content: str) -> dict:
    """Counts of READ, WRITE, CREATE entries."""
    return {
        "read_count": len(re.findall(r"id:\s+READ-\d+", content)),
        "write_count": len(re.findall(r"id:\s+WRITE-\d+", content)),
        "create_count": len(re.findall(r"id:\s+CREATE-\d+", content)),
    }


def export_fork(user_id: str = "grace-mar", include_raw: bool = True) -> dict:
    """Build the fork export structure."""
    profile_dir = REPO_ROOT / "users" / user_id
    self_path = profile_dir / "self.md"
    skills_path = profile_dir / "skills.md"
    evidence_path = profile_dir / "self-evidence.md"
    library_path = profile_dir / "self-library.md"
    fork_manifest_path = profile_dir / "fork-manifest.json"
    agent_manifest_path = profile_dir / "manifest.json"

    self_raw = _read(self_path)
    skills_raw = _read(skills_path)
    evidence_raw = _read(evidence_path)
    library_raw = _read(library_path)

    out = {
        "version": "1.0",
        "format": "grace-mar-fork-export",
        "generated_at": datetime.now().isoformat(),
        "user_id": user_id,
        "summary": {
            "self": _parse_self_summary(self_raw) if self_raw else {},
            "evidence": _parse_evidence_summary(evidence_raw) if evidence_raw else {},
            "skills_present": bool(skills_raw),
        },
    }
    if include_raw:
        out["self"] = {"raw": self_raw}
        out["skills"] = {"raw": skills_raw}
        out["evidence"] = {"raw": evidence_raw}
        out["library"] = {"raw": library_raw}
    if fork_manifest_path.exists():
        try:
            out["fork_manifest"] = json.loads(fork_manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            out["fork_manifest"] = None
    if agent_manifest_path.exists():
        try:
            out["agent_manifest"] = json.loads(agent_manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            out["agent_manifest"] = None
    return out


def export_obsidian(data: dict, out_path: Path) -> None:
    """Write Obsidian-friendly markdown files with YAML frontmatter and internal links."""
    out_path.mkdir(parents=True, exist_ok=True)
    summary = data.get("summary", {})
    self_sum = summary.get("self", {})
    ev_sum = summary.get("evidence", {})

    def write_md(name: str, frontmatter: dict, body: str) -> None:
        lines = ["---"] + [f"{k}: {v}" for k, v in frontmatter.items()] + ["---", "", body]
        (out_path / f"{name}.md").write_text("\n".join(lines), encoding="utf-8")

    write_md(
        "SELF",
        {"type": "self", "user_id": data.get("user_id", ""), "generated_at": data.get("generated_at", "")},
        data.get("self", {}).get("raw", "(no self)"),
    )
    write_md(
        "Skills",
        {"type": "skills", "user_id": data.get("user_id", "")},
        data.get("skills", {}).get("raw", "(no skills)"),
    )
    write_md(
        "Evidence",
        {"type": "evidence", "read_count": ev_sum.get("read_count", 0), "write_count": ev_sum.get("write_count", 0), "create_count": ev_sum.get("create_count", 0)},
        data.get("evidence", {}).get("raw", "(no evidence)"),
    )
    write_md(
        "Library",
        {"type": "library"},
        data.get("library", {}).get("raw", "(no library)"),
    )
    (out_path / "README.md").write_text(
        f"# Fork export — {data.get('user_id', '?')}\n\nGenerated {data.get('generated_at', '')}. See [[SELF]], [[Skills]], [[Evidence]], [[Library]].\n",
        encoding="utf-8",
    )


def export_jsonld(data: dict) -> dict:
    """Return a JSON-LD graph with @context and typed nodes (provenance + mind model)."""
    summary = data.get("summary", {})
    self_sum = summary.get("self", {})
    return {
        "@context": {
            "@vocab": "https://grace-mar.com/ns/",
            "schema": "https://schema.org/",
            "name": "schema:name",
            "description": "schema:description",
            "generated_at": "schema:dateCreated",
            "user_id": "schema:identifier",
        },
        "@id": f"https://grace-mar.com/fork/{data.get('user_id', '')}",
        "@type": "Person",
        "name": self_sum.get("name", "?"),
        "description": "Cognitive fork export — Record (SELF, SKILLS, EVIDENCE)",
        "generated_at": data.get("generated_at"),
        "user_id": data.get("user_id"),
        "summary": {
            "ix_a_count": self_sum.get("ix_a_count", 0),
            "ix_b_count": self_sum.get("ix_b_count", 0),
            "ix_c_count": self_sum.get("ix_c_count", 0),
            **summary.get("evidence", {}),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Export fork to portable JSON")
    parser.add_argument("--user", "-u", default="grace-mar", help="User id (e.g. grace-mar)")
    parser.add_argument("--output", "-o", default=None, help="Output file or directory (default: stdout for default format)")
    parser.add_argument("--no-raw", action="store_true", help="Omit raw file contents (summary + manifest only)")
    parser.add_argument("--format", "-f", choices=("default", "obsidian", "json-ld"), default="default", help="Export format: default (JSON), obsidian (MD vault), json-ld")
    args = parser.parse_args()
    data = export_fork(user_id=args.user, include_raw=not args.no_raw)

    if args.format == "obsidian":
        out_path = Path(args.output or "obsidian-export")
        export_obsidian(data, out_path)
        print(f"Wrote Obsidian vault to {out_path}", file=__import__("sys").stderr)
        return
    if args.format == "json-ld":
        ld = export_jsonld(data)
        text = json.dumps(ld, indent=2, ensure_ascii=False)
        if args.output:
            Path(args.output).write_text(text, encoding="utf-8")
            print(f"Wrote {args.output}", file=__import__("sys").stderr)
        else:
            print(text)
        return

    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"Wrote {args.output}", file=__import__("sys").stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
