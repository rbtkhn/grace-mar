#!/usr/bin/env python3
"""
Export the cognitive fork to a single portable JSON file.

Ontology in export (v1.1+): **self_knowledge** (IX-A slice = SELF-KNOWLEDGE), **self_library**
(with **civ_mem.lib_entry_ids** = CIV-MEM subdomain of SELF-LIBRARY), plus **self**, **skills**,
**evidence**, **library.raw**. See docs/boundary-self-knowledge-self-library.md.

Reads self.md, self-skills.md (or legacy skills.md), self-archive.md (EVIDENCE; optional self-evidence.md
pointer), and self-library.md for the given user and optionally
fork-manifest.json / manifest.json, then writes structured JSON for backup, portability,
or external tooling.

Usage:
    python scripts/export_fork.py
    python scripts/export_fork.py --user grace-mar --output fork-export.json
    python scripts/export_fork.py --user grace-mar --format obsidian --output obsidian-vault
    python scripts/export_fork.py --user grace-mar --format json-ld --output grace-mar.jsonld
    python scripts/export_fork.py --format coach-handoff --output coach-handoff.json  # JSON + .md one-pager
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

try:
    from repo_io import read_path, REPO_ROOT, profile_dir, DEFAULT_USER_ID, resolve_surface_markdown_path
except ImportError:
    from scripts.repo_io import read_path, REPO_ROOT, profile_dir, DEFAULT_USER_ID, resolve_surface_markdown_path

try:
    from surface_aliases import library_export_labels
except ImportError:
    from scripts.surface_aliases import library_export_labels


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


def _parse_ix_b_entries(content: str) -> list[dict]:
    """Extract IX-B CURIOSITY entries (id, topic, one-liner) for coach handoff."""
    entries = []
    start = content.find("### IX-B. CURIOSITY")
    if start < 0:
        return entries
    block = content[start : content.find("### IX-C", start)]
    for m in re.finditer(
        r"-\s+id:\s+(CUR-\d+)\s*\n(.*?)(?=\n\s+-\s+id:\s+CUR-|\n```|\Z)",
        block,
        re.DOTALL,
    ):
        cur_id, rest = m.group(1), m.group(2)
        topic = ""
        response_signal = ""
        for line in rest.splitlines():
            if line.strip().startswith("topic:"):
                topic = line.split(":", 1)[1].strip().strip('"\'')
            elif line.strip().startswith("response_signal:"):
                response_signal = line.split(":", 1)[1].strip().strip('"\'')
        one_liner = response_signal if response_signal else topic
        entries.append({"id": cur_id, "topic": topic, "one_liner": one_liner[:300]})
    return entries


def _extract_ix_a_block(content: str) -> str:
    """IX-A (SELF-KNOWLEDGE) markdown slice for logical export bucket."""
    if not content:
        return ""
    start = content.find("### IX-A")
    if start < 0:
        return ""
    end = content.find("### IX-B", start)
    return content[start : end if end > 0 else start + 12000].strip()


def _civ_mem_lib_ids(library_raw: str) -> list[str]:
    """LIB ids whose entry block mentions CIV-MEM / CMC / civilization_memory scopes."""
    if not library_raw:
        return []
    marker = re.compile(r"civilization_memory|civ_mem|\bcmc\b|civilization-memory", re.I)
    ids: list[str] = []
    for m in re.finditer(r"\n  - id:\s*(LIB-[\w-]+)\s*\n", library_raw):
        nxt = library_raw.find("\n  - id: LIB-", m.end())
        block = library_raw[m.start() : nxt if nxt > 0 else m.start() + 3000]
        if marker.search(block):
            ids.append(m.group(1))
    return ids


def _parse_ix_c_entries(content: str) -> list[dict]:
    """Extract IX-C PERSONALITY entries (id, type, observation) for coach handoff."""
    entries = []
    start = content.find("### IX-C. PERSONALITY")
    if start < 0:
        return entries
    block = content[start : start + 8000]
    for m in re.finditer(
        r"-\s+id:\s+(PER-\d+)\s*\n(.*?)(?=\n\s+-\s+id:\s+PER-|\n```|\Z)",
        block,
        re.DOTALL,
    ):
        per_id, rest = m.group(1), m.group(2)
        obs_type = ""
        observation = ""
        for line in rest.splitlines():
            if line.strip().startswith("type:"):
                obs_type = line.split(":", 1)[1].strip()
            elif line.strip().startswith("observation:"):
                observation = line.split(":", 1)[1].strip().strip('"\'')
        entries.append(
            {"id": per_id, "type": obs_type, "observation": observation[:400]}
        )
    return entries


def export_fork(user_id: str = "grace-mar", include_raw: bool = True) -> dict:
    """Build the fork export structure."""
    user_dir = profile_dir(user_id)
    self_path = user_dir / "self.md"
    skills_path = resolve_surface_markdown_path(user_dir, "self_skills")
    evidence_path = resolve_surface_markdown_path(user_dir, "self_evidence")
    library_path = user_dir / "self-library.md"
    fork_manifest_path = user_dir / "fork-manifest.json"
    agent_manifest_path = user_dir / "manifest.json"

    self_raw = read_path(self_path)
    skills_raw = read_path(skills_path)
    evidence_raw = read_path(evidence_path)
    library_raw = read_path(library_path)

    civ_ids = _civ_mem_lib_ids(library_raw or "")
    out = {
        "version": "1.2",
        "format": "grace-mar-fork-export",
        "generated_at": datetime.now().isoformat(),
        "user_id": user_id,
        "ontology": {
            "self": "full identity markdown (`self.md`)",
            "self_knowledge": "IX-A slice only — SELF-KNOWLEDGE; identity-facing",
            "self_library": "reference-facing; civ_mem nested object = CIV-MEM subdomain of SELF-LIBRARY",
            "self_skills": "capability index (`self-skills.md`; legacy `skills.md`)",
            "self_evidence": "activity / provenance logs (`self-archive.md`; optional `self-evidence.md` pointer)",
            "skills": "deprecated mirror of self_skills",
            "evidence": "deprecated mirror of self_evidence",
        },
        "surface_labels": library_export_labels(),
        "_compat": {
            "deprecated_keys": {
                "skills": "self_skills",
                "evidence": "self_evidence",
                "library": "self_library",
            },
            "surface_registry": "scripts/surface_aliases.py",
        },
        "summary": {
            "self": _parse_self_summary(self_raw) if self_raw else {},
            "evidence": _parse_evidence_summary(evidence_raw) if evidence_raw else {},
            "skills_present": bool(skills_raw),
        },
        "self_knowledge": {
            "ix_a_markdown": _extract_ix_a_block(self_raw or ""),
            "note": "SELF-KNOWLEDGE (IX-A) logical bucket; full identity in self",
        },
        "self_library": {
            "civ_mem": {
                "lib_entry_ids": civ_ids,
                "note": "CIV-MEM subdomain of SELF-LIBRARY; not SELF-KNOWLEDGE",
            },
            "other_domains": {
                "note": "Remaining LIB entries by scope — see library.raw or self-library.md",
            },
        },
    }
    if include_raw:
        out["self"] = {"raw": self_raw}
        out["self_skills"] = {"raw": skills_raw}
        out["self_evidence"] = {"raw": evidence_raw}
        out["skills"] = {"raw": skills_raw}
        out["evidence"] = {"raw": evidence_raw}
        out["library"] = {"raw": library_raw}
        out["self_library"]["raw"] = library_raw
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
    skills_raw = (data.get("self_skills") or data.get("skills") or {}).get("raw", "(no skills)")
    write_md(
        "Skills",
        {"type": "skills", "user_id": data.get("user_id", "")},
        skills_raw,
    )
    evidence_raw_obs = (data.get("self_evidence") or data.get("evidence") or {}).get(
        "raw", "(no evidence)"
    )
    write_md(
        "Evidence",
        {"type": "evidence", "read_count": ev_sum.get("read_count", 0), "write_count": ev_sum.get("write_count", 0), "create_count": ev_sum.get("create_count", 0)},
        evidence_raw_obs,
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


def _write_coach_handoff_onepager(handoff: dict, out_path: Path) -> None:
    """Write a human-readable one-pager (markdown) for coach handoff."""
    name = handoff.get("name", "?")
    generated_at = handoff.get("generated_at", "")
    interests = handoff.get("interests", [])
    style_traits = handoff.get("style_traits", [])
    ev = handoff.get("evidence_summary", {})
    json_basename = out_path.with_suffix(".json").name

    lines = [
        f"# Coach handoff — {name}",
        "",
        f"*Generated {generated_at}*",
        "",
        "## Interests (IX-B)",
        "",
    ]
    if interests:
        for e in interests:
            one_liner = e.get("one_liner") or e.get("topic", "").strip()
            lines.append(f"- {one_liner}" if one_liner else "- (no summary)")
    else:
        lines.append("None documented.")
    lines.extend(["", "## Style / personality (IX-C)", ""])
    if style_traits:
        for e in style_traits:
            obs = (e.get("observation") or "").strip()
            t = (e.get("type") or "").strip()
            if t and obs:
                lines.append(f"- **{t}:** {obs}")
            elif obs:
                lines.append(f"- {obs}")
            else:
                lines.append("- (no observation)")
    else:
        lines.append("None documented.")
    lines.extend([
        "",
        "## Evidence summary",
        "",
        f"- Read: {ev.get('read_count', 0)}",
        f"- Write: {ev.get('write_count', 0)}",
        f"- Create: {ev.get('create_count', 0)}",
        "",
        f"*Generated by Grace-Mar coach-handoff export. Full JSON: {json_basename}*",
    ])
    out_path.write_text("\n".join(lines), encoding="utf-8")


def export_coach_handoff(data: dict) -> dict:
    """Build coach-handoff export: interests (IX-B), style_traits (IX-C), summary. No raw content."""
    self_raw = data.get("self", {}).get("raw", "")
    summary = data.get("summary", {})
    self_sum = summary.get("self", {})
    ev_sum = summary.get("evidence", {})
    return {
        "version": "1.0",
        "format": "coach-handoff",
        "generated_at": data.get("generated_at", ""),
        "user_id": data.get("user_id", ""),
        "name": self_sum.get("name", "?"),
        "interests": _parse_ix_b_entries(self_raw),
        "style_traits": _parse_ix_c_entries(self_raw),
        "evidence_summary": ev_sum,
    }


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
    import warnings

    warnings.warn(
        "export_fork.py is deprecated; use: python scripts/export.py fork -- [<args>]",
        DeprecationWarning,
        stacklevel=1,
    )
    parser = argparse.ArgumentParser(description="Export fork to portable JSON")
    parser.add_argument("--user", "-u", default=DEFAULT_USER_ID, help="User id (e.g. grace-mar)")
    parser.add_argument("--output", "-o", default=None, help="Output file or directory (default: stdout for default format)")
    parser.add_argument("--no-raw", action="store_true", help="Omit raw file contents (summary + manifest only)")
    parser.add_argument("--format", "-f", choices=("default", "obsidian", "json-ld", "coach-handoff"), default="default", help="Export format: default (JSON), obsidian (MD vault), json-ld, coach-handoff (interests + style for handoffs)")
    args = parser.parse_args()
    data = export_fork(user_id=args.user, include_raw=not args.no_raw)

    if args.format == "coach-handoff":
        handoff = export_coach_handoff(data)
        text = json.dumps(handoff, indent=2, ensure_ascii=False)
        out_json = Path(args.output or f"coach-handoff-{args.user}.json")
        out_json.write_text(text, encoding="utf-8")
        md_path = out_json.with_suffix(".md")
        _write_coach_handoff_onepager(handoff, md_path)
        print(f"Wrote coach-handoff to {out_json} and {md_path}", file=__import__("sys").stderr)
        return
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
