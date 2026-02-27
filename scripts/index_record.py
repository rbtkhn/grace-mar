#!/usr/bin/env python3
"""
Record index for fast local search over SELF, EVIDENCE, recursion-gate.

Builds a term index for analyst dedup, PRP retrieval, and record lookup.
Aligns with civilization_memory-style cmc-index-search.

Usage:
  python scripts/index_record.py build [-u USER_ID]
  python scripts/index_record.py query "terms" [-u USER_ID]
  python scripts/index_record.py query "space Jupiter" -u grace-mar

Index stored in users/[id]/.index_record.json (gitignored recommended).
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER = "grace-mar"


def extract_yaml_blocks(content: str, after_marker: str | None = None) -> list[str]:
    """Extract YAML blocks from markdown."""
    if after_marker:
        idx = content.find(after_marker)
        if idx >= 0:
            content = content[idx:]
    return re.findall(r"```(?:yaml|yml)?\s*\n(.*?)```", content, re.DOTALL)


def tokenize(text: str) -> set[str]:
    """Lowercase, split on non-alphanumeric, filter short."""
    tokens = re.findall(r"[a-z0-9]{2,}", text.lower())
    return set(tokens)


def index_self(path: Path) -> list[dict]:
    """Extract IX-A/B/C entries for indexing."""
    hits = []
    content = path.read_text()
    for section, marker in [
        ("IX-A", "### IX-A. KNOWLEDGE"),
        ("IX-B", "### IX-B. CURIOSITY"),
        ("IX-C", "### IX-C. PERSONALITY"),
    ]:
        if marker not in content:
            continue
        blocks = extract_yaml_blocks(content, marker)
        for block in blocks:
            for m in re.finditer(r"id:\s*(LEARN-\d+|CUR-\d+|PER-\d+)", block):
                eid = m.group(1)
                start = max(0, m.start() - 200)
                end = min(len(block), m.end() + 400)
                snippet = block[start:end].replace("\n", " ")[:300]
                hits.append({
                    "type": section,
                    "id": eid,
                    "snippet": snippet,
                    "file": "self.md",
                })
            for m in re.finditer(r"topic:\s*[\"']?([^\"'\n]+)", block):
                topic = m.group(1).strip()
                hits.append({
                    "type": "topic",
                    "value": topic,
                    "file": "self.md",
                })
    return hits


def index_evidence(path: Path) -> list[dict]:
    """Extract ACT entries for indexing."""
    hits = []
    content = path.read_text()
    if "## V. ACTIVITY LOG" not in content:
        return hits
    idx = content.find("## V. ACTIVITY LOG")
    blocks = extract_yaml_blocks(content[idx:])
    for block in blocks:
        for m in re.finditer(r"id:\s*(ACT-\d+)", block):
            act_id = m.group(1)
            start = m.start()
            end = block.find("\n  - id:", start + 1)
            if end < 0:
                end = len(block)
            chunk = block[start:end]
            summary = ""
            for pat in [r"summary:\s*[\"']?([^\"'\n]+)", r"source:\s*[\"']?([^\"'\n]+)", r"activity_type:\s*[\"']?([^\"'\n]+)"]:
                mm = re.search(pat, chunk)
                if mm:
                    summary += " " + mm.group(1).strip()
            summary = summary.strip()[:400] or chunk[:200].replace("\n", " ")
            hits.append({
                "type": "ACT",
                "id": act_id,
                "snippet": summary,
                "file": "self-evidence.md",
            })
    return hits


def index_pending(path: Path) -> list[dict]:
    """Extract CANDIDATE entries (including pending) for indexing."""
    hits = []
    if not path.exists():
        return hits
    content = path.read_text()
    for m in re.finditer(r"CANDIDATE-(\d+)|### (CANDIDATE-\d+)", content):
        cid = m.group(1) or m.group(2)
        start = m.start()
        end = content.find("### ", start + 5)
        if end < 0:
            end = min(len(content), start + 800)
        chunk = content[start:end]
        summary = ""
        for pat in [r"summary:\s*[\"']?([^\"'\n]+)", r"mind_category:\s*[\"']?([^\"'\n]+)"]:
            mm = re.search(pat, chunk)
            if mm:
                summary += " " + mm.group(1).strip()
        summary = summary.strip()[:400] or chunk[:200].replace("\n", " ")
        hits.append({
            "type": "CANDIDATE",
            "id": cid,
            "snippet": summary,
            "file": "recursion-gate.md",
        })
    return hits


def build_index(user_dir: Path) -> dict:
    """Build full index for a user."""
    index = {"terms": {}, "hits": []}
    hits = []

    self_path = user_dir / "self.md"
    if self_path.exists():
        hits.extend(index_self(self_path))
    ev_path = user_dir / "self-evidence.md"
    if ev_path.exists():
        hits.extend(index_evidence(ev_path))
    pr_path = user_dir / "recursion-gate.md"
    hits.extend(index_pending(pr_path))

    for i, h in enumerate(hits):
        h["_idx"] = i
        text = " ".join(str(v) for v in h.values() if isinstance(v, str))
        for t in tokenize(text):
            if t not in index["terms"]:
                index["terms"][t] = []
            index["terms"][t].append(i)
    index["hits"] = hits
    return index


def query_index(index: dict, terms: str) -> list[dict]:
    """Return hits that contain any of the query terms."""
    tokens = tokenize(terms)
    if not tokens:
        return []
    matched_idx = set()
    for t in tokens:
        if t in index["terms"]:
            matched_idx.update(index["terms"][t])
    return [index["hits"][i] for i in sorted(matched_idx)]


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        return 1

    cmd = sys.argv[1].lower()
    user_id = DEFAULT_USER
    args = sys.argv[2:]
    if "-u" in args:
        i = args.index("-u")
        if i + 1 < len(args):
            user_id = args[i + 1]
            args = args[:i] + args[i + 2:]
    user_dir = REPO_ROOT / "users" / user_id
    if not user_dir.exists():
        print(f"User dir not found: {user_dir}", file=sys.stderr)
        return 1

    if cmd == "build":
        index = build_index(user_dir)
        out_path = user_dir / ".index_record.json"
        with open(out_path, "w") as f:
            json.dump(index, f, indent=0)
        print(f"Index built: {len(index['hits'])} hits, {len(index['terms'])} terms -> {out_path}")
        return 0

    if cmd == "query":
        idx_path = user_dir / ".index_record.json"
        if not idx_path.exists():
            print("Run 'build' first.", file=sys.stderr)
            return 1
        with open(idx_path) as f:
            index = json.load(f)
        q = " ".join(args) if args else ""
        results = query_index(index, q)
        for r in results:
            rid = r.get("id", r.get("value", ""))
            f = r.get("file", "")
            snip = (r.get("snippet", "") or "")[:120]
            print(f"  {rid} [{f}] {snip}...")
        print(f"\n{len(results)} matches for '{q}'")
        return 0

    print("Unknown command. Use 'build' or 'query'.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
