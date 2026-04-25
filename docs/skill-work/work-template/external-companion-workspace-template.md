# External Companion Workspace Template

**Status:** Template / additive pattern  
**Scope:** How Grace-Mar may host a **WORK / advisor** lane for a **different person’s** companion instance, governed workspace, or public/config repo—without becoming that person’s Record.  
**Boundary:** This document is **WORK-only** guidance. It does **not** authorize copying `users/grace-mar/**` into another companion’s tree, mirroring another companion’s gated Record prose without trace, or treating the advisor lane as canonical identity truth for anyone other than the companion whose Record lives in **their** repo.

---

## Purpose

Use this pattern when Grace-Mar needs a **durable operator surface** to support someone else’s companion journey: coaching notes, handoffs, mirrors of *workflow* docs, evidence exports, and launch materials—while keeping **strict separation** between:

| Layer | Where it lives | Role |
|-------|----------------|------|
| **WORK / advisor lane** | Under `docs/skill-work/work-<id>/` in grace-mar (or equivalent) | Runbooks, drafts, operator memory—not another companion’s sovereign Record |
| **External companion’s instance repo** | Their GitHub (or other) repository from [companion-self](https://github.com/rbtkhn/companion-self) or chosen template | `users/<their-id>/`, gate, seed survey, Voice wiring—the **home** for their fork’s machinery |
| **External companion’s gated Record** | Same instance repo, merged only through **their** gate and approval path | Durable identity truth (`self.md`, EVIDENCE, prompt)—never silently “owned” by grace-mar WORK |
| **Optional public / config repo** | e.g. OB1-style instance layer | Config, docs, community—still **not** a substitute for the companion’s Record unless their own governance says so |

Grace-mar **advises, mirrors (where allowed), and prepares**; the **external companion** (and their operator) **owns** promotion into their Record.

---

## Allowed contents (advisor lane)

- **Runbooks** — operator procedures, checklists, cadence docs  
- **Handoffs** — paste packs, agent prompts, launch steps for **their** repo (without embedding grace-mar Record paths as truth)  
- **Evidence pointers** — screenshots, exports, dated notes (immutable where policy requires)  
- **Mirrors** — of **workflow** and operator artifacts only (see Mirror rule below)  
- **Progress logs** — qualitative coaching / operator observations in WORK  
- **Onboarding copy** — drafts destined for **their** review, not silent `self.md` edits  
- **Launch / community materials** — operator-owned or companion-approved drafts  
- **Checklists** — leakage, sync, ship gates  
- **Operator notes** — hypotheses, next actions, ledger items  

---

## Prohibited contents (advisor lane)

- **Another companion’s canonical Record** — do not host `self.md`, merged EVIDENCE, or prompt as the lane’s “source of truth” for *their* identity  
- **Copied `users/grace-mar/**` material** — do not paste or sync grace-mar companion Record trees into an external companion template or example bundle  
- **Silent edits to another companion’s `self.md`** (or equivalent)—all identity changes go through **their** pipeline  
- **Merge outputs bypassing that companion’s gate** — no “shadow Record” updated only from grace-mar  
- **Secrets** — credentials, tokens, private keys (see lane leakage checklists)  

---

## Canonical boundary

- **Durable identity truth** lives in the **external companion’s own** instance repo under their governance.  
- **Durable identity changes** must pass through **that companion’s** recursion gate (or equivalent review surface), **their** approval, and **their** merge / governed-apply step—never only through a grace-mar WORK commit.

---

## Recommended promotion path (into *their* Record)

1. **Draft / observation / coaching note** — in the advisor WORK lane (or operator scratch), clearly labeled as non-authoritative.  
2. **Candidate** — packaged for **their** `recursion-gate.md` (or equivalent) with id + summary.  
3. **External companion recursion gate (or equivalent)** — visible queue; no silent merge.  
4. **Approval** — companion (and operator where applicable) decides.  
5. **Merge script / governed apply step** — e.g. `process_approved_candidates.py --apply` **in their repo**, per their instance doctrine.  
6. **Record** — only after the above; grace-mar WORK remains a **mirror or draft source**, not the merge authority.

---

## Recommended lane shape (files / folders)

Names are indicative; adapt per lane without inventing a new framework:

| Artifact | Role |
|----------|------|
| `README.md` | Hub: purpose, boundary, “not their Record,” leakage pointer |
| `INDEX.md` | Flat lookup for operators |
| `SYNC-DAILY.md` (or lane daily surface) | Advisor cadence / snapshot |
| `WORK-LEDGER.md` | Compounding watches and experiments (WORK-only) |
| `LEAKAGE-CHECKLIST.md` | Pre-handoff: no grace-mar Record in their tree |
| `LANE-CI.md` | PR labels, drift guard where used |
| `legacy-aliases.yml` | **When** a rename or identity transition exists—machine-readable legacy path allowlist (optional; see [work-cici/legacy-aliases.yml](../work-cici/legacy-aliases.yml) as one example) |
| `progress-log.md` (or lane-named variant) | Operator observations—not a substitute for their EVIDENCE spine |
| `work-profile.md` (or lane-named variant) | Employee / operator WORK profile if used—**not** their SELF |
| `sources.md` | Authorized feeds and pointers |
| `history.md` | Dated milestones in WORK |
| `evidence/` | Operator evidence artifacts |
| `handoffs/` | Paste-ready payloads for **their** repo |
| `mirrors/` | Synced **non-Record** workflow docs only, per contract |

---

## Directionality rule

Grace-mar may **advise**, **mirror** (non-Record), **summarize**, **prepare drafts**, and maintain **WORK-local** memory for the advisory lane.

Grace-mar may **not** silently become the **source of truth** for another companion’s identity. If a draft graduates to truth, that transition happens **only** in **their** repo through **their** gate.

---

## Mirror rule

- **Mirror** workflow docs and **operator** artifacts the external companion (or operator) expects to stay aligned with—under an explicit **sync contract** when mirrors exist.  
- **Do not** mirror gated Record prose unless the external companion has **explicitly approved** the flow **and** the receiving repo preserves an **approval trace** (who approved what, when). When in doubt, link instead of mirroring.

---

## Retirement path

1. **Stop** active advisory cadence (daily surface, digests).  
2. **Close** ledger items and open operator loops in WORK-LEDGER.  
3. **Archive** experiments under a dated note or `*-archived/` with a short README.  
4. **Leave** the external companion’s instance repo **untouched**—no bulk deletes on their side from grace-mar automation.  
5. **Remove** grace-mar automation (scripts, workflows) **only after** confirming no operator depends on it.

---

## Model example (reference only)

**[work-cici](../work-cici/README.md)** is an **in-repo reference implementation** of an external-companion advisor lane: Cici-first active prose, legacy continuity metadata, mirrors, and strict “not her Record” language. **Do not** treat work-cici as mandatory content to copy into another lane; **do** reuse the **boundary shape** (hub README, leakage checklist, gate-forward promotion) for other supported companions.

---

**Index:** [work-template README](README.md) · [MAPPING.md](MAPPING.md).
