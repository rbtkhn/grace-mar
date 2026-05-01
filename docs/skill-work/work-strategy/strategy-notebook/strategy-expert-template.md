# Strategy expert — templates (WORK only)
<!-- word_count: concise bundle -->

**Single source** for the six on-disk surfaces each commentator uses:
profile, thread, transcript, refined page, strategy page, and mind.

**Notebook contract:** [NOTEBOOK-CONTRACT.md](NOTEBOOK-CONTRACT.md)
**Thread contract:** [THREAD-CONTRACT.md](THREAD-CONTRACT.md)

**Jump:** [Profile](#profile-template) · [Thread](#thread-template) · [Transcript](#transcript-template) · [Refined page](#refined-page-template) · [Strategy page](#strategy-page-template) · [Mind](#mind-template)

---

<a id="profile-template"></a>

## Profile → `strategy-expert-<expert_id>.md`

# Strategy expert — <Full name> (`<expert_id>`)

WORK only; not Record.

Use the profile as the compact lane index: identity, role, pairings, voice tier, and high-level failure modes.

**Minimal shape:**

- Identity table
- Voice fingerprint / tier
- Convergence and tension sketch
- Signature mechanisms / recurrent claims
- Failure modes / drift notes
- Published sources / seed notes

Companion files: thread, transcript, refined page, strategy page, mind.

---

<a id="thread-template"></a>

## Thread → `experts/<expert_id>/<expert_id>-thread-YYYY-MM.md`

# Expert thread — `<expert_id>`

WORK only; not Record.

The thread is the month-bounded continuity surface. It keeps:

- the narrative journal for the month
- the page index for that month
- the machine extraction block

**Thread contract:** [THREAD-CONTRACT.md](THREAD-CONTRACT.md)

**Core rules:**

- Compose the month from that month’s `strategy-page` set.
- Keep the journal above the machine block.
- Keep one file per month when possible; legacy `thread.md` only while migrating.
- Use `thread-page` links to track continuity, not to duplicate page prose.

Companion files: profile, transcript, mind, and page surfaces.

---

### Thread-embedded `strategy-page` blocks

Use the `strategy-page` fence in the monthly thread file for the month’s main analytical pages. The canonical scaffold for the fence is the `Strategy page` section below.

Machine extraction lives between the `<!-- strategy-expert-thread:start -->` and `<!-- strategy-expert-thread:end -->` comments.

---

<a id="transcript-template"></a>

## Transcript → `experts/<expert_id>/transcript.md`

# Expert transcript — `<expert_id>`

WORK only; not Record.

The transcript is the 7-day rolling triage sink, not the long-form SSOT.
It may contain:

- one-line `thread:` registry entries
- short continuation paragraphs
- pointers to `raw-input/`

When the full capture already lives in `raw-input/`, the transcript can stay empty or pointer-only.

Companion files: profile, thread, mind, and refined pages.

---

<a id="refined-page-template"></a>

## Refined page → `experts/<expert_id>/<expert_id>-page-YYYY-MM-DD.md`

# Expert refined page — `<expert_id>`

WORK only; not Record.

This is the standalone analytical page shape.

**Notebook contract:** [NOTEBOOK-CONTRACT.md](NOTEBOOK-CONTRACT.md)

**Surface rules:**

- `### Verbatim` is the curated quote body from `raw-input/`
- `### Reflection` is operator analysis
- `### Predictive Outlook` is the expert's tracked predictions, status, and brief notes tied to the thread
- `### Appendix` is machinery only

Use this when the page should stand on its own outside the thread.

**Skeleton:**

```markdown
# <Expert> refined page — YYYY-MM-DD
WORK only; not Record.

**Expert:** `<expert_id>` · **Published:** YYYY-MM-DD · **Artifact:** refined page.

---

### Verbatim

### Reflection

### Predictive Outlook

---

### Appendix
```

---

<a id="strategy-page-template"></a>

## Strategy page → thread-fence page

# Expert strategy page — `<expert_id>`

WORK only; not Record.

This is the thread-embedded analytical page shape.

**Thread contract:** [THREAD-CONTRACT.md](THREAD-CONTRACT.md)

**Surface rules:**

- `### Chronicle` is the curated quote body
- `### Reflection` is operator analysis
- `### Predictive Outlook` is the expert's tracked predictions, status, and brief notes tied to the thread
- `### Appendix` is machinery only

Use this inside `experts/<expert_id>/<expert_id>-thread-YYYY-MM.md` or legacy `thread.md`.

**Skeleton:**

```markdown
<!-- strategy-page:start id="<kebab-id>" date="YYYY-MM-DD" watch="<optional-watch-slug>" -->
### Page: <human title>

### Chronicle

### Reflection

### Predictive Outlook

---

### Appendix
<!-- strategy-page:end -->
```

---

<a id="mind-template"></a>

## Mind → `strategy-expert-<expert_id>-mind.md`

# Expert mind — `<expert_id>`

WORK only; not Record.

The mind file is the long-form voice fingerprint / style map. Keep it separate from the transcript and the thread.

**Use it for:**

- longer register notes
- transcript-derived style fingerprints
- durable voice patterns

**Do not use it for:**

- literal transcript replacement
- page prose
- thread prose

Companion files: profile, thread, transcript, and page surfaces.
