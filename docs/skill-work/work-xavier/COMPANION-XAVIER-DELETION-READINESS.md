# companion-xavier deletion readiness checklist

Use this before deleting or archiving `companion-xavier` as a separate repository surface.

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
- [ ] Run first `good morning` with:
  - [ ] `work-dev` sync check
  - [ ] `work-politics` sync check
  - [ ] template alignment check (GitHub upstream)
  - [ ] `SYNC-DAILY` update
  - [ ] `DAILY-OPS-CARD` final output
- [ ] Stage (not merge) first candidates safely.

Result: `PASS` / `FAIL`

---

## 2) Dependency audit

- [ ] No required flow step depends on `work-xavier/companion-xavier/*`.
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

