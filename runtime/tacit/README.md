# Runtime tacit capture

**Non-canonical.** Markdown-first intake for lived observations, normalized to JSON for candidate generation. **Not** SELF, SELF-LIBRARY, SKILLS, or EVIDENCE. **Does not** write `recursion-gate.md` or merge into the Record.

**Doctrine:** [docs/tacit-capture/README.md](../../docs/tacit-capture/README.md)

## Layout

| Path | Role |
|------|------|
| `inbox/` | Drop raw `.md` tacit captures (operator-local when gitignored). |
| `normalized/` | Deterministic JSON output from `scripts/tacit/normalize_tacit_capture.py`. |
| `candidates/` | JSON from `scripts/tacit/generate_tacit_candidates.py` (review-only). |
| `index.jsonl` | One JSON object per line: `{id, provenance_path, content_sha256, timestamp}` (operator-local when gitignored). |

## Commands

```bash
python3 scripts/tacit/normalize_tacit_capture.py --input runtime/tacit/inbox/note.md --repo-root . --append-index
python3 scripts/tacit/generate_tacit_candidates.py --normalized runtime/tacit/normalized/<id>.json --output-dir runtime/tacit/candidates
```

See [docs/tacit-capture/README.md](../../docs/tacit-capture/README.md) for intake format and governance boundaries.
