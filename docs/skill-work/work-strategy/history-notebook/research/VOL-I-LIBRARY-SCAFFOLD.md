# Vol I — Library-guided scaffold (operator)

**WORK only;** not Record. This file **informs** drafting; it does **not** replace chapter SSOT.

| SSOT | Role |
|------|------|
| [book-architecture.yaml](../book-architecture.yaml) | Chapter **IDs**, public **titles**, `file` paths, arcs |
| [VOL-I-PROBLEM-CHAPTERS.md](VOL-I-PROBLEM-CHAPTERS.md) | Problem spine: **Q-bundles**, registers |
| [bookshelf-catalog.yaml](bookshelf-catalog.yaml) | **HNSRC-*** shelf rows; `candidate_hn_chapters` planning hints |

**Schema decision (locked for Vol I):** Keep **generic problem titles** from `book-architecture.yaml` (e.g. “Parity, Buffers…”); do not rename chapters to book-specific hooks without a deliberate migration plan.

---

## Shelf strengths and gaps

**Strong anchors:** Greek sources (Landmark + epics + tragedy + Plato), sustained Roman narrative (Everitt + Goldsworthy + Tacitus + late fall), Persia / Mesopotamia / Egypt (Frahm, Llewellyn-Jones, Issa, Cleopatras), steppe / Black Sea (Cunliffe, Roller), **Rome and Persia** (parity), philosophy under empire (Stoics, Lucretius), scriptures + Asian canons (OT/NT, Hindu, Lao Tzu, Confucius), Durant *Story of Civilization* I–III as synthetic spine.

**Thin comparators:** **China and India as continuous *political* history** — shelf has canonical texts (Analects, Tao Te Ching, Hindu scriptures) but few narrative state-history surveys. For `hn-i-v1-16`–`18` (and parts of `12`–`15`), plan explicit **CIV-MEM** or **supplemental reading** unless you acquire titles below.

---

## Optional acquisition targets (reduce MEM-only reliance)

Not required for architecture; pick by taste:

1. **China — one survey** of classical / early imperial state formation and institutions (e.g. Warring States → Qin/Han themes) to pair with **Analects** / **Tao Te Ching** as political context.
2. **South Asia — one survey** of early imperial or post-Vedic political orders (e.g. Maurya/Gupta framing) to pair with **Hindu Scriptures** as more than textual ethics.

Add rows to [bookshelf-catalog.yaml](bookshelf-catalog.yaml) when purchased.

---

## Pending catalog identification

| ID | Status |
|----|--------|
| **HNSRC-0050** | Placeholder: Penguin Clothbound, red spine fish motif — **replace title/author** in the catalog when the spine is read; leave `candidate_hn_chapters` empty until identified. |

---

## Problem spine × shelf (20 chapters)

**Part 1 — State formation and imperial shape**

