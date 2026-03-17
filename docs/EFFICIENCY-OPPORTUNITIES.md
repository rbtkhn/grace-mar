# Repository Efficiency Opportunities (≥2% gains)

Brief scan for at least 2% efficiency gains. Focus: I/O reduction, duplicate work, and build/run-time.

---

## 1. **process_approved_candidates.py — Eliminate 4 redundant file reads (implemented)**

**Issue:** In the `--apply` path the script reads `recursion-gate.md`, `self.md`, `self-evidence.md`, and `prompt.py` at lines 885–888, then modifies them in memory. After the loop it reads all four **again** (948–953) to build `original_files` for rollback.

**Fix:** Build `original_files` from the initial in-memory content immediately after the first read (before the merge loop). Use that for both `_transactional_write` rollback and for the file_plan comparison. No second read.

**Impact:** Saves 4 file reads per merge (non-trivial when profile files are large). Reduces I/O and latency on every `--apply` run.

---

## 2. **docs/civilization-memory/book/website/build.py — Skip build when output is up to date (implemented)**

**Issue:** Every run reads the full MD file and regenerates HTML, even when `APPLIED-THEOLOGY.md` has not changed.

**Fix:** If `index.html` exists and its mtime ≥ `APPLIED-THEOLOGY.md` mtime, skip build and print "Already up to date." Optional: only when `--force` is not passed.

**Impact:** Repeated builds (e.g. after other edits, or in CI) do nothing when the book is unchanged — large time savings in those cases.

---

## 3. **bot/retriever.py — Optional in-process cache for load_record_chunks()**

**Issue:** `load_record_chunks()` reads SELF, SKILLS, EVIDENCE, WORK on every call. In a single bot session with multiple lookups, the same files are read repeatedly.

**Fix:** Cache the result (and optionally path mtimes) per process; invalidate when any source file mtime changes. Reduces I/O when multiple messages trigger retrieval in the same run.

**Impact:** ≥2% of total bot request time when several lookups occur in one session. Lower priority if the bot process is short-lived (one request per process).

---

## 4. **Recursion-gate parsing — Consolidate parsers (future)**

**Issue:** Multiple parsers for `recursion-gate.md`: `split_gate_sections` + `parse_review_candidates` (recursion_gate_review.py), `pending_by_territory` (recursion_gate_territory.py), `parse_recursion_gate` in metrics.py (pending + processed lists), `parse_recursion_gate` in generate_profile.py (different shape: count + list with summary/mind_category/priority_score). Each script that needs gate state may read and parse independently.

**Fix:** One canonical parser (or a small set with clear roles) in one module; others import and use. Reduces code surface and duplicate regex work when multiple scripts run in sequence. Efficiency gain is mainly in maintainability and fewer passes when gate is read multiple times in the same process; per-script run the gain is small unless we add a shared “gate state” cache.

**Impact:** Code/maintainability > 2% runtime per run; could reach ≥2% in workflows that run several gate-dependent scripts (e.g. warmup + gate review + metrics) if they were refactored to share one read.

---

## 5. **export_prp.py — Reuse section extraction**

**Issue:** Repeated regex for `_section()`, `_yaml_list()`, `_yaml_value()` over the same file content in different code paths.

**Fix:** Parse self.md (and other inputs) once into a small in-memory structure (e.g. dict of sections, key YAML fields); derive PRP from that. Reduces repeated scans over the same string.

**Impact:** Likely &lt;2% unless self.md is very large; still a clean refactor.

---

## 6. **Harness warmup / operator_daily_warmup — Shared gate read**

**Issue:** Both read `recursion-gate.md` and compute pending (warmup uses `pending_by_territory`; daily warmup has its own `_pending_candidates`). If both run in the same script or sequence, gate is read twice.

**Fix:** If daily warmup ever calls or is composed with harness_warmup (or vice versa), pass the gate content or a shared “gate state” instead of reading twice. Otherwise leave as is.

**Impact:** ≥2% only when both run in the same session; otherwise negligible.

---

## Summary

| # | Item | Status | Est. gain |
|---|------|--------|-----------|
| 1 | process_approved_candidates: avoid 4 re-reads | Implemented | I/O per merge |
| 2 | website build: skip when up to date | Implemented | 100% when unchanged |
| 3 | retriever cache (per process) | Optional | ≥2% in multi-lookup sessions |
| 4 | Consolidate recursion-gate parsers | Future | Maintainability + shared read |
| 5 | export_prp single-pass parse | Future | Small |
| 6 | Warmup scripts share gate read | If composed | When both run |

Implementing **1** and **2** gives immediate, low-risk gains. **3** is recommended if the bot often serves multiple lookups per process.
