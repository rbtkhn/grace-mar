# skill-jiang — Learned heuristics (CURSOR_APPENDIX)

Append-only **promoted** rules from forward-chain runs. **Cap:** ~15 bullets; merge duplicates; deprecate falsified lines with `DEPRECATED (date): …`.

**Promotion bar:** A heuristic appears here only after it **survived** at least **two** scoring rounds without contradiction, or after operator merge at cadence (rounds 3, 6, 9, 12, 15, post–gt-18).

**Primary calibration source (v0.5.1):** [`lecture-forward-chain-gt-BLIND-prefix-only.md`](../../../research/external/work-jiang/prediction-tracking/lecture-forward-chain-gt-BLIND-prefix-only.md) (`run_mode: prefix_only`, 17 rounds, 2026-04-06). Cadence merges (3 / 6 / 9 / 12 / 15) are folded into the **post–gt-18** pass below; do **not** use historical [`lecture-forward-chain-gt-BLIND.md`](../../../research/external/work-jiang/prediction-tracking/lecture-forward-chain-gt-BLIND.md) for new hypothesis text.

---

## Learned heuristics

1. **Life-example triad before macro wedge:** Early Game Theory runs **dating → school → success/mobility** (student-life hooks) before large **group boundary** topics (e.g. immigration). *Source: chain rounds 1–4, merge M3.*
2. **Civilizational cycle after migration:** A **world-scale cycle / replacement** lecture often follows **immigration or group-status** stress. *Rounds 4–5.*
3. **Finance institutions before hegemon chapter:** **World’s Bank–class** institutional money lecture sets up a **named hegemon** “who wrote the rules” episode (e.g. America’s Game). *Merge M6.*
4. **Ideology mirror after hegemon:** **Communist specter / rival system** lecture often follows **U.S. constitutional–dollar** framing. *Rounds 7–8.*
5. **Hot-war theater after ideology stack:** Expect a **concrete conflict** episode (e.g. US–Iran) once **systems** and **hegemony** are on the table. *Round 8–9.*
6. **First “Law of …” after hot war:** **Named law** abstractions (asymmetry, escalation) follow the **first dedicated war** lecture. *Merge M9.*
7. **Escalation ladder before eschatology:** **Law of escalation** (pathways, nuclear, religious sites) bridges to **eschatological convergence**. *Rounds 10–12.*
8. **Epistemic / deep-network after convergence:** **Narrative control** or **elite maintenance** episode follows **multi-tradition eschatology** mapping. *Merge M12.*
9. **Law of proximity after epistemic turn:** **Domestic/nearest-player** law follows **transnational narrative** chapter. *Rounds 12–14.*
10. **Macro “return of history” after proximity:** **Systemic transition** thesis follows **internal driver** law. *Rounds 14–15.*
11. **Regional primacy thesis after macro reset:** **Who benefits** in the active war (e.g. Pax thesis) follows **order exhaustion** lecture. *Merge M15.*
12. **Capstone bundles leader + commodities + order:** Late series may **compress** Trump/leadership, **reset** language, and **resource realignment** in one closing arc. *Merge M18.*
13. **TBD “At a glance”:** When curated lecture summary is **TBD**, down-rank **mechanism** confidence; **title** may still anchor macro frame (e.g. reset / order). *Round 16.*
14. **Historical Volume IV BLIND (archive only):** [`lecture-forward-chain-gt-BLIND.md`](../../../research/external/work-jiang/prediction-tracking/lecture-forward-chain-gt-BLIND.md) + [`lecture-forward-chain-blind.jsonl`](../../../research/external/work-jiang/prediction-tracking/registry/lecture-forward-chain-blind.jsonl) — batch baseline + `run_kind: replay` closed-loop replay. **Not** a hypothesis source for new blind work. Maintenance / smoke: `closed_loop_gt18_runner.py`, `inject_blind_closed_loop_replays.py`, `run_blind_chain_rounds.py`.
15. **Large-K bundles:** For **K ≥ ~10**, use `bundle --trim-at-full-transcript` to save tokens without breaking the blind boundary; log `read_depth: summary` (see prefix-only rounds 10–17 in the canonical log).

## Known failure modes

- **last_episode_overweight:** Guessing **workplace** immediately after school/success when the series jumps to **migration** instead (round 3–4 transition).
- **TBD_glance_mechanism:** Title encodes arc but **At a glance** empty → risk of **overclaiming** lecture mechanism (mitigate: score **hit** only when title + stated prior align).
- **US-centrism after macro cycle:** After **world game**, the next **finance** tile may be **British/imperial** institutional design—not **US-only**—before **America’s Game** lands (prefix round 5: **H2 partial**).

## Changelog (appendix)

| Date | Change |
|------|--------|
| 2026-04-07 | Scaffold: empty appendix; chain not started. |
| 2026-04-07 | **v0.2 merge:** Populated heuristics M3–M18 from Volume IV backtest log `lecture-forward-chain-gt-01-18.md`. |
| 2026-04-07 | **v0.3:** Mechanical blind enforced via `scripts/work_jiang/forward_chain_blind_bundle.py`; retrospective chain remains priors only until re-run blind. |
| 2026-04-08 | **v0.4 merge:** Heuristics 13–15 + failure-mode tweak; full blind chain logged (see BLIND.md). |
| 2026-04-08 | **v0.4.1 (skill note):** Closed loop = prior **Adjustment** feeds next round; batch `run_blind_chain_rounds.py` not calibration. |
| 2026-04-08 | **v0.4.2:** `forward_chain_blind_bundle.py` **advance** + **`bundle --closed-loop`** gate (state file + non-empty series model); **`--force`** bypass. |
| 2026-04-06 | **v0.4.3 merge:** Closed-loop replay **gt-04 … gt-18** executed + BLIND **Replay** subsections + JSONL `replay` tail; runner/inject scripts under `scripts/work_jiang/`. |
| 2026-04-06 | **v0.4.4 (skill):** Agent invariants — prefix-only predictions; explicit **oracle/smoke** labeling; rule `skill-jiang-closed-loop.mdc`. |
| 2026-04-06 | **v0.5.0 (skill):** Canonical calibration = **`lecture-forward-chain-gt-BLIND-prefix-only.md`** + **`lecture-forward-chain-blind-prefix-only.jsonl`**; historical BLIND quarantined; **`advance --reset`**. Appendix heuristics refreshed from **prefix-only** log at cadence. |
| 2026-04-06 | **v0.5.1 merge:** Post–gt-18 distillation from **prefix-only** BLIND (rounds 1–17 complete); primary-source banner + historical bullet 14 rewrite; failure mode **US-centrism after macro cycle**; heuristics 1–12 treated as **re-validated** against prefix-only scores (cadence 3/6/9/12/15 folded into this pass). |
