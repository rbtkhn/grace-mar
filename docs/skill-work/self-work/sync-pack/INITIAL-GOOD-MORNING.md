# Initial coffee process (template)

Use this sequence for a new instance bootstrapping from `companion-self`.

All steps are optional except where already established in the instance.

---

## Sequence

1. **Template alignment check (optional)**
   - Compare local sync surfaces against canonical upstream template (`companion-self` repo + chosen ref).
   - Output: `aligned` / `minor drift` / `major drift`.

2. **work-dev sync check (optional, if established)**
   - Run relevance/sync check only if a `work-dev` mirror/sync contract already exists for the instance.
   - Output:
     - sync status
     - top relevant updates (if any)
     - **next step suggestions** (1-3 concrete actions)

3. **work-business sync check (optional, if established)**
   - Run relevance/sync check only if a `work-business` mirror/sync contract already exists for the instance.
   - Output:
     - sync status
     - top relevant updates (if any)
     - **next step suggestions** (1-3 concrete actions)

---

## Suggested output block

```md
### Initial coffee sync summary
- Template alignment: <aligned/minor drift/major drift>
- work-dev sync: <not established/no relevant updates/relevant updates found>
- work-dev next steps:
  - <action 1>
- work-business sync: <not established/no relevant updates/relevant updates found>
- work-business next steps:
  - <action 1>
```

---

## Safety

- Keep sync writes in WORK mirror surfaces only.
- Do not write identity truth files directly.
- Stage identity implications via gate flow.

