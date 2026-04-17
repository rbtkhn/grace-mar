# Portability review checklist

Review supplement for candidates with `territory: portable-working-identity`. This does **not** replace the standard merge checklist in `recursion-gate.md` — it adds portability-specific questions that help the companion decide whether an externally extracted claim belongs in the Record.

---

## Before approving each candidate

| # | Question | Why it matters |
|---|----------|----------------|
| 1 | **Is this claim accurate** based on your actual working patterns? | External AI extracts are inferences, not ground truth. Reject what doesn't match reality. |
| 2 | **Is it durable** enough to preserve (`stable` / `recurring`), or just temporary residue? | Ephemeral habits shouldn't enter the Record unless they reveal something persistent underneath. |
| 3 | **Does it contain sensitive or employer-bound content?** | Proprietary processes, internal tooling names, or employer IP must not enter a portable Record. |
| 4 | **Is it portable** across tools and roles, or locked to a specific context? | Claims that only apply to one codebase or one employer are `role_specific` or `employer_bound`, not `cross_tool`. |
| 5 | **Is the proposed target surface correct?** | Domain knowledge → SELF-LIBRARY. Workflows → SKILLS. Behavioral patterns → SELF. Artifact evidence → EVIDENCE. Misplaced candidates lose value. |
| 6 | **Should it be exportable by default or internal-only?** | Some patterns are real but private (e.g. anxiety responses, health-related work rhythms). Mark `non_portable` if appropriate. |

---

## Decision options

| Decision | When to use |
|----------|-------------|
| **Approve** | Claim is accurate, durable, portable, and correctly surfaced |
| **Reject** | Claim is inaccurate, ephemeral, sensitive, or not worth preserving |
| **Approve with abstraction** | The underlying pattern is real, but the claim needs rewording to remove specifics (employer names, project details) |
| **Route to different surface** | Claim is valid but the proposed target surface is wrong — approve and redirect |

---

## Sensitivity quick reference

| `sensitivity_class` | Meaning |
|----------------------|---------|
| `safe` | No sensitive content; can be exported freely |
| `review_required` | Default for imports; companion must evaluate before approving |
| `non_portable` | Contains employer-bound or private content; reject or abstract before approving |

## Portability quick reference

| `portability_class` | Meaning |
|----------------------|---------|
| `cross_tool` | Works across any tool or role |
| `role_specific` | Tied to a particular role but not a particular employer |
| `employer_bound` | Contains employer-specific knowledge |
| `non_exportable` | Should not leave the Record in any export |

---

## Related

- [import-external-working-identity.md](import-external-working-identity.md) — how candidates are imported
- [promotion-rules.md](promotion-rules.md) — where approved candidates land
- [working-identity-candidates.md](working-identity-candidates.md) — candidate schema and lifecycle
