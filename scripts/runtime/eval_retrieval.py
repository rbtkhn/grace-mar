#!/usr/bin/env python3
"""
Evaluate hybrid retrieval quality against a golden-set JSONL.

Each golden-set line: {"query", "surface", "expected_path", "note"}
For each query, runs retrieve() and checks whether expected_path
appears in the top-k results. Reports precision@k and MRR.

Usage:
  python3 scripts/runtime/eval_retrieval.py
  python3 scripts/runtime/eval_retrieval.py --golden tests/fixtures/retrieval-golden.jsonl --top-k 5 --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_RUNTIME_DIR = Path(__file__).resolve().parent
_SCRIPTS_DIR = _RUNTIME_DIR.parent
REPO_ROOT = _RUNTIME_DIR.parent.parent

for _p in (_RUNTIME_DIR, _SCRIPTS_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from hybrid_retrieve import retrieve  # noqa: E402

DEFAULT_GOLDEN = REPO_ROOT / "tests" / "fixtures" / "retrieval-golden.jsonl"


def load_golden(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    entries = []
    for line in path.read_text(encoding="utf-8").strip().splitlines():
        line = line.strip()
        if not line:
            continue
        entries.append(json.loads(line))
    return entries


def evaluate(
    golden: list[dict],
    top_k: int = 5,
) -> dict:
    total = len(golden)
    hits_at_k = 0
    reciprocal_ranks: list[float] = []
    per_query: list[dict] = []

    for entry in golden:
        query = entry["query"]
        surface = entry["surface"]
        expected = entry["expected_path"]

        try:
            results = retrieve(surface, query, top_k=top_k)
        except (ValueError, Exception) as e:
            per_query.append({
                "query": query,
                "expected": expected,
                "hit": False,
                "rank": None,
                "error": str(e),
            })
            reciprocal_ranks.append(0.0)
            continue

        result_paths = [r.path for r in results]
        rank = None
        for i, rp in enumerate(result_paths):
            if expected in rp or rp in expected:
                rank = i + 1
                break

        hit = rank is not None and rank <= top_k
        if hit:
            hits_at_k += 1
            reciprocal_ranks.append(1.0 / rank)
        else:
            reciprocal_ranks.append(0.0)

        per_query.append({
            "query": query,
            "expected": expected,
            "hit": hit,
            "rank": rank,
            "returned_count": len(results),
            "top_paths": result_paths[:3],
        })

    precision_at_k = hits_at_k / total if total > 0 else 0.0
    mrr = sum(reciprocal_ranks) / total if total > 0 else 0.0

    return {
        "top_k": top_k,
        "total_queries": total,
        "hits_at_k": hits_at_k,
        "precision_at_k": round(precision_at_k, 4),
        "mrr": round(mrr, 4),
        "per_query": per_query,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Evaluate hybrid retrieval against golden set.")
    ap.add_argument("--golden", type=Path, default=DEFAULT_GOLDEN, help="Path to golden-set JSONL")
    ap.add_argument("--top-k", type=int, default=5, help="Top-k for retrieval (default: 5)")
    ap.add_argument("--json", action="store_true", default=False, help="Output JSON instead of summary")
    args = ap.parse_args()

    golden = load_golden(args.golden)
    if not golden:
        print("No golden-set entries found.", file=sys.stderr)
        return 1

    result = evaluate(golden, top_k=args.top_k)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Retrieval Evaluation (top_k={result['top_k']})")
        print(f"  Queries:      {result['total_queries']}")
        print(f"  Hits@{result['top_k']}:      {result['hits_at_k']}")
        print(f"  Precision@{result['top_k']}: {result['precision_at_k']:.2%}")
        print(f"  MRR:          {result['mrr']:.4f}")
        print()
        misses = [q for q in result["per_query"] if not q["hit"]]
        if misses:
            print(f"  Misses ({len(misses)}):")
            for m in misses:
                print(f"    - {m['query'][:60]}... → expected: {m['expected']}")
                if m.get("top_paths"):
                    print(f"      got: {m['top_paths'][:2]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
