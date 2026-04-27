---
name: strategy-notebook-lane-split
preferred_activation: lane split
description: Build two strategy-notebook refined pages (host + guest, or A/B expert lanes) from a single multi-expert raw-input transcript, with a shared filename slug, cross-links, and lane-distinct Verbatim. WORK lane, strategy-notebook. Use when the operator says lane split, two-lane refined page, or multi-expert same raw two pages.
portable: false
version: 0.1.0
tags:
- operator
- work-strategy
- strategy-notebook
---

# Strategy notebook — multi-expert lane split (refined pages)

**Preferred activation (operator):** **`lane split`**, **`two-lane refined page`**, **`host + guest refined pages`**, or naming both **`expert_id`s** and the same **`pub_date`**.

## When to use

- A **`raw-input/YYYY-MM-DD/… .md`** file carries **more than one** [strategy `expert_id`](../../../docs/skill-work/work-strategy/strategy-notebook/strategy-commentator-threads.md) in YAML **`threads: […]`** (e.g. host and guest on one YouTube).
- You need **separate** refined judgments by **role**: host lane (interview/coda/Eurasia framing) vs guest lane (substantive claim stack), or any **A** vs **B** lane the operator names.

**Do not** paste the **same** `### Verbatim` in two files — each file gets **only that lane’s speaker-tagged lines** from the **same** `raw-input` file (concatenate all `**Host Name:**` / `**Guest Name:**` turns for that voice). **Paraphrase or “host-arc” narrative belongs in `### Reflection`**, not in `### Verbatim` ([refined-page-template.md](../../../docs/skill-work/work-strategy/strategy-notebook/refined-page-template.md) **SSOT hierarchy** + **Verbatim** rule). **Target** **~3000** words per page, **~70–80%** verbatim; if a lane exceeds the verbatim budget, **condense** (head/tail or paragraph prune) with **`refined_page_word_budget.py condense`**, and list **Omissions** in **Appendix**. Optional helper: `python3 scripts/strategy/extract_transcript_speaker_lanes.py <raw.md> --list` / `--print glenn` (keys depend on labels in the raw).

## SSOT and naming

1. **One** verbatim on disk. **`pub_date` / folder** and **`threads:`** in frontmatter match [raw-input README](../../../docs/skill-work/work-strategy/strategy-notebook/raw-input/README.md) (e.g. `transcript-diesen-crooke-iran-…-YYYY-MM-DD.md`).
2. **Shared middle slug** (from the raw stem, kebab-case) — e.g. `diesen-crooke-iran-global-war-world-order`. Pick **one** order for the pair (**host-guest** or **alphabetical** by `expert_id`); use **the same** stem in both experts’ files.
3. Refined page filenames: **`{expert_id}-page-YYYY-MM-DD-{shared-slug}.md`**, one under each **`experts/{expert_id}/`**. Remove or avoid a same-day **`*-page-YYYY-MM-DD.md`** without **`<slug>`** if it would **collide** with the pair or duplicate one lane’s content.

## Lane content (contract)

| Lane | `### Verbatim` (required shape) |
|------|----------------------------------|
| **Host / A** | **All** dialogue lines spoken by the **host** in the shared `raw-input` transcript (same words as raw; optional light clean per template). *Analytical* description of the host’s “arc” → **`### Reflection`**, not `### Verbatim`. |
| **Guest / B** | **All** dialogue lines spoken by the **guest** in the same raw file. |

- **`### Reflection`**: state the **lane contract**; point to the **sibling** file for the other role (relative path: `../other-expert/...`).
- **`### Foresight`**: lane-specific; when both touch the same event (e.g. vdl), note **seams** (host: multipolar literacy; guest: governance/alignment) so EOD `days.md` does not merge two planes unlabeled.
- Follow [refined-page-template.md](../../../docs/skill-work/work-strategy/strategy-notebook/refined-page-template.md): avoid scattered bold in body sections; appendix bullet order and titles per template.

**Preamble line:** include **Guest/Interviewer (same air)** and **Capture:** two-expert YT (or source), plus a **sibling** link to the other refined file in the first screen.

## Triage and inbox

- **`experts/{id}/transcript.md`**: under the **`## YYYY-MM-DD`** section, add for each file a **`Refined | cold:`** line and a **`Sibling (host|guest):`** line pointing to the other lane. Keep the **Inbox** pointer to the raw SSOT; **`thread:`** / **`crosses:`** per [daily-strategy-inbox.md](../../../docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md) (optional **two cold lines, same URL** for the same interview).
- Inbox long rows may list **two** `thread:` hooks; do not paste the full transcript twice.

## Machine checks

- Run **`python3 scripts/strategy/audit_refined_pages.py`** on new refined pages; fix appendix order if flagged.
- Grep for old filenames if replacing an undated **`*-page-YYYY-MM-DD.md`**.
- **Mearsheimer** auto-assembler: `scripts/strategy/assemble_mearsheimer_pages_verbatim.py` can **overwrite** a guest `mearsheimer-page-*.md` with a full **embed** from `raw-input`. For an entry that uses **lane split** (compressed **guest** **Verbatim**), set **`skip_assembly: true`** on that **manifest** row in **`mearsheimer-pages-manifest.yaml`** so the script **skips** the file. (Do **not** run the assembler to “refresh” lane-split pages unless you intend to move back to full-embed mode.)
- **Ritter** auto-assembler: `scripts/strategy/assemble_ritter_pages_verbatim.py` — same **`skip_assembly: true`** guard on **`ritter-pages-manifest.yaml`** for lane-split guest pages so a full-embed pass does not overwrite compressed **Verbatim**.

## Guardrails

- **WORK only** — not Record, not gate merges.
- **Not** a substitute for **`expert cross-weave`** in **`days.md`**; lane-split is **on-disk** refined page pair; **weave** runs at EOD when you fold the seam.
- If only **one** voice matters for a given episode, use **a single** refined page (guest-first is common) and **pointers** in the other `transcript.md`—**do not** create empty “lane” files.

## See also

- [refined-page-template.md](../../../docs/skill-work/work-strategy/strategy-notebook/refined-page-template.md) — `same-day` **slug** rule, appendix bullets.
- [raw-input README § Multiple refined pages](../../../docs/skill-work/work-strategy/strategy-notebook/raw-input/README.md)
- [`.cursor/skills/strategy-notebook-expert-cross-weave/SKILL.md`](../strategy-notebook-expert-cross-weave/SKILL.md) — folding two experts into one **`days.md`** seam.
- [strategy-commentator-threads.md](../../../docs/skill-work/work-strategy/strategy-notebook/strategy-commentator-threads.md) — `crosses:`, `thread:`

## Example (grace-mar), 2026-04-27

- Raw: `raw-input/2026-04-27/transcript-diesen-crooke-iran-global-war-world-order-2026-04-27.md`
- Refined: `experts/diesen/diesen-page-2026-04-27-diesen-crooke-iran-global-war-world-order.md` (host) + `experts/crooke/crooke-page-2026-04-27-diesen-crooke-iran-global-war-world-order.md` (guest)
