# work-strategy — transcript ingest (operator)

**Purpose:** Hold **raw or lightly curated transcripts** that feed the **work-strategy** pipeline ([current-events-analysis.md](../../../../docs/skill-work/work-strategy/current-events-analysis.md) step 1 **Perceiver**, [persuasive-content-pipeline.md](../../../../docs/skill-work/work-strategy/persuasive-content-pipeline.md), [LEARN_MODE_RULES.md](../../../../docs/skill-work/work-strategy/LEARN_MODE_RULES.md)), **separate from** the companion **Record** and **separate from** [work-jiang](../../../work-jiang/README.md) lecture corpora.

**Not Voice knowledge** until anything is merged through **RECURSION-GATE** per [AGENTS.md](../../../../AGENTS.md).

---

## Predictive History (work-strategy default channel)

**[predictive-history/README.md](../../youtube-channels/predictive-history/README.md)** is the **primary** repo path for **syncing** the Predictive History YouTube channel into `transcripts/*.txt` + `index.json`. That tree is **work-strategy–first**; see [common-inputs.md § PH](../../../../docs/skill-work/work-strategy/common-inputs.md).

**Flow:** Pull captions with the PH README CLI → diff / verify against [work-jiang/lectures/](../../../work-jiang/lectures/) curated `.md` when quoting → optional **digest** `.md` **here** for one-off Perceiver runs or analyst registry rows.

---

## Daily operator cadence

The operator may **upload one or more transcripts per day** for **work-strategy** topics of interest (paste in chat: **episode title**, optional **watch URL**, **body text**). Ingest pattern:

