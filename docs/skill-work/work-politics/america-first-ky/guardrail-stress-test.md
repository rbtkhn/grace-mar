# Guardrail stress-test framework — America First Kentucky (WORK)

## Purpose

Reduce predictable failure modes when drafting **high-stakes** america-first-ky outputs (war powers, insider-trading / ethics, cartel-economy claims, border + civil liberties). Methodology is **inspired by** independent evaluation of clinical AI systems — factorial vignettes, reasoning-vs-action mismatch, anchoring, and miscalibrated alerts — not a claim of medical or clinical use.

**Inspired-by (verify externally):** Icahn School of Medicine at Mount Sinai et al., *ChatGPT Health* structured triage evaluation, **Nature Medicine** (2026). Example institutional summary: [Mount Sinai newsroom](https://www.mountsinai.org/about/newsroom/2026/research-identifies-blind-spots-in-ai-medical-triage). Paper: [Nature Medicine article](https://www.nature.com/articles/s41591-026-04297-7).

This repo **does not** implement clinical triage. We **borrow** the *epistemic* lessons: tail-risk silence, reasoning that does not match the final recommendation, social anchoring, and alerts that track tone instead of risk.

## Scope

| In scope | Out of scope |
|----------|----------------|
| WAP briefs, X draft packages, opposition memos labeled high-stakes | Automated merge into SELF / EVIDENCE |
| Operator- and SMM-enforced checklists | `governance_checker.py` enforcement |
| WORK logs, brief appendices, `content-queue` notes | Routine full traces appended to `self-evidence.md` |
| Optional pipeline events (`stress_test_proposed`, etc.) via `emit_pipeline_event.py` | Fabricated Python hooks in `governance_checker.py` |

## Four failure modes (mandatory human checks)

1. **Inverted U / tail risk** — Strong on routine framing; **silent or weak** on rare but consequential scenarios (e.g. sudden energy-market shock + war powers vote).
2. **Model “knows” but output diverges** — Internal reasoning (or scratch notes) flags a constitutional or ethics issue, but the **published** recommendation softens or contradicts it.
3. **Social context hijacks judgment** — Anchoring from “donor says it’s fine,” poll toplines, or authority cues shifts the conclusion without new evidence.
4. **Guardrails on vibes** — Red-team or internal “blocks” trigger on emotional tone instead of **material** constitutional or corruption risk.

## Factorial stress testing (operator method)

For **each** high-stakes base scenario, the operator (or agent under operator sign-off) documents **controlled variations** on the same factual spine. Mount Sinai-style designs used **multiple factorial conditions** on the same vignettes; we mirror that **logically**, not as a medical test.

**Typical variation knobs (pick those that apply):**

- + Social pressure (“donor / colleague says it’s fine”)
- + Contradictory or noisy poll framing
- + Time pressure (“vote in 48 hours”)
- + Tail-risk injection (e.g. sudden chokepoint / price shock relevant to the scenario)

**Minimum:** 4 variations for a high-stakes brief; **stretch:** 8–16 documented rows in an appendix table.

**Pass criterion:** For each variation, the **stated recommendation** must be **consistent** with the **same risk notes** (no silent downgrade). Any mismatch → **do not ship**; escalate to operator approval inbox; optionally emit `stress_test_failed` (see below).

## Four layers (process — not code)

These are **discipline layers** for humans and drafting agents. They are **not** wired into `governance_checker.py`.

| Layer | Meaning |
|-------|---------|
| **1. Progressive autonomy** | On tail scenarios, default to **shadow / draft-only** until operator explicitly approves ship. |
| **2. Deterministic validation** | Operator checklist: “Does the final paragraph contradict any explicit risk bullet above?” |
| **3. False-positive flywheel** | Prefer **over-flagging** tail risk in internal drafts; then **prune** with evidence before publish. |
| **4. Factorial pass** | Run the variation table before finalizing any Massie pilot **high-stakes** brief. |

## Logging

- **Primary:** WORK artifact — stress-test appendix on the same brief file or linked `stress-test-brief-YYYY-MM-DD.md` under this folder or `work-politics/` weekly brief directory.
- **Do not** routinely dump full reasoning traces into `self-evidence.md`. Optional **ACT-** line only if companion approves a gated candidate that records “we ran stress-test protocol for brief X.”

## Reasoning–output alignment

- **No automated “alignment score”** in this repo unless separately specified and stored in WORK.
- Human rule: if scratch reasoning contains “constitutional concern” / “insider risk” / “unsourced claim,” the **shipped** text must **acknowledge** the same tier of concern or **remove** the risky claim.

## Suggested pipeline events (optional)

`scripts/emit_pipeline_event.py` accepts arbitrary `event_type` strings. Suggested names for audit (operator-run):

- `stress_test_proposed` — candidate id `none` or brief slug in extras
- `stress_test_passed` / `stress_test_failed`
- `guardrail_mismatch_detected`

Example (adjust user id if needed):

```bash
python scripts/emit_pipeline_event.py stress_test_passed none brief=weekly-2026-03-20 territory=wap
```

## When to run

**Always** before final human sign-off on:

- War powers / use-of-force briefs
- Congressional ethics / stock-trading messaging
- “Cartel economy” claims that imply specific actors or legal conclusions
- Border + civil-liberty combined messaging in volatile news windows

**Optional** for low-stakes engagement posts.

## Related

- [stress-test-brief-template.md](stress-test-brief-template.md)
- [analytical-lenses/manifest.md](../analytical-lenses/manifest.md) — triangulation; stress-test is **additional** to lenses, not a replacement
- [AGENT-SESSION-BRIEF.md](AGENT-SESSION-BRIEF.md) — next-session implementation tasks
