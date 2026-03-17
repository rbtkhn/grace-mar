#!/usr/bin/env python3
"""
Query the Record using the ChromaDB semantic index.

Usage:
    python scripts/semantic_query.py -u grace-mar "What does Grace-Mar know about Mars?"
    python scripts/semantic_query.py -u grace-mar --top 5 "favorite animals"

Returns top-k chunk IDs and snippets. Requires index_record.py to have been run.
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))


def query(
    user_id: str = "grace-mar",
    query_text: str = "",
    top_k: int = 5,
    persist_path: Path | None = None,
) -> list[dict]:
    """Return list of {id, document, distance} for the query."""
    try:
        import chromadb
        from chromadb.utils import embedding_functions
    except ImportError:
        return []
    persist_path = persist_path or REPO_ROOT / "users" / user_id / ".chroma"
    if not persist_path.exists():
        return []
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return []
    client = chromadb.PersistentClient(path=str(persist_path))
    ef = embedding_functions.OpenAIEmbeddingFunction(api_key=api_key, model_name="text-embedding-3-small")
    try:
        collection = client.get_collection("record", embedding_function=ef)
    except Exception:
        return []
    results = collection.query(query_texts=[query_text], n_results=min(top_k, 20))
    out = []
    if results and results["ids"] and results["ids"][0]:
        for i, id_ in enumerate(results["ids"][0]):
            doc = (results["documents"][0][i] if results.get("documents") else "") or ""
            dist = (results["distances"][0][i] if results.get("distances") else 0) or 0
            out.append({"id": id_, "document": doc, "distance": dist})
    return out


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Semantic query over Record index")
    ap.add_argument("-u", "--user", default="grace-mar")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("query", nargs="*")
    args = ap.parse_args()
    q = " ".join(args.query).strip()
    if not q:
        print("Usage: semantic_query.py [--top N] 'query text'", file=sys.stderr)
        return 1
    results = query(user_id=args.user, query_text=q, top_k=args.top)
    for r in results:
        print(f"  {r['id']}\t{r['document'][:120]}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
