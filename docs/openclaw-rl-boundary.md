# OpenClaw-RL / RL data boundary (Grace-Mar)

This doc sets **what may and may not** flow into **reinforcement learning**, **fine-tuning**, or **shared training datasets** when you use tools such as [OpenClaw-RL](https://github.com/Gen-Verse/OpenClaw-RL) alongside Grace-Mar. It does **not** change the gated pipeline for **SELF / EVIDENCE / prompt** — only **optional downstream use** of exported logs.

---

## Principles

1. **Record ≠ training set** — Merged **SELF** is authoritative for the Voice. RL updates **model weights**; that is a **different** surface from **human-approved profile text**. Do not treat automatic trajectory export as consent to train on the child’s identity without explicit operator policy.

2. **Minors** — If the companion is a minor, assume **no** raw chat in third-party or pooled RL until a guardian-defined policy says otherwise. Prefer **operator-curated, redacted** snippets only.

3. **No secrets in trajectories** — Same as OpenClaw-RL’s README: never export API keys, tokens, passwords, or medical/legal identifiers into JSONL you might share or upload.

4. **Staging is not canonical** — **RECURSION-GATE** pending text can be wrong, duplicate, or analyst-inferred. Do not use pending candidates as **ground truth** for RL labels; **applied** merges are closer to “approved signal” only when operator intended that.

5. **Knowledge boundary** — Do not use RL to **inject** facts into the Record. Grace-Mar merges only through **RECURSION-GATE + approval**. RL may tune **style or tool use in harness**; it does not replace the gate.

---

## Green / yellow / red (rough guide)

| Zone | Examples | RL / export |
|------|----------|-------------|
| **Green** | Operator-approved anonymized tool traces; synthetic tasks; public system prompts you authored | OK for local experiments if policy allows |
| **Yellow** | `export_conversation_trajectories.py` output from **session-transcript** — use **last-n** slices, review before upload | Review + redact; prefer local self-hosted stack only |
| **Red** | Full child transcripts, medical/education identifiers, gate drafts with rejection reasons tied to real events, any content you would not email to a stranger | Do not pool; do not upload to public datasets |

---

## Script contract

- **`scripts/export_conversation_trajectories.py`** — **Read-only**; emits JSONL for **your** disks. It does **not** call training APIs. Operator decides destination and retention.
- Default output includes **turn, role, channel, text, ts** and optional **pipeline_events** near each turn (best-effort time window). Not a full OpenClaw-RL schema — adapt downstream if needed.

---

## Alignment with AGENTS

- **Gated pipeline** unchanged.
- **OpenClaw** may stage; may not merge.
- **RL** (if used) is **harness-level** unless you explicitly run a separate, guardian-approved process — never a back door into SELF.

---

## References

- [OpenClaw integration](openclaw-integration.md) — export + trajectory section
- [OpenClaw-RL](https://github.com/Gen-Verse/OpenClaw-RL) — upstream README (PII reminder, self-hosted stack)
- [AGENTS.md](../AGENTS.md) — knowledge boundary, permission boundaries
