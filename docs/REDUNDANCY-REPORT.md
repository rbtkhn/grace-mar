# Repository Redundancy Report

Scan for duplicate code, duplicate content, and redundant patterns. Not an exhaustive audit; highlights the main areas.

---

## 1. **Duplicate `_read(path)` helper**

**Where:** At least **25+ scripts** define the same or nearly identical helper:

```python
def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""
```
(or `if not path.exists(): return ""` then `return path.read_text(...)`)

**Files (sample):**  
`process_approved_candidates.py`, `harness_warmup.py`, `export_prp.py`, `export_view.py`, `export_fork.py`, `export_symbolic.py`, `export_curriculum.py`, `export_manifest.py`, `export_intent_snapshot.py`, `export_engagement_profile.py`, `export_user_identity.py`, `recursion_gate_review.py`, `metrics.py`, `generate_profile.py`, `session_brief.py`, `operator_blocker_report.py`, `parse_we_did.py`, `openclaw_heartbeat.py`, `pending_dedup_hint.py`, `fork_checksum.py`, `measure_growth_and_density.py`, `generate_wap_weekly_brief.py`, `proposal_brief.py`, `load_alpha_school_benchmarks.py`, `export_runtime_bundle.py`, `work_politics_ops.py`, `generate_lesson_prompt.py`, `bot/retriever.py`, and others.

**Reuse already present:**  
`operator_handoff_check.py` and `operator_daily_warmup.py` import `_read` from `harness_warmup`; `export_manifest` imports from `export_intent_snapshot`.

**Recommendation:** Add a small shared module (e.g. `scripts/repo_io.py` or `scripts/_common.py`) with `def read_path(path: Path) -> str` and `REPO_ROOT`; have scripts that only need read+root import from there. Reduces copy-paste and keeps encoding/behavior in one place.

---

## 2. **Duplicate REPO_ROOT / profile path setup**

**Where:** Many scripts repeat:

```python
REPO_ROOT = Path(__file__).resolve().parent.parent
PROFILE_DIR = REPO_ROOT / "users" / user_id   # or REPO_ROOT / "users" / "grace-mar"
```

**Recommendation:** Same shared module can expose `REPO_ROOT` and `profile_dir(user_id: str) -> Path`. Optional; some scripts need REPO_ROOT for non-user paths (e.g. `bot/`, `docs/`).

---

## 3. **Duplicate default user id**

**Where:** The pattern

```python
os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"
```

(or `default="grace-mar"` in argparse) appears in **40+** places: bot (core, retriever, bot.py), `apps/miniapp_server.py`, and most scripts that take `-u` / `--user`.

**Recommendation:** Centralize in one place, e.g. `scripts/_common.py` or `bot/conf.py`:  
`DEFAULT_USER_ID = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"`.  
Scripts and bot import it; argparse uses `default=DEFAULT_USER_ID`. Reduces drift if env or default ever changes.

---

## 4. **Multiple recursion-gate parsers**

**Where:**

| Module | Function(s) | Returns / purpose |
|--------|-------------|--------------------|
| `recursion_gate_review.py` | `split_gate_sections(full_md)` | (candidates_section, processed_section) |
| `recursion_gate_review.py` | `parse_review_candidates(...)` | Structured candidate list for review |
| `recursion_gate_territory.py` | `pending_by_territory(pr_content)` | Pending split by wap vs companion |
| `metrics.py` | `parse_recursion_gate(content)` | (pending_list, processed_list) with id/status/outcome |
| `generate_profile.py` | `parse_recursion_gate(content)` | (count, list of dicts with summary, mind_category, priority_score) |

So there are **three** different “parse recursion-gate” shapes: (1) raw section split, (2) pending + processed with status/outcome, (3) pending count + list with summary/mind_category/priority_score. Territory logic adds another layer.

**Recommendation:** Treat `recursion_gate_review` (and territory) as the canonical source for “candidates + processed” and “pending by territory.” Have `metrics.py` and `generate_profile.py` call into it (or a thin adapter) instead of maintaining separate parsers. One read/parse, multiple views. Reduces risk of regex/section drift and duplicate maintenance.

---

## 5. **Duplicate section / YAML extraction**

