# Reviewer matrix (compact)

**Purpose:** One structured review pass with **seven lenses**—not seven separate sub-agents. Use in [review](agent-prompts/review.md) and [compound](agent-prompts/compound.md) prompts.

**Global promotion rule (all reviewers):** A reviewer may **recommend** a compound note, a follow-up PR, or flag `gate_candidate`—and must **not** directly edit SELF, SKILLS, EVIDENCE, Library, or other durable Record surfaces.

| Reviewer | Scope | Questions (examples) | Failure modes | Output format | Promotion rule |
|----------|--------|----------------------|---------------|---------------|----------------|
| **1. Boundary Reviewer** | Record vs WORK; path placement; authority language | Does this change imply Record write or merge? Does it stay under allowed paths? | Covert SELF/EVIDENCE edits; `recursion-gate` language without staging | Findings: `boundary_ok` / `boundary_risk` + bullets | If risk: recommend compound note + **no** direct Record edit; `gate_candidate` only if a governed change is truly needed. |
| **2. Governance Reviewer** | Recursion-gate, skills, policy alignment | Is this change aligned with [AGENTS.md](../../../AGENTS.md) / territory rules? Any bypass of approval? | Silent policy drift; “temporary” hardcoded secrets | `governance_ok` / `governance_risk` + bullets | Recommend follow-up doc or PR; `gate_candidate` for policy-sensitive merges only with explicit rationale. |
| **3. Implementation Reviewer** | Code shape, dependencies, size of diff | Is the change minimal? Correct abstraction? Reuse? | Over-engineering; drive-by refactors | `impl_pass` / `impl_nits` + bullets | Recommend refactors or split PRs; compound note for recurring patterns. |
| **4. Test Reviewer** | Tests, coverage, flakiness | Are there tests or justified absence? Do tests assert behavior not trivia? | Missing regression for bug fix; brittle mocks | `test_ok` / `test_gap` + bullets | Recommend tests in follow-up; compound note for “self-catching test” field. |
| **5. Documentation Reviewer** | User-facing and operator docs | Are README/usage updated when behavior changes? | Stale commands; wrong paths | `docs_ok` / `docs_gap` + bullets | Recommend doc PR or compound note for operator UX. |
| **6. Operator-UX Reviewer** | Clarity, errors, run commands | Can the operator run and debug this without tribal knowledge? | Cryptic errors; missing `--help` | `ux_ok` / `ux_gap` + bullets | Compound note for friction patterns; not Record. |
| **7. Adversarial Reviewer** | Abuse, dual-use, exfil, prompt injection (where relevant) | What breaks if the tool is used maliciously or inputs are hostile? | Path traversal; unsafe eval | `adversary_ok` / `adversary_risk` + bullets | Escalate to governance + compound note; `gate_candidate` only for serious security governance items. |

**Consolidation:** Merge all tables into a single review artifact (comment, compound note, or PR description)—one **Block per reviewer** with the output format line + bullets.
