#!/usr/bin/env python3
"""Advisory check: implemented capabilities should have proof ledger coverage.

Exits 0 with warnings, or 1 if --strict and a implemented item lacks proof id reference.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    cap_path = REPO_ROOT / "artifacts/work-dev/capability-status.json"
    proof_path = REPO_ROOT / "artifacts/work-dev/proof_ledger.json"
    caps = json.loads(cap_path.read_text(encoding="utf-8"))
    proof = json.loads(proof_path.read_text(encoding="utf-8"))
    contexts = {e.get("context") for e in proof.get("entries", [])}

    issues: list[str] = []
    for item in caps.get("items", []):
        if item.get("status") != "implemented":
            continue
        iid = item.get("id")
        if iid not in contexts:
            issues.append(
                f"implemented capability {iid!r} has no proof_ledger entry with context={iid!r} (advisory)"
            )

    for msg in issues:
        print(msg, file=sys.stderr)
    if args.strict and issues:
        return 1
    print("ok: verify_work_dev_claims (advisory unless --strict)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