| Step | What |
|------|------|
| **File** | New `*.md` in this folder — kebab-case slug from title (optional date prefix `YYYY-MM-DD-` if you want sort-by-day). |
| **Header** | Source, URL (or “pin when known”), **ingested** date, participants. |
| **Body** | Short **Perceiver** neutral summary (≤200 words) + optional **strategy hooks** table + **full transcript** with light ASR cleanup. |
| **Git** | Follow **[Commit policy (ingest → git)](#commit-policy-ingest--git)** below. |
| **Three minds (chat)** | **Every ingest:** when the transcript file (and INDEX row, if applicable) is **done for the turn**, end with the **[post-entry lens offer](#three-minds-lens-offer-after-every-ingest)** — three one-line options (**Barnes → Mearsheimer → Mercouris**), each in that mind’s **linguistic fingerprint** (see [`skill-strategy` SKILL](../../../../.cursor/skills/skill-strategy/SKILL.md#post-entry-lens-offer)). Operator may skip or pick; do **not** run full lens analysis until they choose. |

Same guardrails as below: research upstream, not Record; verify numbers before ship-facing copy.

### Three minds lens offer (after every ingest)

This is the same **optional lens menu** as [`skill-strategy` Post-entry lens offer](../../../../.cursor/skills/skill-strategy/SKILL.md#post-entry-lens-offer), but **ingest is always a substantive artifact** — so the assistant **always** presents it once the digest exists (committed or not).

```
Lens pass (optional — pick one, combine, or skip):
- Barnes: <one line in Barnes linguistic fingerprint>
- Mearsheimer: <one line in Mearsheimer linguistic fingerprint>
- Mercouris: <one line in Mercouris linguistic fingerprint>
```

**Fingerprint:** Same requirement as [`skill-strategy` § Post-entry lens offer](../../../../.cursor/skills/skill-strategy/SKILL.md#post-entry-lens-offer) — read **LINGUISTIC FINGERPRINT** in [CIV-MIND-BARNES.md](../strategy-notebook/minds/CIV-MIND-BARNES.md), [CIV-MIND-MEARSHEIMER.md](../strategy-notebook/minds/CIV-MIND-MEARSHEIMER.md), [CIV-MIND-MERCOURIS.md](../strategy-notebook/minds/CIV-MIND-MERCOURIS.md). No generic placeholder lines.

**Rules:** **B → M → M** order; **one-liners in-voice only** until the operator picks; not a default **tri-frame** deep pass unless they ask (see [strategy-minds-granular](../../../../.cursor/rules/strategy-minds-granular.mdc)). If they pick a lens, append to that day’s **`days.md`** block per [MINDS-SKILL-STRATEGY-PATTERNS](../../../../docs/skill-work/work-strategy/minds/MINDS-SKILL-STRATEGY-PATTERNS.md) recipes.

---

## Commit policy (ingest → git)

**Goal:** One predictable rule so **ingest** and **EXECUTE_LOCAL** are not confused.

| Action | Default |
|--------|---------|
| **Write** transcript `*.md` + **append** [analyst-corpus INDEX](../analyst-corpus/INDEX.md) when applicable | When the operator clearly wants a **durable** ingest — same turn as the file bodies. |
| **`git commit` (local)** | **Do it in the same turn** when the ingest is complete (new/updated transcript + INDEX row), so the repo matches chat. **Unless** the operator says **draft only**, **no commit**, **PLAN** (no file permission), or **stash** / **don’t commit** — then leave **uncommitted** working tree. |
| **`git push` (remote)** | **Not** implied by ingest. Only when the operator says **EXECUTE** (with push), **DOCSYNC** (with push), or **git push** / **push to origin**. |

**Bundling:** Checklist or stub edits done **as part of the same ingest** may sit in the **same commit** as the transcript; unrelated lane work should stay **out** of that commit (see [repo-hygiene-pass](../../../../.cursor/skills/repo-hygiene-pass/SKILL.md)).

---

## Layout

| Pattern | Use |
|---------|-----|
| **Curated digest** | `*.md` in this folder — YAML or front matter optional; body = transcript excerpt + **source URL**, **date**, **operator summary** (see [work-dev/transcripts/nate-b-jones-ai-job-market-seven-skills-2026.md](../../work-dev/transcripts/nate-b-jones-ai-job-market-seven-skills-2026.md) for shape). **Commit** when the digest is the durable artifact. |
| **Raw captions** | `*.txt` from YouTube/podcast ASR — may stay **local-only** (gitignore) if large; prefer provenance header (`# url: …`, `# fetched_at_utc: …`). |

---

## How to ingest

1. **Manual paste** — Drop text into a new `.md` or `.txt`; add source line at top.
2. **YouTube (same tooling as other lanes)** — For **Predictive History** channel videos, use [youtube-channels/predictive-history/README.md](../../youtube-channels/predictive-history/README.md) and `scripts/fetch_youtube_channel_transcripts.py` (raw usually under `youtube-channels/predictive-history/transcripts/`, often gitignored). For **work-strategy-only** sources (e.g. GTC panels, strategy podcasts), either copy the fetched `.txt` here with a note **or** add a channel folder under `research/external/youtube-channels/` following that README’s pattern.
3. **Downstream** — Run **Perceiver** (neutral fact summary ≤200 words) from the file; then [current-events-analysis.md](../../../../docs/skill-work/work-strategy/current-events-analysis.md) (energy hook if relevant → lenses → synthesis). Log outcomes in **STRATEGY.md** §III / §IV (operator strategy log) when useful.
4. **Same turn — lens menu** — Present **[Three minds lens offer](#three-minds-lens-offer-after-every-ingest)** in chat (see table row above). **Skip** only if the operator said **no menu** / **no options** for that turn.

---

## Guardrails

- Treat long-form media as **narrative + opinion** unless triangulated with **primary** or **cited news** — see [external-tech-scan.md](../../../../docs/skill-work/work-strategy/external-tech-scan.md).
- **work-politics** ship copy still needs **sources** and gate policy; transcripts here are **upstream** research.

---

## See also

- [Tucker Carlson curated book](../../youtube-channels/tucker-carlson/README.md) — **highly curated** index (not full channel); processed bodies still live **here** as `*.md`.
- [Analyst corpus INDEX](../analyst-corpus/INDEX.md) — register each transcript row + optional per-analyst notes under `analyst-corpus/analysts/<slug>/`.
- [common-inputs.md](../../../../docs/skill-work/work-strategy/common-inputs.md) — shared inputs with work-politics.
- [work-strategy README](../../../../docs/skill-work/work-strategy/README.md) — territory index.
