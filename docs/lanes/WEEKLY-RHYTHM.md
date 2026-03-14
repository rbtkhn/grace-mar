# Weekly rhythm — operator checklist

Run **once per week** (e.g. same calendar slot). Tick what you did; skip lanes that were dormant.

| # | Lane | Action | Done |
|---|------|--------|------|
| 1 | **Record** | Open `recursion-gate.md` — pending count 0 or explicit decisions (approve / reject / defer) | ☐ |
| 2 | **Record** | If companion had Voice milestones: stage or note **doc-only this week** (README WPC rhythm idea) | ☐ |
| 3 | **WPC** | Refresh [brief-source-registry](../skill-work/work-political-consulting/brief-source-registry.md); run brief generator + **§0 recency** live pass | ☐ |
| 4 | **WPC** | One line in head: **doc-only** vs **one WAP candidate staged** | ☐ |
| 5 | **Civ-mem** | If active: one retrieval or index sanity check; no ship without human approval | ☐ |
| 6 | **Operator** | Skim [operator-cognition.md](operator-cognition.md) north star — still true? | ☐ |
| 7 | **Repo** | `python3 scripts/harness_warmup.py -u grace-mar --compact` pasted or run | ☐ |

**Time box:** 30–90 min total; WPC brief can be the long pole.

**Integrity (when Record or prompt changed this week):**

```bash
python3 scripts/validate-integrity.py --user grace-mar
python3 scripts/export_manifest.py -u grace-mar -o users/grace-mar
python3 scripts/fork_checksum.py --manifest
```

(Or run full merge postflight if you processed the gate.)
