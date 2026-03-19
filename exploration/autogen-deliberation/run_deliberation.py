#!/usr/bin/env python3
"""
Exploration: internal deliberation loop (Path 1). Read-only ingest of Record +
recent recursion-gate candidates; output is DRAFT only. No merge. No writes to
Record or gate. Optional AutoGen; dry-run works without it.

Usage:
  python exploration/autogen-deliberation/run_deliberation.py -u grace-mar
  python exploration/autogen-deliberation/run_deliberation.py -u grace-mar --dry-run

Output: exploration/autogen-deliberation/output/deliberation-draft-YYYYMMDD.md
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path


def _repo_root() -> Path:
    """Resolve repo root (parent of exploration/)."""
    script_dir = Path(__file__).resolve().parent
    # exploration/autogen-deliberation/ -> repo root is script_dir.parent.parent
    return script_dir.parent.parent


def _load_self(repo_root: Path, user_id: str) -> str:
    """Load self.md for the user (read-only)."""
    path = repo_root / "users" / user_id / "self.md"
    if not path.exists():
        return f"(self.md not found: {path})"
    return path.read_text(encoding="utf-8", errors="replace")


def _load_gate_snippet(repo_root: Path, user_id: str, max_chars: int = 8000) -> str:
    """Load a snippet of recursion-gate.md (read-only)."""
    path = repo_root / "users" / user_id / "recursion-gate.md"
    if not path.exists():
        return "(recursion-gate.md not found)"
    text = path.read_text(encoding="utf-8", errors="replace")
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n... (truncated)\n"
    return text


def _write_draft(content: str, out_dir: Path) -> Path:
    """Write draft to output/deliberation-draft-YYYYMMDD.md. Creates out_dir if needed."""
    out_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    out_path = out_dir / f"deliberation-draft-{date_str}.md"
    out_path.write_text(content, encoding="utf-8")
    return out_path


def run_dry_run(repo_root: Path, user_id: str, out_dir: Path) -> Path:
    """Load context and write a placeholder draft (no AutoGen)."""
    self_content = _load_self(repo_root, user_id)
    gate_snippet = _load_gate_snippet(repo_root, user_id)

    draft = f"""# Deliberation draft (dry run) — {datetime.now().isoformat(timespec='minutes')}

**Status:** Draft only. Not a candidate. Not staged. Review and, if desired, stage manually via existing pipeline.

**Invariant:** This file is non-canonical. Nothing here enters the Record without companion approval and merge via `process_approved_candidates.py`.

---

## Loaded context (read-only)

### self.md (excerpt)

```markdown
{self_content[:6000]}{"..." if len(self_content) > 6000 else ""}
```

### recursion-gate.md (excerpt)

```markdown
{gate_snippet[:4000]}{"..." if len(gate_snippet) > 4000 else ""}
```

---

## Deliberation (placeholder)

With AutoGen installed and without `--dry-run`, a small GroupChat (Guardian, Validator, Explorer, Writer) would deliberate over the above context and produce proposed refinements or candidate suggestions here. Output would remain draft; staging would be a separate, human-reviewed step.

To run with AutoGen: install `pyautogen` (or `autogen`) and run without `--dry-run`. See README in this directory.
"""

    return _write_draft(draft, out_dir)


def run_with_autogen(repo_root: Path, user_id: str, out_dir: Path) -> Path:
    """Run a minimal AutoGen deliberation and write draft. Optional dependency."""
    try:
        import autogen
    except ImportError:
        return run_dry_run(
            repo_root, user_id, out_dir
        )  # fallback: same as dry run

    self_content = _load_self(repo_root, user_id)
    gate_snippet = _load_gate_snippet(repo_root, user_id)
    context = f"## SELF (excerpt)\n\n{self_content[:5000]}\n\n## Recursion-gate (excerpt)\n\n{gate_snippet[:3000]}"

    # Minimal config: one assistant that produces a short deliberation note.
    # Expand to GroupChat (Guardian, Validator, Explorer, Writer) when needed.
    config_list = []
    if hasattr(autogen, "config_list_from_dotenv") or hasattr(autogen, "config_list_from_json"):
        try:
            if hasattr(autogen, "config_list_from_dotenv"):
                config_list = autogen.config_list_from_dotenv()
            elif hasattr(autogen, "config_list_from_json"):
                config_list = autogen.config_list_from_json("OAI_CONFIG_LIST")
        except Exception:
            pass
    if not config_list:
        # No LLM config: write placeholder and return
        return run_dry_run(repo_root, user_id, out_dir)

    # Stub: real implementation would instantiate ConversableAgent(s) and GroupChat.
    # We do not add AutoGen API details here to keep the script runnable without
    # a specific AutoGen version. Output remains draft-only.
    draft = f"""# Deliberation draft — {datetime.now().isoformat(timespec='minutes')}

**Status:** Draft only. Not a candidate. Not staged.

**Context loaded:** self.md + recursion-gate snippet (read-only).

---

## Context used

{context[:8000]}

---

## Deliberation output (stub)

AutoGen is available. A full implementation would run a GroupChat (Guardian, Validator, Explorer, Writer) and append the conversation or summary here. This stub avoids hard-coding a specific AutoGen API. To implement: add agent creation and group chat execution; write their final message or summary to this section. Output must never be written to Record or recursion-gate by this script.
"""

    return _write_draft(draft, out_dir)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exploration: deliberation draft from Record + gate (read-only; output is draft only)."
    )
    parser.add_argument("-u", "--user", default="grace-mar", help="User id (default: grace-mar)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not use AutoGen; load context and write placeholder draft only.",
    )
    args = parser.parse_args()

    repo_root = _repo_root()
    out_dir = repo_root / "exploration" / "autogen-deliberation" / "output"

    if args.dry_run:
        path = run_dry_run(repo_root, args.user, out_dir)
    else:
        path = run_with_autogen(repo_root, args.user, out_dir)

    print(f"Wrote draft (non-canonical): {path}")
    print("Review the draft; stage only via existing pipeline after human review.")


if __name__ == "__main__":
    main()
