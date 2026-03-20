#!/usr/bin/env python3
"""
Validate docs/self-library-domains.json: required fields, unique ids, required routable domains, routing_docs exist.

See docs/self-library-domains.md. Used by validate-integrity.py.

  python3 scripts/validate_library_domain_registry.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Every id listed here must appear in registry with full metadata. Extend when
# new auto-routed library domains are added to bot/lookup_* or core lookup order.
REQUIRED_ROUTABLE_DOMAIN_IDS = frozenset({"civ_mem"})

REQUIRED_KEYS = (
    "id",
    "name",
    "what",
    "surface",
    "authority",
    "invocation",
    "mutation_policy",
    "freshness",
    "owner",
)


def validate_library_domain_registry(repo_root: Path) -> list[str]:
    errors: list[str] = []
    path = repo_root / "docs" / "self-library-domains.json"
    if not path.is_file():
        return [f"Missing {path.relative_to(repo_root)}"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"self-library-domains.json: invalid JSON: {e}"]
    domains = data.get("domains")
    if not isinstance(domains, list) or len(domains) == 0:
        return ["self-library-domains.json: domains must be a non-empty array"]

    ids_seen: set[str] = set()
    for d in domains:
        if not isinstance(d, dict):
            errors.append("self-library-domains.json: each domain must be an object")
            continue
        for k in REQUIRED_KEYS:
            if k not in d:
                errors.append(f"domain {d.get('id', '?')!r}: missing required key {k!r}")
        did = d.get("id")
        if isinstance(did, str):
            if did in ids_seen:
                errors.append(f"duplicate domain id: {did}")
            ids_seen.add(did)
        fw = d.get("freshness")
        if isinstance(fw, dict):
            if not any(k in fw for k in ("last_refresh", "staleness", "evidence_coverage")):
                errors.append(
                    f"domain {d.get('id', '?')!r}: freshness should include "
                    "at least one of last_refresh, staleness, evidence_coverage"
                )
        elif d.get("id"):
            errors.append(f"domain {d.get('id')!r}: freshness must be an object")

        for doc in d.get("routing_docs") or []:
            if not isinstance(doc, str):
                continue
            rel = repo_root / doc
            if not rel.is_file():
                errors.append(f"domain {d.get('id', '?')!r}: routing_doc not found: {doc}")

    for rid in REQUIRED_ROUTABLE_DOMAIN_IDS:
        if rid not in ids_seen:
            errors.append(
                f"Required routable domain id missing from registry: {rid!r} "
                f"(declare in self-library-domains.json; see docs/self-library-domains.md)"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Library Domain Registry JSON.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (default: parent of scripts/)",
    )
    args = parser.parse_args()
    err = validate_library_domain_registry(args.repo_root.resolve())
    if err:
        print("Library Domain Registry validation FAILED:", file=sys.stderr)
        for e in err:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("Library Domain Registry: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
