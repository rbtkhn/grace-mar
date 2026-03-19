# Exploration: AutoGen-style internal deliberation (Path 1)

**Status:** Experimental. Not part of the core pipeline. Do not integrate into `bot/` or `scripts/process_approved_candidates.py` without explicit design approval.

**Purpose:** Minimal prototype for an internal deliberation loop: read-only ingest of Record + recent recursion-gate candidates; output is **draft only** for operator review. No merge path. No writes to Record or gate.

**Design doc:** [docs/exploration-multi-agent-deliberation.md](../../docs/exploration-multi-agent-deliberation.md)  
**Assessment:** [docs/feedback-autogen-exploration-2026-03-assessment.md](../../docs/feedback-autogen-exploration-2026-03-assessment.md)

---

## Invariants (must preserve)

- **No write to Record.** This script never writes to `self.md`, `self-evidence.md`, `bot/prompt.py`, or calls `process_approved_candidates.py`. Output goes only to `output/` (non-canonical).
- **Staging only after human review.** Deliberation output is a draft. If the operator wants to stage any of it, they do so manually (or via existing pipeline tooling); this script does not append to `recursion-gate.md`.
- **Optional dependency.** AutoGen is optional. If not installed, the script runs a dry run (loads context, writes a placeholder draft) so the repo does not depend on AutoGen.

---

## Usage

From repo root:

```bash
# With optional AutoGen (pip install pyautogen or autogen)
python exploration/autogen-deliberation/run_deliberation.py -u grace-mar

# Dry run (no AutoGen): loads self + gate snippet, writes placeholder draft
python exploration/autogen-deliberation/run_deliberation.py -u grace-mar --dry-run
```

Output is written to `exploration/autogen-deliberation/output/deliberation-draft-YYYYMMDD.md`. Review the draft; if you want to stage any part as a candidate, use the normal pipeline (manual edit of `recursion-gate.md` or existing staging flow).

---

## Output directory

`output/` holds draft files only. These are **not** canonical Record or gate artifacts. Do not commit sensitive content if the repo is shared; add `output/*.md` to `.gitignore` if desired.