| Chapter ID | Title (public) | Primary shelf anchors (`HNSRC`) | Drafting note |
|------------|----------------|----------------------------------|---------------|
| `hn-i-v1-01` | Legitimacy After Conquest | [0001](#hnsrc-0001), [0002](#hnsrc-0002), [0008](#hnsrc-0008), [0009](#hnsrc-0009), [0036](#hnsrc-0036), [0055](#hnsrc-0055) | Near Eastern + Persian + biblical templates; Herodotus for Greek–Persian “law of empires.” |
| `hn-i-v1-02` | Civilizational Endurance Under Defeat | [0027](#hnsrc-0027), [0043](#hnsrc-0043), [0044](#hnsrc-0044), [0020](#hnsrc-0020), [0017](#hnsrc-0017) | Tragedy + Plutarch + Roman resilience; Goldsworthy on institutional vs territorial survival. |
| `hn-i-v1-03` | When Power Changes Shape | [0041](#hnsrc-0041), [0042](#hnsrc-0042), [0028](#hnsrc-0028)–[0032](#hnsrc-0032), [0012](#hnsrc-0012) | Regime form: republic vs monarchy vs empire; Macedonian succession. |
| `hn-i-v1-04` | Administration, Law, and the Long Run | [0045](#hnsrc-0045), [0030](#hnsrc-0030), [0031](#hnsrc-0031), [0032](#hnsrc-0032), [0035](#hnsrc-0035), [0039](#hnsrc-0039), [0040](#hnsrc-0040), [0051](#hnsrc-0051), [0053](#hnsrc-0053), [0057](#hnsrc-0057) | Strong Roman spine; Lao/Confucius as **ethical-administrative** contrast; **China** institutions may need MEM/supplement. |
| `hn-i-v1-05` | Expansion Ceilings, Glory, and Consolidation | [0018](#hnsrc-0018), [0019](#hnsrc-0019), [0006](#hnsrc-0006), [0011](#hnsrc-0011), [0034](#hnsrc-0034) | Mediterranean + Hellenistic + Parthian frontier “ceilings.” |

**Part 2 — Reach, inclusion, institutions**

| Chapter ID | Title (public) | Primary shelf anchors | Drafting note |
|------------|----------------|----------------------|---------------|
| `hn-i-v1-06` | Sea Roads and Circulation Empires | [0003](#hnsrc-0003), [0018](#hnsrc-0018), [0047](#hnsrc-0047), [0007](#hnsrc-0007) | Naval Athens + Punic seas + *Odyssey* + Caesar’s maritime reach. |
| `hn-i-v1-07` | Inclusion, Occupation, Annihilation | [0001](#hnsrc-0001), [0002](#hnsrc-0002), [0009](#hnsrc-0009), [0013](#hnsrc-0013), [0045](#hnsrc-0045) | Empires of difference + Hellenistic fusion; siege/annihilation via Thucydides + Punic wars. |
| `hn-i-v1-08` | Institutions Against Genius | [0027](#hnsrc-0027), [0028](#hnsrc-0028)–[0030](#hnsrc-0030), [0006](#hnsrc-0006) | Character-driven history vs institutional momentum. |
| `hn-i-v1-09` | Copying, Standardization, Selective Absorption | [0048](#hnsrc-0048), [0049](#hnsrc-0049), [0004](#hnsrc-0004), [0017](#hnsrc-0017) | Literary and political translation (Greek → Roman); Italian assimilation. |
| `hn-i-v1-10` | From Subjects to Stakeholders | [0003](#hnsrc-0003), [0030](#hnsrc-0030), [0051](#hnsrc-0051), [0053](#hnsrc-0053), [0008](#hnsrc-0008), [0040](#hnsrc-0040), [0038](#hnsrc-0038) | Citizenship and obligation; **India** thin — Hindu texts as careful parallel or add survey. |

**Part 3 — Frontiers, geography, elites**

| Chapter ID | Title (public) | Primary shelf anchors | Drafting note |
|------------|----------------|----------------------|---------------|
| `hn-i-v1-11` | Territorial Maximum, Strategic Maximum, Overreach | [0003](#hnsrc-0003), [0006](#hnsrc-0006), [0011](#hnsrc-0011), [0034](#hnsrc-0034) | Sicily, Alexander, eastern frontier. |
| `hn-i-v1-12` | Geography of Origin and Permanence | [0015](#hnsrc-0015), [0016](#hnsrc-0016), [0055](#hnsrc-0055), [0056](#hnsrc-0056) | Steppe / Black Sea + Durant synthesis; **India** geography via MEM/Durant if needed. |
| `hn-i-v1-13` | Mechanism Failure at the Frontier | [0015](#hnsrc-0015), [0016](#hnsrc-0016), [0034](#hnsrc-0034), [0019](#hnsrc-0019), [0045](#hnsrc-0045), [0005](#hnsrc-0005) | Logistics + eastern disasters + Anabasis corridor. |
| `hn-i-v1-14` | Elite Defection and the Shape of Defeat | [0003](#hnsrc-0003), [0020](#hnsrc-0020), [0029](#hnsrc-0029), [0027](#hnsrc-0027) | Thucydidean elites + late Rome + Antony/Cleopatra. |
| `hn-i-v1-15` | Deflection and Ambivalence Toward Outside Orders | [0039](#hnsrc-0039), [0038](#hnsrc-0038), [0041](#hnsrc-0041), [0052](#hnsrc-0052) | Comparative philosophy; Roman/Greek political examples carry the narrative weight. |

**Part 4 — Eastern synthesis, parity, collapse**

| Chapter ID | Title (public) | Primary shelf anchors | Drafting note |
|------------|----------------|----------------------|---------------|
| `hn-i-v1-16` | Non-Native Rule, Hybridity, Peak, Exhaustion | [0013](#hnsrc-0013), [0014](#hnsrc-0014), [0036](#hnsrc-0036), [0037](#hnsrc-0037), [0057](#hnsrc-0057) | Hellenistic + Roman hybridity strong; **China** non-native dynasties → MEM/supplement. |
| `hn-i-v1-17` | Fragmentation and Monopoly of Authority | [0004](#hnsrc-0004), [0020](#hnsrc-0020), [0017](#hnsrc-0017) | Hellenistic fragmentation + Roman civil wars; **China** optional via MEM. |
| `hn-i-v1-18` | Corridors, Exchange, Legibility, Aftermath of Conquest | [0055](#hnsrc-0055)–[0057](#hnsrc-0057), [0034](#hnsrc-0034), [0013](#hnsrc-0013), [0035](#hnsrc-0035), [0045](#hnsrc-0045) | Durant + Alexandria + Rome–Persia + legibility (census/tax themes). |
| `hn-i-v1-19` | Parity, Buffers, Exhaustion, Third Shock | [0034](#hnsrc-0034), [0009](#hnsrc-0009), [0001](#hnsrc-0001), [0002](#hnsrc-0002), [0008](#hnsrc-0008) | Strongest single-theme fit on shelf: long Iran–Mediterranean parity. |
| `hn-i-v1-20` | Collapse, Vacancy, Succession | [0020](#hnsrc-0020), [0018](#hnsrc-0018), [0045](#hnsrc-0045), [0037](#hnsrc-0037), [0057](#hnsrc-0057) | Western terminus + Punic closure + Christian transition in Durant III. |

Anchor links above jump to **HNSRC** rows in the next section.

---

## HNSRC index (Vol I planning)

Use [bookshelf-catalog.yaml](bookshelf-catalog.yaml) as the authoritative row for each id. Listed `candidate_hn_chapters` are aligned to this scaffold (validator: `python3 scripts/validate_bookshelf_catalog.py --strict`).

### HNSRC-0001 — HNSRC-0010

- <a id="hnsrc-0001"></a>**HNSRC-0001** — Herodotus, *The Histories*
- <a id="hnsrc-0002"></a>**HNSRC-0002** — *The Landmark Herodotus*
- <a id="hnsrc-0003"></a>**HNSRC-0003** — *The Landmark Thucydides*
- <a id="hnsrc-0004"></a>**HNSRC-0004** — Xenophon, *Hellenika* (Landmark)
- <a id="hnsrc-0005"></a>**HNSRC-0005** — Xenophon, *Anabasis* (Landmark)
- <a id="hnsrc-0006"></a>**HNSRC-0006** — Arrian, *Campaigns of Alexander* (Landmark)
- <a id="hnsrc-0007"></a>**HNSRC-0007** — Julius Caesar (Landmark)
- <a id="hnsrc-0008"></a>**HNSRC-0008** — Frahm, *Assyria*
- <a id="hnsrc-0009"></a>**HNSRC-0009** — Llewellyn-Jones, *Persians*
- <a id="hnsrc-0010"></a>**HNSRC-0010** — Everitt, *The Rise of Athens*

### HNSRC-0011 — HNSRC-0020

- <a id="hnsrc-0011"></a>**HNSRC-0011** — Everitt, *Alexander the Great*
- <a id="hnsrc-0012"></a>**HNSRC-0012** — Goldsworthy, *Philip and Alexander*
- <a id="hnsrc-0013"></a>**HNSRC-0013** — Issa, *Alexandria*
- <a id="hnsrc-0014"></a>**HNSRC-0014** — Llewellyn-Jones, *The Cleopatras*
- <a id="hnsrc-0015"></a>**HNSRC-0015** — Cunliffe, *The Scythians*
- <a id="hnsrc-0016"></a>**HNSRC-0016** — Roller, *Empire of the Black Sea*
- <a id="hnsrc-0017"></a>**HNSRC-0017** — Everitt, *The Rise of Rome*
- <a id="hnsrc-0018"></a>**HNSRC-0018** — Goldsworthy, *The Punic Wars*
- <a id="hnsrc-0019"></a>**HNSRC-0019** — Gabriel, *Hannibal*
- <a id="hnsrc-0020"></a>**HNSRC-0020** — Goldsworthy, *How Rome Fell*

### HNSRC-0027 — HNSRC-0058 (incl. classics + Durant + Gibbon + Kaldellis)

- <a id="hnsrc-0027"></a>**HNSRC-0027** — Plutarch, *Lives*
- <a id="hnsrc-0028"></a>**HNSRC-0028** — Goldsworthy, *Caesar: Life of a Colossus*
- <a id="hnsrc-0029"></a>**HNSRC-0029** — Goldsworthy, *Antony and Cleopatra*
- <a id="hnsrc-0030"></a>**HNSRC-0030** — Everitt, *Cicero*
- <a id="hnsrc-0031"></a>**HNSRC-0031** — Goldsworthy, *Augustus: First Emperor of Rome*
- <a id="hnsrc-0032"></a>**HNSRC-0032** — Everitt, *Augustus: The Life of Rome's First Emperor*
- <a id="hnsrc-0033"></a>**HNSRC-0033** — Everitt, *Hadrian and the Triumph of Rome*
- <a id="hnsrc-0034"></a>**HNSRC-0034** — Goldsworthy, *Rome and Persia*
- <a id="hnsrc-0035"></a>**HNSRC-0035** — Goldsworthy, *Pax Romana*
- <a id="hnsrc-0036"></a>**HNSRC-0036** — *The Old Testament*
- <a id="hnsrc-0037"></a>**HNSRC-0037** — *The New Testament*
- <a id="hnsrc-0038"></a>**HNSRC-0038** — *Hindu Scriptures*
- <a id="hnsrc-0039"></a>**HNSRC-0039** — Lao Tzu, *Tao Te Ching*
- <a id="hnsrc-0040"></a>**HNSRC-0040** — Confucius, *The Analects*
- <a id="hnsrc-0041"></a>**HNSRC-0041** — Plato, *The Republic*
- <a id="hnsrc-0042"></a>**HNSRC-0042** — Plato, *Symposium and Phaedrus*
- <a id="hnsrc-0043"></a>**HNSRC-0043** — Sophocles, *The Theban Plays*
- <a id="hnsrc-0044"></a>**HNSRC-0044** — Aeschylus, *The Oresteia*
- <a id="hnsrc-0045"></a>**HNSRC-0045** — Tacitus, *Annals and Histories*
- <a id="hnsrc-0046"></a>**HNSRC-0046** — Homer, *The Iliad*
- <a id="hnsrc-0047"></a>**HNSRC-0047** — Homer, *The Odyssey*
- <a id="hnsrc-0048"></a>**HNSRC-0048** — Virgil, *The Aeneid*
- <a id="hnsrc-0049"></a>**HNSRC-0049** — Ovid, *Metamorphoses*
- **HNSRC-0050** — Placeholder (see [Pending catalog identification](#pending-catalog-identification))
- <a id="hnsrc-0051"></a>**HNSRC-0051** — Marcus Aurelius, *Meditations*
- <a id="hnsrc-0052"></a>**HNSRC-0052** — Lucretius, *On the Nature of Things*
- <a id="hnsrc-0053"></a>**HNSRC-0053** — Seneca, *Letters from a Stoic*
- <a id="hnsrc-0054"></a>**HNSRC-0054** — Gibbon, *Decline and Fall* (medieval shelf; spans ancient + medieval)
- <a id="hnsrc-0055"></a>**HNSRC-0055** — Durant, *Story of Civilization* Vol. I
- <a id="hnsrc-0056"></a>**HNSRC-0056** — Durant, Vol. II (*The Life of Greece*)
- <a id="hnsrc-0057"></a>**HNSRC-0057** — Durant, Vol. III (*Caesar and Christ*)
- <a id="hnsrc-0058"></a>**HNSRC-0058** — Kaldellis, *The New Roman Empire* (Vol II shelf; Byzantine)

Medieval-era rows (**HNSRC-0021**–**0026**, etc.) remain in the catalog for other volumes; they are not listed in the 20-chapter matrix above unless cross-linked for continuity (e.g. Gibbon, Kaldellis).

---

## Maintenance

- After changing [bookshelf-catalog.yaml](bookshelf-catalog.yaml), run `python3 scripts/validate_bookshelf_catalog.py --strict`.
- When **HNSRC-0050** is identified, update the YAML row and add `candidate_hn_chapters` if appropriate; trim this file’s placeholder section.
