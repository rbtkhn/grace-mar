#!/usr/bin/env python3
"""
Build a ChromaDB vector index from Record (SELF, SKILLS, EVIDENCE) for semantic lookup.

Run after merge or when Record changes: python scripts/index_record.py -u grace-mar
Requires OPENAI_API_KEY and chromadb. Index is stored under users/<id>/.chroma (gitignored).

This is **not** the Tier 1.3 keyword retriever used in chat grounding — that is
``bot.retriever.load_record_chunks`` / ``retrieve`` (lexical scoring, optional
``.cache/retriever_chunks.pkl``). Vector index and keyword index are independent.
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

def _load_chunks(user_id: str) -> list[tuple[str, str]]:
    """Load (chunk_id, text) from Record using retriever logic."""
    os.environ["GRACE_MAR_USER_ID"] = user_id
    from bot.retriever import load_record_chunks
    chunks = load_record_chunks()
    return [(c[0], c[1]) for c in chunks]


def build_index(user_id: str = "grace-mar", persist_path: Path | None = None) -> int:
    """Build or refresh Chroma collection. Returns number of chunks indexed."""
    try:
        import chromadb
        from chromadb.utils import embedding_functions
    except ImportError:
        print("Install chromadb: pip install chromadb", file=sys.stderr)
        return 0
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        print("OPENAI_API_KEY not set; cannot embed.", file=sys.stderr)
        return 0

    persist_path = persist_path or REPO_ROOT / "users" / user_id / ".chroma"
    persist_path.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(persist_path))
    ef = embedding_functions.OpenAIEmbeddingFunction(api_key=api_key, model_name="text-embedding-3-small")
    collection = client.get_or_create_collection("record", embedding_function=ef, metadata={"user_id": user_id})

    chunks = _load_chunks(user_id)
    if not chunks:
        print("No chunks from Record.", file=sys.stderr)
        return 0
    ids = [c[0] for c in chunks]
    documents = [c[1] for c in chunks]
    collection.upsert(ids=ids, documents=documents)
    print(f"Indexed {len(chunks)} chunks to {persist_path}", file=sys.stderr)
    return len(chunks)


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Build ChromaDB index from Record")
    ap.add_argument("-u", "--user", default="grace-mar")
    args = ap.parse_args()
    n = build_index(user_id=args.user)
    return 0 if n else 1


if __name__ == "__main__":
    sys.exit(main())
