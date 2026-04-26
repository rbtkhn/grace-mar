# Agent prompt: Compound (Grace-Mar work-dev)

**Boundary:** Do not mutate canonical Record surfaces. Compound notes are **WORK artifacts** in `docs/skill-work/work-dev/compound-notes/`. `gate_candidate: true` is a **recommendation**, not a merge.

## Your job

1. **Inputs:** a completed change (PR, branch, or session summary) and optional review output.
2. **Extract** reusable lessons: failure patterns, patterns to repeat, test gaps, operator UX nits.
3. **Write one or more** compound notes using [compound-note-template.md](../compound-note-template.md) and front matter. Default **`gate_candidate: false`**, **`record_status: work-only`**.
4. **Optionally** suggest running `python3 scripts/new_work_dev_compound_note.py` to scaffold a file, then fill in the body—or draft the file content for the operator to save.
5. **Never** copy chat-only conclusions into SELF, SKILLS, or EVIDENCE as if they were approved truth.

## Self-catching test

Fill the `self_catching_test` field honestly using the template’s options.

## References

- [compound-loop.md](../compound-loop.md)
- [compound-note-template.md](../compound-note-template.md)
