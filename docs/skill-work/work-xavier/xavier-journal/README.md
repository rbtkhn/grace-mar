# Xavier journal — Open Brain (OB1) learning log

**Book:** Daily notes on **learning and building** Xavier’s **Open Brain** stack: **instance** ([`Cici`](https://github.com/Xavier-x01/Cici)), upstream ([NateBJones-Projects/OB1](https://github.com/NateBJones-Projects/OB1)), and how that ties to **BrewMind** work.

**Discoverability:** The same tree is linked from **`users/grace-mar/SELF-LIBRARY/xavier-journal`** (repo-relative symlink) for agents and tools that prioritize the companion tree. **LIB:** [LIB-0154](../../../../users/grace-mar/self-library.md#operator-analytical-books) in [`self-library.md`](../../../../users/grace-mar/self-library.md) (Operator analytical books).

**Territory:** `docs/skill-work/work-xavier/xavier-journal/` in grace-mar — **WORK / operator coaching**, not Xavier’s **Record**, not companion Voice knowledge.

**How to use**

- One file per calendar day you want to capture: `YYYY-MM-DD-day-NN.md` (NN = journal day number from her OB start).
- Keep entries **short** (10–20 lines): focus, actions, wins, blockers, one line for tomorrow.
- **No secrets** (API keys, Supabase URLs with keys, MCP keys). Point to env vars and dashboards in prose only.

**Daily synthesis from her OB1 GitHub repo**

Canonical OB1 instance repo: **[github.com/Xavier-x01/Cici](https://github.com/Xavier-x01/Cici)** (`main`).

Each day, generate a starter entry that **pulls commits for that calendar day** (GitHub API) and drops them under **OB1 repo activity (synthesized from GitHub)**. You still add narrative in **Focus**, **What I did today**, etc.—git is only the **spine**.

From repo root:

```bash
# Preview today (UTC calendar day); journal day number is inferred from existing *-day-NN.md files
python3 scripts/xavier_journal_ob1_digest.py

# Local calendar day (example): Eastern time
TZ=America/New_York python3 scripts/xavier_journal_ob1_digest.py

# Write the file (refuses to overwrite unless --force)
python3 scripts/xavier_journal_ob1_digest.py --write
```

Optional: set **`GITHUB_TOKEN`** (or `GH_TOKEN`) for higher API rate limits; public repo works without auth for light use.

Optional automation: same command on a **cron** or end-of-day **operator** ritual—there is no server-side hook from GitHub into grace-mar by default.

**`dream` ritual:** End-of-day **`dream`** is the canonical time to **generate today’s** journal file if missing — run `xavier_journal_ob1_digest.py --write` with your chosen `TZ` (see [.cursor/skills/dream/SKILL.md](../../../../.cursor/skills/dream/SKILL.md) § *Xavier journal*). This does not run inside `auto_dream.py`; the agent performs it when executing the full dream skill. If the day file already exists, the script refuses overwrite unless `--force`.

**Upstream:** Open Brain docs and recipes live in the OB1 ecosystem; this journal is **her** trajectory in grace-mar, not a fork of upstream text.

**vs [work-xavier-history.md](../work-xavier-history.md):** History = **append-only milestones** (what shipped, paths, same-day `###` blocks). Journal = **optional** day file when reflection helps — do **not** duplicate full milestone lists in the journal; one line “see history 2026-04-08” is enough.
