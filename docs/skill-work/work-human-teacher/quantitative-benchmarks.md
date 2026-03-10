# Quantitative Benchmarks — work-human-teacher

Benchmarks to track personalized growth, engagement, formative loop health, and edge progression. Emphasizes Record evolution and lesson-related pipeline activity over economic outcomes.

---

## Priority Six (instrument first)

| Metric | Description | Source |
|--------|-------------|--------|
| **IX growth per week** | IX-A/B/C entries merged per week | self.md evolution log |
| **Evidence rate** | ACT-*, WRITE-*, CREATE-* entries per week | self-evidence.md |
| **Lesson-sourced merge rate** | Approved / total lesson-sourced candidates | recursion-gate.md |
| **Handback → merge latency** | Days from "we did X" stage to merge | recursion-gate.md, pipeline-events |
| **Skill-think level changes per quarter** | READ/MATH/CHINESE level upgrades | skills.md, skill-think.md |
| **Regeneration frequency** | Lesson prompts generated per week | Generator logs (add instrumentation) |

---

## Full Benchmark Set

### Record growth

| Metric | Description | Source |
|--------|-------------|--------|
| IX growth per week | IX-A/B/C entries merged per week | self.md evolution log |
| Evidence rate | ACT-*, WRITE-*, CREATE-* entries per week | self-evidence.md |
| Activity mix | Ratio of WRITE vs CREATE vs ACT (curated observation) | self-evidence.md |
| Lookup approval rate | Knowledge lookups approved / total requested | recursion-gate.md, ACT entries |

### Pipeline health (lesson-related)

| Metric | Description | Source |
|--------|-------------|--------|
| Lesson-sourced candidates per week | Candidates staged from "we did X" (lesson/transcript handback) | recursion-gate.md (metadata: source: lesson) |
| Merge rate (lesson-sourced) | Approved / total lesson-sourced candidates | recursion-gate.md |
| Time in gate (lesson-sourced) | Days from stage to approve/reject | recursion-gate.md timestamps |
| Rejection rate (lesson-sourced) | Rejected / total lesson-sourced | recursion-gate.md |

### Formative loop

| Metric | Description | Source |
|--------|-------------|--------|
| Regeneration frequency | Lesson prompts generated per week | Generator logs (add instrumentation) |
| Post-merge regeneration rate | Generator run within N days of merge | Pipeline events + generator logs |
| Handback → merge latency | Days from "we did X" stage to merge | recursion-gate.md, pipeline-events |
| Sessions with handback per week | Lesson-related "we did X" reports per week | pipeline-events.jsonl |

### Edge progression

| Metric | Description | Source |
|--------|-------------|--------|
| Skill-think level changes | READ/MATH/CHINESE level upgrades per quarter | skills.md, skill-think.md |
| Edge advancement | New edges crossed (e.g., phonetic spelling → conventional) | skills.md evolution |
| Container activation | THINK/WRITE/BUILD status (active vs seed) | skills.md |

### Engagement proxies

| Metric | Description | Source |
|--------|-------------|--------|
| Evidence diversity | Distinct activity types per month (WRITE, CREATE, ACT, lookup) | self-evidence.md |
| Curiosity uptake | IX-B entries merged per month | self.md IX-B |
| Lexile trajectory | Writing sample Lexile over time (if analyzed) | WRITE evidence, scripts |
| Wisdom-question responses | Count of wisdom questions answered in bot | session-transcript, self-archive.md |

### Generator usage

| Metric | Description | Source |
|--------|-------------|--------|
| Prompts generated per week | Generator invocations | Generator logs (add instrumentation) |
| Focus distribution | `--focus reading|math|work|integrated` usage | Generator logs |
| Alpha-school flag usage | `--alpha-school` invocations when available | Generator logs |

### Alpha-school alignment (when `--alpha-school` is used)

| Metric | Description | Source |
|--------|-------------|--------|
| Screen time adherence | Session duration vs 2-hour target | Session logs, handback metadata |
| Block composition | Segment length and count per session | Structured handback |
| Mastery threshold hits | In-session success rate vs 90% target | Structured handback (requires format) |

---

## Instrumentation Notes

- **recursion-gate.md** — Add `source: lesson` (or `source: transcript_handback`) to candidates staged from lesson "we did X" or transcript paste so lesson-sourced metrics can be filtered.
- **generate_lesson_prompt.py** — Add optional `--log` or emit events to record: timestamp, `--focus`, `--alpha-school`, `-u` user. Write to `pipeline-events.jsonl` or a dedicated `lesson-generator-events.jsonl`.
- **Aggregation script** — Optional: `scripts/human_teacher_benchmarks.py` to summarize IX growth, evidence rate, lesson-sourced merge rate, handback latency, skill-think changes from the above sources.
