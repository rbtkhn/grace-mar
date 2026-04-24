# Candidate comparison protocol (Workbench)

**Purpose:** Compare **two or more** generated **artifacts** (A/B, **round 2** vs **round 1**) before picking a default branch, PR direction, or follow-on prompt. This is **operator judgment**; there is no automatic “winner” merge.

**Not** a substitute for: [harness replay](../../../harness-replay.md) (in-repo path: `docs/harness-replay.md`), gate queue ordering, or CI — unless you add separate tooling. **Not** a merge path.

**Maps to:** One [workbench receipt](WORKBENCH-RECEIPT-SPEC.md) per **candidate** (same `workbenchRunId` and a shared label in `revisionSummary` or a companion markdown table, if you need grouping).

## Comparison table (copy into WORK notes or a scratch doc)

| Column | What to write |
|--------|----------------|
| **Candidate** | `artifactCandidateLabel` (e.g. `A`, `B`) — **not** a gate `CANDIDATE-nnnn` unless you also set `relatedGateCandidateId` |
| **Path** | Repo-root-relative path to the artifact root or main entry (same idea as `pathsTouched[0]`) |
| **Launch status** | Did `launchCommand` work on first try? (ok / required fix / n/a) |
| **Visual status** | Per [VISUAL-INSPECTION-PROTOCOL.md](VISUAL-INSPECTION-PROTOCOL.md) — pass / fail / skipped |
| **Test status** | Unit/smoke/CLI: pass / fail / not run (tests prove **code behavior**, not world truth) |
| **Strengths** | Short bullet list (operator view) |
| **Weaknesses** | Short bullet list (operator view) |
| **Recommendation** | e.g. “Merge B with one fix,” “Abandon A,” “needs design review” — **human** only |
| **Safe next action** | One step: e.g. “File PR for B only,” “Re-prompt on layout only,” “Do not commit — spike” |

## Procedure

1. **Freeze inputs** — same machine, same dependency install command (or document differences).
2. **Run each candidate** — separate workbench receipt per candidate (or one receipt with a clear multi-candidate table only if you extend the spec later; v0.1 prefers **one receipt per run** with distinct `receiptId`).
3. **Fill the table** — do not copy LLM adjectives without your own one-line in **Strengths/Weaknesses**.
4. **Record recommendation** — must be a **human** or explicitly attributed operator call; not “model says ship.”
5. **Safe next action** — must **not** imply gate approval. If the next action is a gate candidate, say “draft candidate for recursion-gate” — still **staged by normal tools**, not by workbench.

## If candidates tie

- Use **inconclusive** in `status` and either gather more data (e.g. another screenshot, perf trace) or escalate to a **design** decision in WORK, not Record.

## Truth scope

- This comparison ranks **local artifact behavior and maintainability in context**. It does not rank **factual** correctness of content shown inside a dashboard unless you add a separate, explicit verification process (e.g. [fact-check](../../../.cursor/skills/fact-check/SKILL.md) with cites — **out of scope** for this protocol).