**Where:** Several scripts implement similar helpers:

- `export_prp.py`: `_section()`, `_yaml_list()`, `_yaml_value()`
- `generate_lesson_prompt.py`: `_section()`, `_yaml_value()`, `_yaml_list()`, `_parse_yaml_list()`
- `export_user_identity.py`: `_section()`
- `export_view.py`: `_section()`
- `export_curriculum.py`: `_extract_yaml_list()`
- `generate_profile.py`: internal `_section(title, filename, content)` for HTML

Signatures and regexes differ slightly (e.g. section by `## Title` vs next `##`). Not all need the same return shape.

**Recommendation:** Low priority. If a shared “markdown section + YAML field” util is added, it should live in one module and support the call patterns used by export_prp, generate_lesson_prompt, and export views. Optional refactor.

---

## 6. **APPLIED-THEOLOGY.md vs beauty-and-the-blade-manuscript.md**

**Relationship:** Manuscript is the same body of content as the main book (*Beauty and the Blade*), with a **title page / manuscript front matter** and **end matter** (e.g. Sources and References). Body is kept in sync manually or by convention.

**Redundancy:** Intentional dual artifact (web/source vs submission manuscript). Not code redundancy; content is deliberately mirrored. Risk is **drift** if only one file is updated.

**Recommendation:** Document the convention (e.g. in `docs/civilization-memory/book/README.md`): “Body sections mirror APPLIED-THEOLOGY.md; manuscript adds title page and end matter.” Optionally add a small script or check that compares section hashes between the two and reports drift (no auto-merge, to preserve editorial control).

---

## 7. **Duplicate sys.path manipulation**

**Where:** Many scripts that import from `scripts` do:

```python
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
```
or `sys.path.insert(0, str(REPO_ROOT))`.

**Recommendation:** Acceptable; each script is runnable standalone. Consolidating would require a single entrypoint or installed package. No change unless the repo moves to a package layout.

---

## 8. **Documentation overlap**

**Where:** Some conceptual overlap between:

- `AGENTS.md` (guardrails, pipeline, triadic cognition)
- `docs/grace-mar-core.md` (governance)
- `docs/conceptual-framework.md` (Record, Voice, terminology)
- `docs/architecture.md` (system design)

and between skill-work READMEs and central docs. Not full duplication; cross-links and different audiences.

**Recommendation:** Keep as is. Optional: add a one-page “Where to read what” (or extend readme) so new contributors know which doc to open for pipeline vs architecture vs concepts.

---

## 9. **Civ-mem / book content**

**Where:**  
- `docs/civilization-memory/essays/` (e.g. ONE-SUBJECT-MANY-TONGUES, UNIVERSAL-LOVE-AND-MASTERY, WRITING-THE-BOOK-AND-DEATH) are source essays.  
- `APPLIED-THEOLOGY.md` incorporates or adapts that content into one book.

So there is **intentional** reuse of ideas and text (essays → book), not accidental duplication. Same as manuscript: risk is drift if essays are updated and the book is not (or vice versa).

**Recommendation:** Document that the book is the assembled artifact; essays are sources. No structural change.

---

## Summary table

| # | Category | Severity | Action |
|---|----------|----------|--------|
| 1 | `_read()` in 25+ scripts | High (copy-paste) | Shared `repo_io` / `_common` with `read_path()` |
| 2 | REPO_ROOT / profile_dir repeated | Medium | Same shared module |
| 3 | Default user id in 40+ places | Medium | Single `DEFAULT_USER_ID` (and argparse default) |
| 4 | Multiple recursion-gate parsers | Medium | Canonical parse in recursion_gate_review; others call or adapt |
| 5 | Section/YAML extraction in exports | Low | Optional shared util |
| 6 | APPLIED-THEOLOGY vs beauty-and-the-blade-manuscript | Intentional | Document convention; optional drift check |
| 7 | sys.path insert in scripts | Low | Leave as is |
| 8 | Doc overlap | Low | Optional “where to read what” |
| 9 | Civ-mem essays vs book | Intentional | Document relationship |

---

*Report generated from repository scan. Recommendations are optional; implement when they reduce maintenance cost or drift risk.*
