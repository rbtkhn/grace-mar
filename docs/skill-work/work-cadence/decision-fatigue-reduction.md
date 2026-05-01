# Decision fatigue reduction

**Status:** WORK-layer operator doctrine. Not Record truth, not a gate path, not automation authority.

**Purpose:** Reduce repeated re-routing while preserving explicit human approval. The system may recommend a default next move, but the operator still chooses whether to accept, redirect, or stop.

---

## Terms

| Term | Meaning |
|------|---------|
| **Route menu** | A menu whose job is to pick a territory or mode of attention, such as the `coffee` hub. |
| **Action menu** | A menu whose job is to pick a concrete next move after the route is known, such as a Conductor Action Menu. |
| **Recommended default** | The assistant's best current pick from a visible menu, grounded in the current script output, lane state, or recent rhythm. |
| **Accept default** | An operator reply such as `go`, `default`, `yes`, `sounds good`, or equivalent agreement after a recommended default was named in the current turn. |

---

## Rules

1. **Menus route attention.** Use menus to choose a lane, conductor stance, or action path; do not use them to keep reopening the same decision.
2. **Once routed, recommend one next move.** When evidence is strong enough, name a single recommended default rather than presenting every branch as equally weighted.
3. **One submenu is enough.** After one follow-up submenu, the next assistant turn should either execute the selected item, recommend the default, or report the blocker.
4. **Off-menu remains meaningful.** If the operator replies outside the visible options, treat that as refusal, park, redirect, or new instruction. Do not spend a menu option on refusal.
5. **Defaults are not authority.** A recommended default is decision support only. It does not approve gate candidates, create lanes, spend money, publish, merge, or modify the Record.

---

## Chat shape

When a menu has a strong default, use one short line near the menu:

```text
Recommended default: C - say "go" to accept, or pick another hub letter.
```

For action menus, use the same shape with the local letter set:

```text
Recommended default: B - highest evidence-to-effort ratio in this pass.
```

Only use `go` / `default` / `yes` / `sounds good` as acceptance when the current turn explicitly named a recommended default. Otherwise interpret those replies in normal conversational context.

---

## Boundaries

- Keep fixed menu shapes fixed: `coffee` remains A-E; Conductor Action Menu remains A-C.
- Durable logs should keep using stable identifiers: conductor slugs, file paths, lane names, candidate IDs, or script output labels. Menu letters are UI conveniences.
- Gate and Record behavior is unchanged. Any Record promotion still requires the normal staged and approved path.
- Continuity dashboards may surface as a single warning line in `coffee` or `dream`; they should stay silent when `ok` and must not expand into another menu.
