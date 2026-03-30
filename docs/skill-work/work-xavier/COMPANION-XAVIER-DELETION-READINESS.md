# companion-xavier deletion readiness checklist

**Update (2026-03):** The **monorepo subtree** (`docs/skill-work/work-xavier/companion-xavier/`) was removed from grace-mar; **work-xavier** (advisor module) remains. Xavier’s **sovereign instance** is expected in **her own** `companion-xavier` GitHub repo. This checklist still applies if you need a **clean-room** proof that onboarding works from **companion-self** alone.

Use this before deleting or archiving **`companion-xavier` as her standalone repository** (not the old grace-mar subtree).

Goal: prove a new user can bootstrap from `companion-self` template without Xavier-specific rescue logic.

---

## Pass/fail gate

All sections below must be `PASS`.
Any `FAIL` means keep `companion-xavier` as validation harness.

---

## 1) Clean-room bootstrap test

- [ ] Create a fresh instance from `companion-self` (no Xavier subtree copied).
- [ ] Complete seed survey and capture without custom docs.
- [ ] Initialize WORK intake from survey + uploaded docs.
- [ ] Run first `hey` with:
  - [ ] `work-dev` sync check
  - [ ] `work-politics` sync check
  - [ ] template alignment check (GitHub upstream)
  - [ ] `SYNC-DAILY` update
  - [ ] `DAILY-OPS-CARD` final output
- [ ] Stage (not merge) first candidates safely.

Result: `PASS` / `FAIL`

---

## 2) Dependency audit

- [ ] No required flow step depends on a **nested instance subtree** inside grace-mar (removed); flows use **her repo** + companion-self template.
- [ ] No required onboarding doc still references deleted paths.
- [ ] All critical mechanics live in template or generic instance docs.

Result: `PASS` / `FAIL`

---

## 3) Operator load test

- [ ] New user completes first run in <= 90 minutes.
- [ ] Operator intervention is minimal (clarification, not rescue).
- [ ] No repeated confusion about gate boundaries or sync steps.

Result: `PASS` / `FAIL`

---

## 4) Safety and governance test

- [ ] No direct `self.md` edits during onboarding.
- [ ] Identity updates route through gate.
- [ ] Sync changes stay in mirror/work docs.
- [ ] Public-ship decisions remain human-approved.

Result: `PASS` / `FAIL`

---

## 5) One-week stability test

- [ ] 5 consecutive good-morning runs complete with logs updated.
- [ ] No skipped sync logs for > 3 days.
- [ ] `DAILY-OPS-CARD` produced daily and used for execution.
- [ ] Template-alignment drift handled without ad hoc process invention.

Result: `PASS` / `FAIL`

---

## Decision

- Delete/archive `companion-xavier` only if all sections pass.
- If any section fails, record fixes, rerun clean-room test, and reassess.

