# LEAKAGE-CHECKLIST — before merging companion-xavier seed PR

Use before committing or publishing any export of the `companion-xavier/` subtree.

- [ ] **No** `users/grace-mar/` path strings under `companion-xavier/users/xavier/` (except this policy doc referencing the rule).
- [ ] **No** Grace-Mar identity facts, IX-A/B/C body text, or `recursion-gate` candidates copied from the grace-mar fork.
- [ ] **`self-library.md`** has **empty** `entries:` or only Xavier-approved rows — **no** grace-mar LIB ids.
- [ ] **work-politics** material in monorepo remains **curated** — job comp / wallet / client secrets: confirm **private** repo only or redact for any public fork.
- [ ] **SEED-MANIFEST** matches what is actually on disk (paths, hashes optional in later passes).
- [ ] Run: `python3 scripts/check_companion_xavier_leakage.py` (must exit 0).
- [ ] Run: `python3 scripts/validate-integrity.py --user xavier --json` (review warnings).
