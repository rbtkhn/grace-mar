# Agent Encoding — Phase 1

**Purpose:** Reference material for Grace-Mar when acting as agent manager of Grace Gems (message assist, listing validation). Companion-approved; knowledge boundary applies. Agent proposes; companion approves.

**Phase 1 scope:** Provenance–stone table, terminology glossary, meta-rules for drafts. See [roadmap](roadmap.md) for phases.

**Source:** Pre-1970 jewelry industry research ([jewelry-industry-research-pre1970.md](jewelry-industry-research-pre1970.md)); Wade (1918), Shipley (1948), Smith (1958).

---

## 1. Provenance–Stone Table

Use for listing validation, provenance copy, and message drafts. Flag when stone + provenance are inconsistent.

| Stone | Valid provenance regions | Notes |
|-------|--------------------------|-------|
| **Ruby** | Burma (Upper Burma), Thailand, Ceylon (Sri Lanka), Mozambique | Burma: finest historically (Wade 1918) |
| **Sapphire** | Ceylon (Sri Lanka), Kashmir, Burma, Thailand, Australia | Ceylon: sapphires, moonstone |
| **Emerald** | Colombia (Muzo, Chivor), Zambia, Egypt (historical), Russia (Ural) | Colombia: Muzo, Chivor historically finest |
| **Diamond** | South Africa, Brazil, India, Australia | Kimberley, river diggings |
| **Opal** | Australia (black opals, New South Wales), Hungary, Mexico (fire opal) | Australia: black opals, NSW |
| **Moonstone** | Ceylon (Sri Lanka) | Often recut in West for grain alignment |
| **Topaz** | Brazil, Sri Lanka, Russia (Ural), Arizona | Brazil: imperial, blue |
| **Tourmaline** | Brazil, Ceylon, Burma, Mozambique, Madagascar | Various colors by locality |
| **Amethyst** | Siberia, Uruguay, Brazil | Siberia: deep red component |
| **Peridot** | St. John's Island (Red Sea), Arizona, Burma, Queensland | Chrysolite |
| **Turquoise** | Persia (Khorasan), New Mexico, Arizona, Nevada, California | Persia: finest blue |
| **Garnet** | India, Sri Lanka, South Africa, Russia, Madagascar | Almandine, pyrope, spessartine |
| **Tanzanite** | Tanzania | Discovered 1967 |
| **Jade (nephrite)** | China, Siberia, New Zealand | |
| **Jadeite** | Burma (Upper Burma), China, Tibet | Burma: best historically |
| **Lapis lazuli** | Afghanistan, Siberia, Chile | |
| **Citrine** | Brazil, Spain (heated smoky quartz) | Golden quartz |

**Validation rule:** If a listing or message claims stone X from region Y, check that Y appears in the valid provenance row for X. If not, flag for review.

---

## 2. Terminology Glossary

Use for listing copy and message drafts. Ensure terms match the stone/cut form. Flag misuse.

### Cut forms

| Term | Definition |
|------|------------|
| **Cabochon** | Rounded top, flat or slightly convex base. French *caboche* (bald head). Best thickness ~half the spread for total reflection. Oldest cut form. |
| **Rose cut** | Facets on rounded top; 24 triangular facets; thickness ~half diameter. |
| **Brilliant** | Standard for diamond; round with 32 top facets, 24 back facets + culet. Colored stones: ~39° top, ~44° back for brilliancy. |
| **Step cut** | Rectangular facets; deeper color. Includes emerald cut. |

### Weights and metals

| Term | Definition |
|------|------------|
| **Carat** | Unit of weight for precious stones. Standardized; use for gem weight. |
| **14k, 18k** | Gold purity: 14/24 or 18/24 parts gold. Grace Gems: solid 14k/18k. |

### Treatments and authenticity

| Term | Definition |
|------|------------|
| **Untreated** | No heat, irradiation, or other enhancement. Grace Gems: natural, untreated gemstones. |
| **Natural** | Formed in nature; not lab-grown or synthetic. |
| **Lab-grown / synthetic** | Chemically identical to natural but man-made. Grace Gems: not offered. |
| **Imitation** | Glass, paste; differs in composition. Grace Gems: not used. |

### Other

| Term | Definition |
|------|------------|
| **Provenance** | Geographic origin of a stone. |
| **Handmade** | Fabricated by hand; not mass-produced. Grace Gems: handmade in Denver. |
| **Custom** | Made to order; personalized. |
| **Bridal set** | Matching engagement ring + wedding band. |

**Validation rule:** If copy uses "rose cut" for a brilliant, or "cabochon" for a faceted stone, flag for review.

---

## 3. Meta-Rules for Drafts

Apply when drafting messages, listing copy, or FAQ responses. Agent uses these; companion approves final text.

### Identification hierarchy (Wade 1918)

- **Numerical properties over color** — Prefer verifiable claims (refraction, specific gravity, hardness, lab cert) over subjective description ("it looks blue").
- **Concrete facts** — "We verify by [X, Y, Z]" or "Lab-certified when [condition]" — not vague authenticity claims.
- **No guessing** — Use only documented Grace Gems policies and practices. Do not invent verification methods.

### Educational selling rule (Wade 1918)

