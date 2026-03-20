# CMC Routing

**Purpose:** Decide when to query Civilization Memory Codex vs. skip to full LLM lookup.

**Registry:** CIV-MEM routing is declared as domain `civ_mem` in [self-library-domains.md](self-library-domains.md) / [self-library-domains.json](self-library-domains.json). Validators require this domain to be present.

## Routing contract (identity vs reference)

- **CMC hits are reference retrieval** — answers come from material catalogued under the **CIV-MEM** subdomain of **SELF-LIBRARY** (LIB rows + codex), not from `self.md`.
- **CMC retrieval is not an identity update** — codex text does not become SELF-KNOWLEDGE until separately merged through the gate into IX-A (if ever).
- **Internal CIV-MEM** lives under **SELF-LIBRARY** (`self-library.md`, hybrid corpus paths) — see [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md).

**Ontology (summary):** **routing to CMC** = routing into the **CIV-MEM domain of SELF-LIBRARY**, **not** into SELF or SELF-KNOWLEDGE.

## Flow

```
SELF-LIBRARY (LIB entries) → miss
    │
    ▼
should_route_to_cmc(question)?
    │
    ├── No  → full LLM lookup (skip CMC subprocess)
    │
    └── Yes → query_cmc(question) → hit? → REPHRASE : full lookup
```

## Combined Routing Logic

**Ontology (repeat):** A CMC hit is **CIV-MEM / SELF-LIBRARY reference retrieval** — not an update to SELF or SELF-KNOWLEDGE. The Voice may *say* what the codex returns; that content is **not** identity until separately gated into SELF.

Three layers work together:

### 1. Negative triggers (skip first)

If the question matches any negative trigger, **never** route to CMC:

- **Phrases:** "how do you spell", "how to spell", "what's the spelling", "spell the word"
- **Words:** spell, spelling, math, maths, arithmetic, add, subtract, multiply, divide, calculator, equation, formula

### 2. Strong terms (civilization/region + US history, classical music, ballet)

One match → route to CMC. Includes civilization/region names and high-value historical/cultural terms:

- **Civilizations:** rome, roman, romans, china, chinese, greece, greek, greeks, egypt, egyptian
- persia, persian, india, indian, russia, russian, anglia, britain, british
- england, english, mongol, ottoman, byzantine, islam, islamic, french, france
- germany, german, africa, african, maya, mayan, aztec, inca, mesopotamia, babylon
- **US history:** america, american, americans
- **Central Europe / classical music:** austria, austrian, vienna
- **High-value figures/works:** lincoln, nutcracker, tchaikovsky, schubert, ballet, president, presidents

### 3. Weak terms (historical concepts)

Concepts alone are ambiguous ("history of Pokemon"). Route only when **2+ weak terms** match:

- ancient, dynasty, emperor, empress, empire, empires, civilization, civilizations
- conquest, war, treaty, medieval, renaissance, colonial, revolution
- strategy, political, politics, culture, pharaoh, pharaohs, aqueduct, aqueducts
- composer, composers, symphony

**Examples:**
- "What did the Romans use aqueducts for?" → strong (romans) → route ✓
- "how do you spell elephant" → negative (spell) → skip ✓
- "history of Pokemon" → 1 weak (history) → skip ✓
- "ancient Egyptian pharaohs" → strong (egyptian) → route ✓
- "Who was Abraham Lincoln?" → strong (lincoln) → route ✓
- "What is the Nutcracker ballet?" → strong (nutcracker) → route ✓
- "Who was Schubert?" → strong (schubert) → route ✓
- "Who were the US presidents?" → strong (presidents, american) → route ✓

## Rationale

- **Negative triggers:** Avoid CMC for spelling, math, generic science.
- **Strong terms:** Civilizations map directly to CMC content.
- **Weak-only gate:** Prevents broad terms like "history" from routing non-civilizational questions.

## Override

For testing or special cases, `query_cmc(question, skip_routing=True)` bypasses the routing check.
