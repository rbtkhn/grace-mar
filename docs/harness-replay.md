# Harness event replay

**North star (full causal debugger):** See [harness-replay-spec.md](harness-replay-spec.md) — three modes (answer / proposal / merge), future event envelope, UI shape, and pairing with the [boundary review queue](boundary-review-queue.md).

**Purpose (this CLI):** Reconstruct **audit-lane** context for a **staged proposal** (candidate) or **bundle** export—**not** a full neural “why did the model say X” trace unless that was logged elsewhere.

Grace-Mar separates **record**, **runtime**, **audit**, and **policy** ([harness-inventory.md](harness-inventory.md)). Replay pulls from the **audit** lane:

| Source | What it explains |
|--------|------------------|
| `pipeline-events.jsonl` | staged / applied / rejected and extras |
| `harness-events.jsonl` | merge_applied, exports, bundle ids |
| `merge-receipts.jsonl` | merge batch, approver, checksum snapshot |
| `recursion-gate.md` | Current **or** **Processed** candidate YAML (if still in file) |
| `self-evidence.md` | ACT line if `--evidence` given |

**Limitations**

- **Voice answers:** Full SYSTEM prompt + retrieval trace per message is **not** stored in harness-events by default. Use **session-transcript** tail (`--transcript-snippet`) only as a **hint**—it may be redacted or huge.
- **Processed candidates** removed from `recursion-gate.md` leave only **pipeline + harness + merge-receipts**; git history may still have the block.
- **Trust:** Replay shows **what was recorded**, not cryptographic proof of model internals.

---

## Usage

```bash
python scripts/replay_harness_event.py -u grace-mar --candidate CANDIDATE-0089
python scripts/replay_harness_event.py -u grace-mar --bundle-id 5229e838372b
python scripts/replay_harness_event.py -u grace-mar --candidate CANDIDATE-0085 --evidence ACT-0024 --transcript-snippet
```

Output is **markdown** to stdout; redirect to a file for tickets.

---

## Related

- [harness-replay-spec.md](harness-replay-spec.md) — product spec and roadmap
- [harness-inventory.md](harness-inventory.md) — audit stream vocabulary
- [operator-weekly-review.md](operator-weekly-review.md) — gate rhythm
