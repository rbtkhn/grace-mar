# Unified export CLI (`scripts/export.py`)

**Purpose:** One entrypoint that **dispatches** to existing `scripts/export_*.py` modules via subprocess (v1). Does not reimplement fork loading.

**Default user (M1):** If the child invocation has no `-u` / `--user`, `export.py` injects `-u` using, in order: explicit `export.py -u`, then `GRACE_MAR_USER_ID`, then repo heuristic (`grace-mar` when `users/grace-mar` exists, else `_template`).

**Forwarding (M2):** Use `--` to pass flags to the target script verbatim:

```bash
python3 scripts/export.py fork -- -o fork-export.json
python3 scripts/export.py fork -- --format json-ld -o out.jsonld
```

Omitting `--` still forwards any tokens after the subcommand (e.g. `export.py fork -o out.json`).

**G1 — `all`:** Same as `bundle` (forwards to `export_runtime_bundle.py`).

**Non-goals:** `export_view`, `export_gate_to_review_queue`, … — run those scripts directly.

**Template repo:** [companion-self](../companion-self/) may not yet ship every `export_*.py`; `export.py` errors clearly if a target script is missing. Promote scripts from the instance repo per [MERGING-FROM-COMPANION-SELF.md](MERGING-FROM-COMPANION-SELF.md).

**Migration:**

| Before | After |
|--------|--------|
| `python scripts/export_fork.py -u grace-mar -o x.json` | `python scripts/export.py fork -- -u grace-mar -o x.json` |
| `python scripts/export_prp.py -u grace-mar` | `python scripts/export.py prp --` (or add `-o` after `--`) |
| `python scripts/export_runtime_bundle.py -u grace-mar` | `python scripts/export.py bundle --` or `python scripts/export.py all --` |
| `python scripts/export_emulation_bundle.py -u grace-mar` | `python scripts/export.py emulation --` |

Legacy scripts remain; they may emit `DeprecationWarning` when run as `__main__`.
