# Jiang compressions

**Operator research** — compressed, high-signal snapshots of work artifacts from the [work-jiang](../README.md) lane.

Each JSON file under this directory should:

- Pass the **compression checklist** in `python3 scripts/jiang-compress.py` (operator y/N — not the same as companion approval in `recursion-gate.md`).
- Declare a **category**: `operational` | `analytical` | `synthesis` | `other`.
- Include **executable next actions** (1–3) and **linked evidence** strings (paths, ACT/READ ids, or doc references).
- Stay **small**: aim for the full serialized JSON under **~800 characters** when practical (see [`../schemas/jiang-compression-v1.schema.json`](../schemas/jiang-compression-v1.schema.json) `maxSerializedChars`).

**Membrane:** These files are not SELF or EVIDENCE. Anything that should become Record truth must go through **RECURSION-GATE** and approval.

**Create:** `python3 scripts/jiang-compress.py -u <fork-id>`  
**Doc:** [docs/skill-work/work-jiang/COMPRESSION-ENGINE.md](../../../../docs/skill-work/work-jiang/COMPRESSION-ENGINE.md)
