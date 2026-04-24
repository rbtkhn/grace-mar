# ALIGNMENT — companion-self · grace-mar · Cici’s companion / instance (external)

**Goal:** One **Identity Fork Protocol**, one **canonical path** layout under `users/<id>/` in **each** instance repo, and **no** copying grace-mar’s Record into another companion’s tree.

| Layer | companion-self (template) | grace-mar (this repo) | Cici’s instance (`companion-xavier` or her chosen repo) |
|-------|---------------------------|------------------------|-----------------------------------------------|
| Role | Blueprint | Reference instance `users/grace-mar/` + **work-cici** advisor module | Her fork — **`users/xavier/`** (or template ID) **in her repository** |
| Record | `users/_template/` scaffold only | Live grace-mar Record | Her Record — **hosted outside** grace-mar |

**grace-mar:** Operator runs the **work-cici** project (this folder) to advise Xavier; mirrors and runbooks live here.

**Xavier:** Clones / works in **her** repo; seed survey, gate, and exports are **there**.

See also: [audit-structural-alignment-grace-mar-companion-self.md](../../audit-structural-alignment-grace-mar-companion-self.md), [TEMPLATE-BASELINE.md (pointer)](TEMPLATE-BASELINE.md), [MERGING-FROM-COMPANION-SELF](../../merging-from-companion-self.md).

If you use **Open Brain**–style capture + MCP + vector search, read [companion-self-for-open-brain-users.md](../work-companion-self/companion-self-for-open-brain-users.md) before mapping tooling to the Record. **Wired in work-cici:** [xavier-instance-two-step.md](xavier-instance-two-step.md) (tooling box), [first-good-morning-runbook.md](first-good-morning-runbook.md) (operator note + checklist **5b**), [SESSION-0-OPERATOR.md](SESSION-0-OPERATOR.md) (step **2a**), [LEAKAGE-CHECKLIST.md](LEAKAGE-CHECKLIST.md).

## OB1 vs Cici (development frontier)

**OB1** (upstream) is the **shared memory substrate**—Supabase, pgvector, MCP, and the contribution ecosystem around the core **thoughts** runtime; product evolution there stays **platform-shaped** (protocol, retrieval, extensions), not a personal cognitive-fork Record. **[Cici](https://github.com/Xavier-x01/Cici)** is **Xavier’s instance layer** on that substrate: **config and docs in git**, optional **bridges**, and Phase 1 **git-first governed state** (evidence → prepared context → governed state, **proposals**, **authority-map**, CI validation). The frontier between them is **where durable instance truth is authored**: OB1 assumes the **database** as the natural home for captured thoughts; Cici’s doctrine pushes **reviewable, versioned files** as canonical when git and Supabase disagree, with Supabase as **operational bridge** (search, MCP), not the sole source of identity truth. Full stack roles table: [OB1 mapping § Conceptual map](../../integrations/ob1/mapping.md#conceptual-map-ob1-cici-grace-mar).
