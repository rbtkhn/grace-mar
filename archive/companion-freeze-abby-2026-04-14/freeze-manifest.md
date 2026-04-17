# Companion Freeze — Abby (Grace-Mar)

**Frozen:** 2026-04-14
**Git tag:** `companion-freeze/abby-2026-04-14`
**System:** grace-mar
**Companion:** Abby (Grace-Mar), age 6, Colorado, first grade
**Record status at freeze:** SEEDING

---

## Contents

### Structured exports (machine-readable)

| Directory | Export class | Script | Format |
|-----------|-------------|--------|--------|
| `export-full/` | Full governed profile | `export_runtime_bundle.py --mode portable_bundle_only` | Runtime bundle (JSON + MD) |
| `export-prp/` | Tool bootstrap profile | `export_prp.py` | Portable Record Prompt (text) |
| `export-fork/` | JSON fork | `export_fork.py` | Single JSON file |
| `export-capability/` | Demonstrated capability | `export_capability.py` | JSON (SKILLS + EVIDENCE + rationales) |

### Raw Record files (human-readable markdown)

| File | Surface |
|------|---------|
| `raw-record/self.md` | SELF — identity, preferences, knowledge, curiosity, personality |
| `raw-record/self-archive.md` | EVIDENCE — READ, WRITE, CREATE, ACT entries |
| `raw-record/self-skills.md` | SKILLS — capability claims, gaps, struggles |
| `raw-record/skill-think.md` | THINK skill surface |
| `raw-record/skill-write.md` | WRITE skill surface |
| `raw-record/skill-steward.md` | STEWARD skill surface |
| `raw-record/self-history.md` | Derived history timeline |

### Companion-specific files

| File | Description |
|------|-------------|
| `companion-files/companion-context.md` | Artistic style survey, personality notes |
| `companion-files/survey-capture.md` | Seed survey capture template |
| `companion-files/seed-phase-2-survey.md` | Phase 2 seed survey responses |
| `companion-files/seed-phase-3-survey.md` | Phase 3 seed survey responses |
| `companion-files/analysis-homework-samples-2026-02-24.md` | Homework sample analysis |
| `companion-files/audit-grok-transcript-2026-02-24.md` | Grok transcript audit |
| `companion-files/journal.md` | Companion journal |
| `companion-files/health-fitness-profile.md` | Health/fitness profile |
| `companion-files/health-fitness-profile-hannah.md` | Hannah health/fitness profile |
| `companion-files/health-fitness-survey-hannah.md` | Hannah health/fitness survey |
| `companion-files/user.md` | Derived OpenClaw identity export |
| `companion-files/gate-dashboard.html` | Derived gate dashboard |

### Artifacts (schoolwork, creative work)

All images and reports from `users/grace-mar/artifacts/` — includes WRITE entries (handwriting samples, journal pages), CREATE entries (drawings, collages), simulation reports, and creative/draft directories.

### Supporting data

| Directory | Description |
|-----------|-------------|
| `rationales/` | Artifact-rationale JSON files (WRITE-0003, WRITE-0006, CREATE-0001, CREATE-0004, CREATE-0005) |
| `notes/` | Telegram conversation log (2026-02-25) |
| `review-queue/` | Boundary classification JSONs (CANDIDATE-0997/0998/0999) |
| `reflection-proposals/` | Reflection cycle output (REFLECT-20260322-001 + index) |
| `metrics/` | Voice judgment probe baselines (baseline, current, demo) |

---

## Re-import instructions

To restore this Record in a future companion-self instance:

1. **Quick Voice access:** Paste `export-prp/grace-mar-prp.txt` into any LLM conversation.
2. **Full runtime sideload:** Copy `export-full/` contents into a new instance's `users/<id>/runtime-bundle/`.
3. **JSON fork import:** Use `export-fork/fork-export.json` with `scripts/import_working_identity_candidates.py` or direct JSON loading.
4. **Capability portfolio:** `export-capability/capability-export.json` contains SKILLS + EVIDENCE for capability-focused contexts.
5. **Raw markdown:** All `raw-record/` files are self-describing and human-readable without any tooling.

The git tag `companion-freeze/abby-2026-04-14` preserves the complete repo state at freeze time, including all operational files, WORK lanes, and git history.
