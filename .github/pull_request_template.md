## Summary

<!-- What does this PR change and why? -->

## Lane declaration (required for CI)

**Add a GitHub label** on this PR so lane-scope checks pass:

| Your change | Label to add |
|------------|----------------|
| work-dev integration (OpenClaw, handback, work-dev docs/scripts) | `lane/work-dev` |
| work-jiang research lane | `lane/work-jiang` |
| companion Record / users / bot prompt | `lane/companion-record` |
| work-politics scripts/docs | `lane/work-politics` |
| work-companion-xavier docs | `lane/work-companion-xavier` |
| repo infra (workflows, pyproject, broad tooling) | `lane/infra` |

Use **exactly one** primary lane label above.

If the diff **intentionally crosses lanes**, also add **`lane/cross`** and fill the justification block below (non-empty fenced block required).

## Lane declaration (human-readable)

- [ ] This PR is **work-dev** only — label `lane/work-dev`
- [ ] This PR is **work-jiang** only — label `lane/work-jiang`
- [ ] This PR is **companion-record** / **work-politics** / **infra** / **work-companion-xavier** only — matching `lane/...`
- [ ] This PR **intentionally crosses lanes** — labels `lane/cross` + one primary `lane/...` + justification below

### Cross-lane justification

<!-- Required when `lane/cross` is set: non-empty body or CI fails. -->

```text


```

## Checklist

- [ ] Tests / validation run locally where relevant
- [ ] Docs updated if behavior or operator workflow changed
