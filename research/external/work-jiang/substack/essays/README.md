# Predictive History — Volume VII: Essays (curated text)

**Volume:** These files are **Volume VII — Essays** of the **Predictive History** multivolume line — the **written newsletter** (published on Substack). Book scope and ordering rules: [book/VOLUME-VII-ESSAYS.md](../../book/VOLUME-VII-ESSAYS.md).

**Purpose:** Hold **full essay bodies** so you can search, diff, and analyze Substack posts **in-repo**, the same way you use `lectures/` for video (Volumes I–V) and `interviews` for Volume VI.

**Canonical URL** for each piece remains [Predictive History on Substack](https://predictivehistory.substack.com/). This folder is an **operator mirror** for research tooling.

## Conventions

| Item | Rule |
|------|------|
| **Filename** | Substack post slug exactly: `<slug>.md` (matches `/p/<slug>`). |
| **Front matter** | Required — see any file here for fields. |
| **Body** | Paste your own export or subscriber copy under `## Essay body`. |
| **Rights** | You are responsible for **copyright** and **Substack terms**. Prefer **private** git remotes for paid posts; do not redistribute publicly without permission. |
| **Crosswalk** | [../README.md](../README.md) maps themes to `lectures/`; each section links to the matching file here. |
| **Analysis** | One memo per essay: `research/external/work-jiang/analysis/essay-<slug>-analysis.md`. |

## Adding a new post

1. Create `essays/<slug>.md` from the template below (or copy an existing essay file).
2. Add or extend a section in [../README.md](../README.md) with URL, date, and overlap table.
3. Create `analysis/essay-<slug>-analysis.md` (copy from `essay-the-acceleration-analysis.md` and replace metadata).
4. Run `python3 scripts/work_jiang/validate_work_jiang.py` from repo root.

### Front-matter template

```yaml
---
source_kind: substack_essay
essays_volume: 7
substack_slug: your-slug-here
canonical_url: https://predictivehistory.substack.com/p/your-slug-here
title: "Post title as on Substack"
publication_date: "YYYY-MM-DD"
deck: "Optional subtitle / deck line from Substack"
paid: true
ingested_at: "YYYY-MM-DD"
rights_note: "Operator-sourced copy for research; Substack is canonical."
---

# Title (repeat or shorten)

## Essay body

(Paste full text here.)
```

**Note:** `scripts/work_jiang/normalize_analysis_frontmatter.py` only auto-fills memos whose filenames start with an **11-character YouTube id**. Volume VII (Essays) analysis files use the `essay-<slug>-analysis.md` pattern and are **edited by hand** (or extend the script later).
