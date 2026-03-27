# work-career

**Operator work territory** — preparing for high-signal AI / agentic roles (K-shaped labor market framing) **without** treating job notes or drafts as Record truth. See [AGENTS.md](../../../AGENTS.md): merge into SELF / EVIDENCE / prompt only through the gated pipeline.

**Not:** web scraping of job boards in v1 (ToS, fragility). **Yes:** manual JSON/CSV you export or paste, filtered and reviewed locally.

---

## Conventions

| Item | Location |
|------|----------|
| This README + templates | `docs/skill-work/work-career/` |
| Manual job list (commit **example** only; real list optional local) | [data/ai-jobs.manual.example.json](data/ai-jobs.manual.example.json) |
| JSON shape | [data/ai-jobs.manual.schema.json](data/ai-jobs.manual.schema.json) |
| Skill proof worksheet | [skill-demo-worksheet.md](skill-demo-worksheet.md) |
| Opportunity / application draft scaffold | [job-opportunity-review-template.md](job-opportunity-review-template.md) |
| Scripts | `scripts/work_career/` |
| Paste-ready gate drafts | [users/grace-mar/reflection-proposals/](../../../users/grace-mar/reflection-proposals/) or [recursion-gate-staging/](../../../users/grace-mar/recursion-gate-staging/) with `DRAFT-` prefix |

**Do not** create `users/grace-mar/review-queue/` for jobs — template JSON queues live under `users/demo/review-queue` and `users/_template/review-queue`.

---

## Related repo artifacts

- [Specification precision (work-dev)](../work-dev/templates/specification-precision.md)
- [Failure pattern checklist](../../../users/grace-mar/recursion-gate-staging/failure-pattern-checklist.md)
- [Nate B. Jones digest — seven skills](../../../research/external/work-dev/transcripts/nate-b-jones-ai-job-market-seven-skills-2026.md)
- [Token economics CLI](../../../scripts/token_economics.py) — copy `scripts/token_economics_models.example.json` → `scripts/token_economics_models.json` for what-if cost blends; see [economic-benchmarks.md](../work-dev/economic-benchmarks.md)

---

## Commands (after scripts exist)

```bash
# Merge a CSV export into a single JSON list (dedupe by url)
python3 scripts/work_career/merge_job_export.py --input path/to/export.csv --output docs/skill-work/work-career/data/ai-jobs.manual.json

# Filter saved jobs by keywords (default list + optional --keywords-file)
python3 scripts/work_career/filter_jobs.py --input docs/skill-work/work-career/data/ai-jobs.manual.json

# Check worksheet links point at existing repo paths
python3 scripts/work_career/skill_gap_checklist.py --worksheet docs/skill-work/work-career/skill-demo-worksheet.md
```

---

## Principle

Labor-market statistics in external media are **not** integration truth. Use this lane for **your** opportunities and **honest** proof links — not placeholder “example corp” listings committed as fact.
