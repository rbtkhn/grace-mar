# Bloom mastery and 2 Sigma — adaptation to companion-self / Grace-Mar

**Purpose:** Name **Benjamin Bloom’s mastery-learning frame** and the **2 Sigma** finding (strong tutoring lifts most learners well above group instruction) and map them onto this repo’s **gates, evidence, WORK compression, and containers** — without claiming school outcomes or adding automated mastery scores.

**Related lens:** [alpha-mastery-adaptation.md](alpha-mastery-adaptation.md) translates **Alpha School’s** operational mechanics (90% lesson gates, 2-hour block, Time Back) onto the same architecture. This doc stays **Bloom-first**; for Alpha-specific rows and benchmarks, use that file.

**Governed by:** Same boundary as the Alpha doc — design vocabulary and honest tooling descriptions, not verified performance data.

---

## What Bloom adds to the conversation

- **Mastery before advance** — Learners move on only after **demonstrated** understanding, so partial knowledge does not compound into “Swiss cheese.”
- **Formative use of evidence** — Ongoing checks and corrections, not only a final exam.
- **2 Sigma** — Bloom’s summary that **one-to-one mastery tutoring** (plus mastery pacing) produced effect sizes near two standard deviations vs conventional group instruction in his studies; later work debates replication and conditions. Here it is an **analogy**: the **Voice** and **operator tools** can play a tutoring-like role **grounded in the Record**, not unbounded model knowledge.

This codebase is **not** a learning management system. The analogy is **adult, self-directed, sovereign** practice on a **cognitive fork**.

---

## Map to companion-self / Grace-Mar

| Bloom idea | companion-self / Grace-Mar meaning | Where it lives |
|------------|-----------------------------------|----------------|
| Clear objectives | Founding intent + seed core facts (when present) | [`users/<id>/reflection-proposals/SEED-founding-intent.md`](../users/grace-mar/reflection-proposals/) (when present); `users/<id>/seed/minimal-core.json` per [seed-phase-wizard.md](seed-phase-wizard.md) — file may not exist until seed phase runs |
| Initial orientation | Good morning rhythm + daily intention | [scripts/good-morning-brief.py](../scripts/good-morning-brief.py); `reflection-proposals/DAILY-INTENTION-*.md` |
| Formative evidence | Activity log, staging, approved trail | [`self-evidence.md`](../users/grace-mar/self-evidence.md), [`recursion-gate.md`](../users/grace-mar/recursion-gate.md) ([identity-fork-protocol.md](identity-fork-protocol.md)), [`self-archive.md`](../users/grace-mar/self-archive.md) after merge — not a `self-evidence/` directory or a separate `Record/` tree |
| Corrective loop | Contradictions + sovereign gate + merge script | [contradiction-resolution.md](contradiction-resolution.md), [CONTRADICTION-ENGINE-SPEC.md](CONTRADICTION-ENGINE-SPEC.md), RECURSION-GATE, [scripts/process_approved_candidates.py](../scripts/process_approved_candidates.py); staging conflict checks in `bot/conflict_check.py` — **no** `gate-guardian.js` in this repo |
| ~90% “mastery before advance” | Compression / clarity bar before treating work as closed | [scripts/jiang-compress.py](../scripts/jiang-compress.py), [COMPRESSION-ENGINE.md](skill-work/work-jiang/COMPRESSION-ENGINE.md) — **operator checklist + JSON schema**, not an automated 90% scorer (see below) |
| 80–85% flow zone | Sprint/session difficulty “in the zone” (self-rated) | Optional [sprint-template.md](../research/external/work-jiang/sprints/sprint-template.md); see also [alpha-school-reference.md](skill-work/work-alpha-school/alpha-school-reference.md), [educational-software-history-insights.md](educational-software-history-insights.md) |
| Practice / articulation | THINK vs WRITE containers | [`users/<id>/skill-think.md`](../users/grace-mar/skill-think.md), [`users/<id>/skill-write.md`](../users/grace-mar/skill-write.md) ([canonical-paths.md](canonical-paths.md)) |
| Time back | Intention + memory horizons + WORK lanes | good-morning-brief, [memory-template.md](memory-template.md), WORK files under `users/<id>/` |
| Variation reduction | Layer boundaries and identity/library rules | [AGENTS.md](../AGENTS.md), [conceptual-framework.md](conceptual-framework.md), [scripts/identity_library_boundary_rules.py](../scripts/identity_library_boundary_rules.py) — **no** `layer-enforcer.py` or `truth-density-score.py` unless added later |
| 1:1 tutoring analog | Recursive Record + Voice (queried, bounded) | [conceptual-framework.md](conceptual-framework.md) (triadic cognition, pipeline) |

---

## What the tooling actually does (no fairy tales)

**`jiang-compress.py` today**

- Runs an **interactive operator checklist** (y/N). Failure exits the script; it does **not** compute a percentage or block saves automatically like an LMS.
- Reads optional **`seed/minimal-core.json`** and **founding intent** paths when they exist.
- Emits **compression JSON** under `research/external/work-jiang/compressions/` and can **print a RECURSION-GATE stub** for manual paste — it does **not** merge into `self.md` or `self-evidence.md`.

So the parallel to “90% before the next lesson” is **discipline**: structured prompts toward **one-sentence clarity, linkable evidence, and next actions** before building on an artifact — not a hidden autograder.

**RECURSION-GATE**

- The **companion-controlled** integration moment for the Record. Analysts and operators **stage**; only approved paths merge (see AGENTS.md and the process script).

---

## Future / not shipped (v1 doc only)

Not implemented as first-class artifacts in this pass:

- A repo-wide **`progress-unit-tracker.json`** or automated mastery index
- Auto-tuning **good-morning-brief** from numeric “scores”
- Mandatory **night reflection** hooks tied to Bloom bands

These can be revisited if the operator wants explicit schemas and scripts.

---

## Grace-Mar / operator notes

Living doc: tighten paths if instance layout changes; keep **template-only** names (`gate-guardian.js`, `layer-enforcer.py`, `truth-density-score.py`, fictional `Record/` trees) out of grace-mar prose unless explicitly labeled **future or external template**.
