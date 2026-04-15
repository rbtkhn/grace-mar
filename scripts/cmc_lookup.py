#!/usr/bin/env python3
"""
CLI wrapper for CMC lookup with --civilization filter and JSON output.

Thin layer over bot.lookup_cmc — adds civilization filtering,
structured JSON output, and standalone CLI usage for operator
work-strategy sessions.

Usage:
    python3 scripts/cmc_lookup.py "What did Rome use aqueducts for?"
    python3 scripts/cmc_lookup.py "Byzantine continuity" --civilization byzantine
    python3 scripts/cmc_lookup.py "Hormuz chokepoint" --json --top-k 3
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from bot.lookup_cmc import (
    _get_cmc_path,
    _index_exists,
    _query_inrepo_civmem,
    _safe_query,
    should_route_to_cmc,
)


def cmc_search(
    query: str,
    top_k: int = 5,
    civilization: str | None = None,
    skip_routing: bool = False,
) -> dict:
    """Structured CMC search with optional civilization filter."""
    if not skip_routing and not should_route_to_cmc(query):
        return {"status": "skipped", "reason": "outside CMC scope", "query": query}

    cmc_root = _get_cmc_path()
    use_external = cmc_root and _index_exists(cmc_root)

    if not use_external:
        inrepo = _query_inrepo_civmem(query, limit=top_k)
        if inrepo:
            return {
                "status": "success",
                "source": "inrepo",
                "query": query,
                "raw_output": inrepo,
                "parsed_results": _parse_raw(inrepo),
                "sources": [],
            }
        return {
            "status": "miss",
            "reason": "CMC not available or no matches",
            "query": query,
        }

    script = cmc_root / "tools" / "cmc-index-search.py"
    if not script.is_file():
        return {"status": "error", "message": f"cmc-index-search.py not found at {script}"}

    safe_q = _safe_query(query)
    if not safe_q:
        return {"status": "error", "message": "query reduced to empty after sanitization"}

    cmd = ["python3", str(script), "query", safe_q, "--limit", str(top_k)]
    if civilization:
        cmd.extend(["--civilization", civilization])

    try:
        result = subprocess.run(
            cmd, cwd=str(cmc_root), capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            return {"status": "error", "message": result.stderr.strip()[:500]}

        raw = result.stdout.strip()
        if not raw or "No matches" in raw:
            return {"status": "miss", "reason": "no matches", "query": query}

        parsed = _parse_indexed_output(raw)
        return {
            "status": "success",
            "source": "external",
            "query": query,
            "civilization_filter": civilization,
            "raw_output": raw,
            "parsed_results": parsed,
            "sources": [r["path"] for r in parsed if r.get("path")],
        }
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "CMC query timeout (15s)"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def _parse_raw(text: str) -> list[dict]:
    """Parse in-repo snippet text into result dicts."""
    results = []
    for i, chunk in enumerate(text.split("\n\n")):
        chunk = chunk.strip()
        if chunk:
            results.append({"index": i, "snippet": chunk})
    return results


def _parse_indexed_output(raw: str) -> list[dict]:
    """Parse cmc-index-search.py output blocks into structured dicts."""
    results = []
    for block in re.split(r"\n(?=\d+\.\s)", raw):
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        entry: dict = {}
        if lines:
            path_match = re.match(r"\d+\.\s+(.+)", lines[0])
            if path_match:
                entry["path"] = path_match.group(1).strip()
        if len(lines) >= 2:
            entry["title"] = lines[1].strip()
        if len(lines) >= 3:
            entry["snippet"] = lines[2].strip()
        if entry:
            results.append(entry)
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="CMC lookup CLI")
    ap.add_argument("query", help="Search query")
    ap.add_argument("--top-k", type=int, default=5, help="Max results (default: 5)")
    ap.add_argument("--civilization", help="Filter by civilization (e.g. rome, china)")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--skip-routing", action="store_true", help="Bypass scope check")
    args = ap.parse_args()

    result = cmc_search(
        args.query,
        top_k=args.top_k,
        civilization=args.civilization,
        skip_routing=args.skip_routing,
    )

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        status = result["status"]
        print(f"Status: {status}")
        if status == "success":
            print(f"Source: {result.get('source', '?')}")
            if result.get("civilization_filter"):
                print(f"Filter: {result['civilization_filter']}")
            print(f"Results: {len(result.get('parsed_results', []))}")
            print()
            for r in result.get("parsed_results", []):
                if r.get("path"):
                    print(f"  {r['path']}")
                if r.get("title"):
                    print(f"    {r['title']}")
                if r.get("snippet"):
                    print(f"    {r['snippet'][:200]}")
                print()
        elif status == "skipped":
            print(f"Reason: {result.get('reason', '')}")
        elif status == "miss":
            print(f"Reason: {result.get('reason', '')}")
        else:
            print(f"Error: {result.get('message', '')}")

    return 0 if result["status"] in ("success", "skipped", "miss") else 1


if __name__ == "__main__":
    sys.exit(main())