- **One concrete fact per touchpoint** — Each message or listing excerpt should include at least one verifiable fact: provenance, treatment status, metal purity, or policy.
- **Match customer knowledge** — "The buying public" is increasingly informed; drafts should be at least as accurate as what an informed customer expects.
- **Application in salesmanship** — Integrating gemological facts into customer touchpoints builds trust and supports sales.

### Knowledge boundary

- **Record only** — Use only documented Record content (SELF, business profile, policies) for business facts.
- **No inference** — Do not invent policies, provenance, or verification methods.
- **Flag when uncertain** — If a draft requires a fact not in the Record, flag for companion to add or approve.

### Tone / voice guidelines (Lazar: design matters)

- **Friendly, accurate, simple** — Warm and helpful; no stiff or corporate language.
- **Natural, not templated** — Sound human; avoid robotic phrases.
- **One concrete fact per reply** — Provenance, policy, treatment status, metal — not filler.
- **Match customer tone** — If they're casual, respond casually; if formal, stay professional but warm.

---

## 4. Handback Semantics

*Wu insight: encode tribal knowledge so the agent knows when to stage vs. draft vs. flag.*

### When to stage vs. draft vs. flag

| Situation | Action | Example |
|-----------|--------|---------|
| Etsy order fulfilled, review received | **Stage** candidate for RECURSION-GATE | "We fulfilled order #1234" → stage ACT-XXXX |
| Customer message needs reply | **Draft** reply; human sends | Message assist produces draft; operator copies into Etsy |
| Listing has stone + provenance mismatch | **Flag** for review | Ruby + "Australia" → flag (Burma, Thailand, Ceylon, Mozambique valid) |
| New listing added | **Stage** candidate | "We added listing: [title]" → stage for EVIDENCE |
| Customer asks about authenticity | **Draft** reply using identification hierarchy | Use provenance, treatment status, lab cert if applicable |
| Unknown policy question | **Flag** — fact not in Record | Do not invent; flag for companion to add |

### One-task semantics (Lazar: token window, clarity)

- **Message assist** — One customer message per run. Do not batch multiple messages in one prompt.
- **Listing validation** — One listing per run. Do not validate multiple listings in one prompt.
- **Etsy handback** — One event type per staging step (e.g. one order, one review).
- **Rationale** — Keeps context small; agent stays focused; avoids token overload.

### Context assembly for message-assist

1. **Load** — agent-encoding.md (meta-rules, glossary, tone guidelines), Grace Gems README in work-business/grace-gems (policies), [message-assist-calibration.md](message-assist-calibration.md) if present.
2. **Include** — Provenance table if message mentions a stone; care-by-stone (Phase 2) if message asks about care.
3. **Exclude** — Anything not documented in Record. No LLM inference.
4. **Output** — Draft reply only; no preamble. Human copies and sends.

### "We did X" patterns for Etsy events

| Event | Pattern | Target |
|-------|---------|--------|
| Order fulfilled | "We fulfilled order #1234" | ACT-XXXX, EVIDENCE |
| Review received | "We got a 5-star review from [buyer]" | ACT-XXXX, EVIDENCE |
| New listing | "We added listing: [title]" | CREATE-XXXX or ACT-XXXX |
| Custom order completed | "We completed custom order for [item]" | ACT-XXXX |
| Sale milestone | "We hit 2,000 sales" | ACT-XXXX |
| Feedback | "Customer asked about [topic]; we replied with [summary]" | ACT-XXXX (optional) |

*Companion approves merge; agent stages only.*

---

## 5. Example Drafts (Exposure to Quality)

*Lazar: expose agent to what good looks like. Use these as reference for message-assist calibration.*

### Shipping (e.g. "Do you ship to Canada?")

> Yes! We offer free worldwide shipping. Your order will ship from Denver within 2–3 weeks. Tracking is included.

### Authenticity (e.g. "Is this stone natural or lab-grown?")

> All our gemstones are 100% natural and untreated. We source from trusted suppliers (Sri Lanka, Mozambique, Colombia, etc.). If you’d like lab certification for a specific piece, we can arrange that for an additional fee.

### Layaway / payment

> We offer layaway — typically 30% down, with the remainder due over a few weeks. Let me know which item you’re interested in and I can set up a private listing for you.

*Use only documented policies. Tone: friendly, accurate, one concrete fact per reply.*

---

## 6. Usage

| Agent use case | Reference |
|----------------|-----------|
| Message assist (draft reply) | Provenance table, glossary, meta-rules, §4 context assembly |
| Listing validation | Provenance table, glossary, §4 stage vs. flag |
| Etsy handback | §4 "We did X" patterns |
| FAQ / authenticity | Identification hierarchy, educational selling rule |
| Care instructions | *(Phase 2: care-by-stone)* |

---

## 7. Maintenance

- Companion approves changes. No autonomous edits.
- Provenance table: add regions only when companion documents new sourcing.
- Glossary: extend when new terms enter Grace Gems vocabulary.
- Meta-rules: update only with companion approval.

---

*Last updated: 2026-02-27. §3 tone guidelines, §4 one-task semantics, §5 example drafts, message-assist-calibration loop (Lazar + Wu insights).*
