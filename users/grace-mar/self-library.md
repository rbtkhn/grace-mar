# LIBRARY — grace-mar

A curated return-to store of references, canon works, and influential media. It supports lookup when answering questions and preserves what has shaped the mind or belongs in Grace-Mar's long-term intellectual world.

**Cloned from companion-self** `users/_template/self-library.md` (2026-02-26). Grace-mar-specific entries (reference works, videos) appended. File renamed from library.md to self-library.md for consistency with self-* taxonomy.

**Schema:** [docs/library-schema.md](../../docs/library-schema.md)

---

## Entries

```yaml
entries:
  # --- Grace-mar reference works (prepended) ---
  - id: LIB-0001
    title: "Usborne World Geography Encyclopedia (Internet Linked)"
    author: "Usborne"
    isbn: "9780746042069"
    lane: "reference"
    type: "reference"
    status: "active"
    engagement_status: "available"
    lookup_priority: "medium"
    scope: ["geography", "world atlas", "maps"]
    source: "manual"
    added_at: 2026-02-20
    notes: "Complete World Atlas. Ordered Sept 2025."

  - id: LIB-0002
    title: "Usborne World History Encyclopedia: An Illustrated Introduction to World History for Kids, full of Maps, Time Charts and over 800 Links for Homework Help"
    author: "Usborne"
    isbn: "9781836052555"
    lane: "reference"
    type: "reference"
    status: "active"
    engagement_status: "available"
    lookup_priority: "medium"
    scope: ["history", "world history", "maps", "time charts"]
    source: "manual"
    added_at: 2026-02-20
    notes: "Usborne Encyclopedias. Ordered Sept 2025."

  - id: LIB-0003
    title: "Usborne Science Encyclopedia: An In-depth Guide for Young Scientists Exploring Gravity, Flight, Genes, DNA and More, with Over 180 Video Clips and 1000 Recommended Websites for Further Learning"
    author: "Usborne"
    isbn: "9781805079019"
    lane: "reference"
    type: "reference"
    status: "active"
    engagement_status: "available"
    lookup_priority: "medium"
    scope: ["science", "physics", "chemistry", "biology", "gravity", "flight", "genes", "DNA"]
    source: "manual"
    added_at: 2026-02-20
    notes: "Ordered Sept 2025."


  # --- Companion-self (books and stories) ---
  - id: LIB-0004
    title: "Greek Myths (Bulfinch, PG 22381)"
    author: "Usborne"
    isbn: "9781474986441"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["mythology", "Greek myths", "ancient Greece"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/22381"
    added_at: 2026-02-20
    notes: "Replaced by story-level entries LIB-0064 to LIB-0077 (Bulfinch 3327, Odyssey 1727)."

  - id: LIB-0005
    title: "The Odyssey (Homer, PG 1727)"
    author: "Usborne"
    isbn: "9781409598930"
    lane: "canon"
    type: "book"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Greek", "Odyssey", "Homer"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/1727"
    added_at: 2026-02-20
    notes: "Ordered Sept 2025."

  - id: LIB-0006
    title: "Stories from India (PG 2388)"
    author: "Usborne"
    isbn: "9781409596714"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["mythology", "India", "stories", "folktales"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2388"
    added_at: 2026-02-20
    notes: "Replaced by story-level entry LIB-0078 (PD 2388)."

  - id: LIB-0007
    title: "Adventure classics (PG 521, 120, 829)"
    author: "Usborne"
    isbn: "9781409522300"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["adventure", "stories"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/1184"
    added_at: 2026-02-20
    notes: "Replaced by story-level entries LIB-0079 to LIB-0081 (PD 521, 120, 829)."

  - id: LIB-0008
    title: "Bible stories (KJV, PG 10)"
    author: "Usborne"
    isbn: "9781409580980"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["Bible", "stories", "religion"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/10"
    added_at: 2026-02-20
    notes: "Replaced by story-level entries LIB-0082 to LIB-0088 (KJV 10)."

  - id: LIB-0009
    title: "Stories from China (PG 25240)"
    author: "Usborne"
    isbn: "9781474947077"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["China", "stories", "folktales"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/25240"
    added_at: 2026-02-20
    notes: "Replaced by story-level entry LIB-0089 (PD 25240)."

  - id: LIB-0010
    title: "Myths from around the world (Bulfinch, PG 3327)"
    author: "Usborne"
    isbn: "9781409596738"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["mythology", "world myths", "folktales"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    added_at: 2026-02-20
    notes: "Replaced by story-level entries LIB-0064 to LIB-0077 (Greek/Roman in 3327)."

  - id: LIB-0011
    title: "Ballet stories (PG 38733)"
    author: "Usborne"
    isbn: "9781474922050"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["ballet", "dance", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    added_at: 2026-02-20
    notes: "Replaced by story-level entries LIB-0052 to LIB-0063. Ordered Sept 2025."

  - id: LIB-0012
    title: "The Secret Garden (PG 17396)"
    author: "Usborne"
    isbn: "9781409586562"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["classics", "Secret Garden", "stories"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/17396"
    added_at: 2026-02-20
    notes: "Replaced by story-level entry LIB-0090 (Secret Garden 17396)."

  - id: LIB-0013
    title: "Aesop's Fables (PG 21)"
    author: "Usborne"
    isbn: "9781409538875"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["fables", "Aesop", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/21"
    added_at: 2026-02-20
    notes: "Replaced by story-level entries LIB-0091 to LIB-0095 (Aesop 21)."

  - id: LIB-0014
    title: "Greek myths (PG 11582)"
    author: "Usborne"
    isbn: "9781409531678"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["mythology", "Greek myths", "stories"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/11582"
    added_at: 2026-02-20
    notes: "Replaced by story-level entries LIB-0064 to LIB-0076 (Bulfinch 3327)."

  - id: LIB-0015
    title: "Norse myths (Guerber, PG 28497)"
    author: "Usborne"
    isbn: "9781409550723"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["mythology", "Norse", "Vikings", "stories"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/28497"
    added_at: 2026-02-20
    notes: "Replaced by story-level entries LIB-0096 to LIB-0100 (Guerber 28497)."

  - id: LIB-0016
    title: "Andersen's Fairy Tales (PG 27200)"
    author: "Usborne"
    isbn: "9781409523390"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["fairy tales", "Hans Christian Andersen", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    added_at: 2026-02-20
    notes: "Replaced by story-level entries LIB-0040 to LIB-0051. Ordered Sept 2025."

  - id: LIB-0017
    title: "King Arthur (Malory, PG 610)"
    author: "Usborne"
    isbn: "9781409563266"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["King Arthur", "legends", "stories", "mythology"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/610"
    added_at: 2026-02-20
    notes: "Replaced by story-level entry LIB-0101 (Malory 610)."

  - id: LIB-0018
    title: "Stories from Shakespeare (PG 100)"
    author: "Usborne"
    isbn: "9781409522232"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["Shakespeare", "plays", "stories"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/100"
    added_at: 2026-02-20
    notes: "Replaced by story-level entries LIB-0102 to LIB-0114 (Complete Works 100)."

  - id: LIB-0019
    title: "Grimm's Fairy Tales (PG 2591)"
    author: "Usborne"
    isbn: "9780746098547"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["fairy tales", "Grimm", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    added_at: 2026-02-20
    notes: "Replaced by story-level entries LIB-0025 to LIB-0039. Ordered Sept 2025."

  - id: LIB-0020
    title: "Dickens (PG author 37)"
    author: "Usborne"
    isbn: "9781474938136"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["Dickens", "classics", "literature"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/author/37"
    added_at: 2026-02-20
    notes: "Replaced by story-level entries LIB-0115 to LIB-0120 (per-novel PD links)."

  - id: LIB-0021
    title: "Arabian Nights (Lang, PG 128)"
    author: "Anna Milbourne"
    isbn: "9781409533009"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["Arabian Nights", "tales", "Middle East", "stories"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/128"
    added_at: 2026-02-20
    notes: "Replaced by story-level entries LIB-0121 to LIB-0125 (Lang 128)."

  - id: LIB-0022
    title: "Shakespeare, Complete Works (PG 100)"
    author: "Usborne"
    isbn: "9781409598770"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["Shakespeare", "plays", "stories", "classics"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/100"
    added_at: 2026-02-20
    notes: "Replaced by story-level entries LIB-0102 to LIB-0114 (Complete Works 100)."

  - id: LIB-0023
    title: "Jane Austen (PG author 68)"
    author: "Usborne"
    isbn: "9781474938143"
    lane: "canon"
    type: "book"
    status: "deprecated"
    engagement_status: "planned"
    lookup_priority: "none"
    scope: ["Jane Austen", "novels", "classics", "literature"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/author/68"
    added_at: 2026-02-20
    notes: "Replaced by story-level entries LIB-0126 to LIB-0131 (per-novel PD links)."

  - id: LIB-0025
    title: "Snow White and Rose Red"
    lane: "canon"
    type: "story"
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Grimm", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    added_at: 2026-02-22

  - id: LIB-0026
    title: "Little Red Riding Hood"
    lane: "canon"
    type: "story"
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Grimm", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    added_at: 2026-02-22

  - id: LIB-0027
    title: "Rapunzel"
    lane: "canon"
    type: "story"
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Grimm", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    added_at: 2026-02-22

  - id: LIB-0028
    title: "Sleeping Beauty"
    lane: "canon"
    type: "story"
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Grimm", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    added_at: 2026-02-22

  - id: LIB-0029
    title: "The Frog Prince"
    lane: "canon"
    type: "story"
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Grimm", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    added_at: 2026-02-22

  - id: LIB-0030
    title: "The Musicians of Bremen"
    lane: "canon"
    type: "story"
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Grimm", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    added_at: 2026-02-22

  - id: LIB-0031
    title: "Rumpelstiltskin"
    lane: "canon"
    type: "story"
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Grimm", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    added_at: 2026-02-22

  - id: LIB-0032
    title: "Tom Thumb"
    lane: "canon"
    type: "story"
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Grimm", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    added_at: 2026-02-22

  - id: LIB-0033
    title: "Hansel and Gretel"
    lane: "canon"
    type: "story"
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Grimm", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    added_at: 2026-02-22

  - id: LIB-0034
    title: "The Twelve Dancing Princesses"
    lane: "canon"
    type: "story"
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Grimm", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    added_at: 2026-02-22

  - id: LIB-0035
    title: "The Bear and the Wren"
    lane: "canon"
    type: "story"
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Grimm", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    added_at: 2026-02-22

  - id: LIB-0036
    title: "King Thrushbeard"
    lane: "canon"
    type: "story"
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Grimm", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    added_at: 2026-02-22

  - id: LIB-0037
    title: "The Goose Girl"
    lane: "canon"
    type: "story"
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Grimm", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    added_at: 2026-02-22

  - id: LIB-0038
    title: "The Elves and the Shoemaker"
    lane: "canon"
    type: "story"
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Grimm", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    added_at: 2026-02-22

  - id: LIB-0039
    title: "Snow White and the Seven Dwarfs"
    lane: "canon"
    type: "story"
    volume: "Grimm's Fairy Tales (PG 2591)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Grimm", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2591"
    added_at: 2026-02-22

  - id: LIB-0040
    title: "The Princess and the Pea"
    lane: "canon"
    type: "story"
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Hans Christian Andersen", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    added_at: 2026-02-22

  - id: LIB-0041
    title: "The Emperor's New Clothes"
    lane: "canon"
    type: "story"
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Hans Christian Andersen", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    added_at: 2026-02-22

  - id: LIB-0042
    title: "Thumbelina"
    lane: "canon"
    type: "story"
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Hans Christian Andersen", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    added_at: 2026-02-22

  - id: LIB-0043
    title: "The Ugly Duckling"
    lane: "canon"
    type: "story"
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Hans Christian Andersen", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    added_at: 2026-02-22

  - id: LIB-0044
    title: "The Little Mermaid"
    lane: "canon"
    type: "story"
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Hans Christian Andersen", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    added_at: 2026-02-22

  - id: LIB-0045
    title: "The Emperor and the Nightingale"
    lane: "canon"
    type: "story"
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Hans Christian Andersen", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    added_at: 2026-02-22

  - id: LIB-0046
    title: "The Flying Trunk"
    lane: "canon"
    type: "story"
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Hans Christian Andersen", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    added_at: 2026-02-22

  - id: LIB-0047
    title: "The Brave Tin Soldier"
    lane: "canon"
    type: "story"
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Hans Christian Andersen", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    added_at: 2026-02-22

  - id: LIB-0048
    title: "The Wild Swans"
    lane: "canon"
    type: "story"
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Hans Christian Andersen", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    added_at: 2026-02-22

  - id: LIB-0049
    title: "The Little Fir Tree"
    lane: "canon"
    type: "story"
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Hans Christian Andersen", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    added_at: 2026-02-22

  - id: LIB-0050
    title: "The Tinderbox"
    lane: "canon"
    type: "story"
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Hans Christian Andersen", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    added_at: 2026-02-22

  - id: LIB-0051
    title: "The Snow Queen"
    lane: "canon"
    type: "story"
    volume: "Andersen's Fairy Tales (PG 27200)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fairy tales", "Hans Christian Andersen", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/27200"
    added_at: 2026-02-22

  - id: LIB-0052
    title: "Cinderella"
    lane: "canon"
    type: "story"
    volume: "Ballet stories (PG 38733)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["ballet", "dance", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    added_at: 2026-02-22

  - id: LIB-0053
    title: "Swan Lake"
    lane: "canon"
    type: "story"
    volume: "Ballet stories (PG 38733)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["ballet", "dance", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    added_at: 2026-02-22

  - id: LIB-0054
    title: "Sleeping Beauty"
    lane: "canon"
    type: "story"
    volume: "Ballet stories (PG 38733)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["ballet", "dance", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    added_at: 2026-02-22

  - id: LIB-0055
    title: "Don Quixote"
    lane: "canon"
    type: "story"
    volume: "Ballet stories (PG 38733)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["ballet", "dance", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    added_at: 2026-02-22

  - id: LIB-0056
    title: "Coppélia"
    lane: "canon"
    type: "story"
    volume: "Ballet stories (PG 38733)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["ballet", "dance", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    added_at: 2026-02-22

  - id: LIB-0057
    title: "The Nutcracker"
    lane: "canon"
    type: "story"
    volume: "Ballet stories (PG 38733)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["ballet", "dance", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    added_at: 2026-02-22

  - id: LIB-0058
    title: "The Firebird"
    lane: "canon"
    type: "story"
    volume: "Ballet stories (PG 38733)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["ballet", "dance", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    added_at: 2026-02-22

  - id: LIB-0059
    title: "Giselle"
    lane: "canon"
    type: "story"
    volume: "Ballet stories (PG 38733)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["ballet", "dance", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    added_at: 2026-02-22

  - id: LIB-0060
    title: "Ondine"
    lane: "canon"
    type: "story"
    volume: "Ballet stories (PG 38733)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["ballet", "dance", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    added_at: 2026-02-22

  - id: LIB-0061
    title: "La Sylphide"
    lane: "canon"
    type: "story"
    volume: "Ballet stories (PG 38733)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["ballet", "dance", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    added_at: 2026-02-22

  - id: LIB-0062
    title: "La Fille Mal Gardée"
    lane: "canon"
    type: "story"
    volume: "Ballet stories (PG 38733)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["ballet", "dance", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    added_at: 2026-02-22

  - id: LIB-0063
    title: "Romeo and Juliet"
    lane: "canon"
    type: "story"
    volume: "Ballet stories (PG 38733)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["ballet", "dance", "stories"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/38733"
    added_at: 2026-02-22

  - id: LIB-0064
    title: "Prometheus and Pandora"
    lane: "canon"
    type: "story"
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Greek myths"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    added_at: 2026-02-26

  - id: LIB-0065
    title: "Apollo and Daphne"
    lane: "canon"
    type: "story"
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Greek myths"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    added_at: 2026-02-26

  - id: LIB-0066
    title: "Phaeton"
    lane: "canon"
    type: "story"
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Greek myths"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    added_at: 2026-02-26

  - id: LIB-0067
    title: "Midas, Baucis and Philemon"
    lane: "canon"
    type: "story"
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Greek myths"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    added_at: 2026-02-26

  - id: LIB-0068
    title: "Proserpine (Persephone)"
    lane: "canon"
    type: "story"
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Greek myths"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    added_at: 2026-02-26

  - id: LIB-0069
    title: "Pygmalion and Dryope"
    lane: "canon"
    type: "story"
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Greek myths"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    added_at: 2026-02-26

  - id: LIB-0070
    title: "Cupid and Psyche"
    lane: "canon"
    type: "story"
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Greek myths"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    added_at: 2026-02-26

  - id: LIB-0071
    title: "Cadmus and the Myrmidons"
    lane: "canon"
    type: "story"
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Greek myths"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    added_at: 2026-02-26

  - id: LIB-0072
    title: "Minerva and Arachne, Niobe"
    lane: "canon"
    type: "story"
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Greek myths"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    added_at: 2026-02-26

  - id: LIB-0073
    title: "Perseus and Medusa"
    lane: "canon"
    type: "story"
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Greek myths"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    added_at: 2026-02-26

  - id: LIB-0074
    title: "The Golden Fleece and Medea"
    lane: "canon"
    type: "story"
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Greek myths"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    added_at: 2026-02-26

  - id: LIB-0075
    title: "Hercules"
    lane: "canon"
    type: "story"
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Greek myths"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    added_at: 2026-02-26

  - id: LIB-0076
    title: "Theseus and the Minotaur"
    lane: "canon"
    type: "story"
    volume: "Greek myths (Bulfinch, PG 3327)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Greek myths"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/3327"
    added_at: 2026-02-26

  - id: LIB-0077
    title: "The Odyssey"
    lane: "canon"
    type: "story"
    volume: "Homer, Odyssey (PG 1727)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Greek", "Homer"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/1727"
    added_at: 2026-02-26

  - id: LIB-0078
    title: "Stories from India (collection)"
    lane: "canon"
    type: "story"
    volume: "Stories from India (PG 2388)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["India", "stories", "folktales"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/2388"
    added_at: 2026-02-26

  - id: LIB-0079
    title: "Robinson Crusoe"
    lane: "canon"
    type: "story"
    volume: "Adventure classics (PG 521, 120, 829)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["adventure", "stories"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/521"
    added_at: 2026-02-26

  - id: LIB-0080
    title: "Treasure Island"
    lane: "canon"
    type: "story"
    volume: "Adventure classics (PG 521, 120, 829)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["adventure", "stories"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/120"
    added_at: 2026-02-26

  - id: LIB-0081
    title: "Gulliver's Travels"
    lane: "canon"
    type: "story"
    volume: "Adventure classics (PG 521, 120, 829)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["adventure", "stories"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/829"
    added_at: 2026-02-26

  - id: LIB-0082
    title: "Creation and Eden"
    lane: "canon"
    type: "story"
    volume: "Bible, KJV (PG 10)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Bible", "stories", "religion"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/10"
    added_at: 2026-02-26

  - id: LIB-0083
    title: "Noah and the Flood"
    lane: "canon"
    type: "story"
    volume: "Bible, KJV (PG 10)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Bible", "stories", "religion"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/10"
    added_at: 2026-02-26

  - id: LIB-0084
    title: "Abraham and Isaac"
    lane: "canon"
    type: "story"
    volume: "Bible, KJV (PG 10)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Bible", "stories", "religion"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/10"
    added_at: 2026-02-26

  - id: LIB-0085
    title: "Moses and the Exodus"
    lane: "canon"
    type: "story"
    volume: "Bible, KJV (PG 10)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Bible", "stories", "religion"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/10"
    added_at: 2026-02-26

  - id: LIB-0086
    title: "David and Goliath"
    lane: "canon"
    type: "story"
    volume: "Bible, KJV (PG 10)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Bible", "stories", "religion"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/10"
    added_at: 2026-02-26

  - id: LIB-0087
    title: "Daniel in the Lions' Den"
    lane: "canon"
    type: "story"
    volume: "Bible, KJV (PG 10)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Bible", "stories", "religion"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/10"
    added_at: 2026-02-26

  - id: LIB-0088
    title: "The Nativity"
    lane: "canon"
    type: "story"
    volume: "Bible, KJV (PG 10)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Bible", "stories", "religion"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/10"
    added_at: 2026-02-26

  - id: LIB-0089
    title: "Stories from China (collection)"
    lane: "canon"
    type: "story"
    volume: "Stories from China (PG 25240)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["China", "stories", "folktales"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/25240"
    added_at: 2026-02-26

  - id: LIB-0090
    title: "The Secret Garden"
    lane: "canon"
    type: "story"
    volume: "The Secret Garden (PG 17396)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["classics", "Secret Garden"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/17396"
    added_at: 2026-02-26

  - id: LIB-0091
    title: "The Lion and the Mouse"
    lane: "canon"
    type: "story"
    volume: "Aesop's Fables (PG 21)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fables", "Aesop"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/21"
    added_at: 2026-02-26

  - id: LIB-0092
    title: "The Hare and the Tortoise"
    lane: "canon"
    type: "story"
    volume: "Aesop's Fables (PG 21)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fables", "Aesop"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/21"
    added_at: 2026-02-26

  - id: LIB-0093
    title: "The Wolf and the Lamb"
    lane: "canon"
    type: "story"
    volume: "Aesop's Fables (PG 21)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fables", "Aesop"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/21"
    added_at: 2026-02-26

  - id: LIB-0094
    title: "The Shepherd's Boy and the Wolf"
    lane: "canon"
    type: "story"
    volume: "Aesop's Fables (PG 21)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fables", "Aesop"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/21"
    added_at: 2026-02-26

  - id: LIB-0095
    title: "The Dog and the Shadow"
    lane: "canon"
    type: "story"
    volume: "Aesop's Fables (PG 21)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["fables", "Aesop"]
    maturity: 1
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/21"
    added_at: 2026-02-26

  - id: LIB-0096
    title: "The Creation (Norse)"
    lane: "canon"
    type: "story"
    volume: "Norse myths (Guerber, PG 28497)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Norse", "Vikings"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/28497"
    added_at: 2026-02-26

  - id: LIB-0097
    title: "Odin and the Norse Gods"
    lane: "canon"
    type: "story"
    volume: "Norse myths (Guerber, PG 28497)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Norse", "Vikings"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/28497"
    added_at: 2026-02-26

  - id: LIB-0098
    title: "Thor and Loki"
    lane: "canon"
    type: "story"
    volume: "Norse myths (Guerber, PG 28497)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Norse", "Vikings"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/28497"
    added_at: 2026-02-26

  - id: LIB-0099
    title: "The Death of Baldur"
    lane: "canon"
    type: "story"
    volume: "Norse myths (Guerber, PG 28497)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Norse", "Vikings"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/28497"
    added_at: 2026-02-26

  - id: LIB-0100
    title: "Ragnarok"
    lane: "canon"
    type: "story"
    volume: "Norse myths (Guerber, PG 28497)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["mythology", "Norse", "Vikings"]
    maturity: 2
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/28497"
    added_at: 2026-02-26

  - id: LIB-0101
    title: "Tales of King Arthur (collection)"
    lane: "canon"
    type: "story"
    volume: "Usborne Illustrated Tales of King Arthur"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["King Arthur", "legends", "mythology"]
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/610"
    added_at: 2026-02-26

  - id: LIB-0102
    title: "Hamlet"
    lane: "canon"
    type: "story"
    volume: "Shakespeare, Complete Works (PG 100)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Shakespeare", "plays"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/100"
    added_at: 2026-02-26

  - id: LIB-0103
    title: "Macbeth"
    lane: "canon"
    type: "story"
    volume: "Shakespeare, Complete Works (PG 100)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Shakespeare", "plays"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/100"
    added_at: 2026-02-26

  - id: LIB-0104
    title: "Romeo and Juliet"
    lane: "canon"
    type: "story"
    volume: "Shakespeare, Complete Works (PG 100)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Shakespeare", "plays"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/100"
    added_at: 2026-02-26

  - id: LIB-0105
    title: "A Midsummer Night's Dream"
    lane: "canon"
    type: "story"
    volume: "Shakespeare, Complete Works (PG 100)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Shakespeare", "plays"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/100"
    added_at: 2026-02-26

  - id: LIB-0106
    title: "The Tempest"
    lane: "canon"
    type: "story"
    volume: "Shakespeare, Complete Works (PG 100)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Shakespeare", "plays"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/100"
    added_at: 2026-02-26

  - id: LIB-0107
    title: "Othello"
    lane: "canon"
    type: "story"
    volume: "Shakespeare, Complete Works (PG 100)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Shakespeare", "plays"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/100"
    added_at: 2026-02-26

  - id: LIB-0108
    title: "King Lear"
    lane: "canon"
    type: "story"
    volume: "Shakespeare, Complete Works (PG 100)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Shakespeare", "plays"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/100"
    added_at: 2026-02-26

  - id: LIB-0109
    title: "The Merchant of Venice"
    lane: "canon"
    type: "story"
    volume: "Shakespeare, Complete Works (PG 100)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Shakespeare", "plays"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/100"
    added_at: 2026-02-26

  - id: LIB-0110
    title: "Twelfth Night"
    lane: "canon"
    type: "story"
    volume: "Shakespeare, Complete Works (PG 100)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Shakespeare", "plays"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/100"
    added_at: 2026-02-26

  - id: LIB-0111
    title: "As You Like It"
    lane: "canon"
    type: "story"
    volume: "Shakespeare, Complete Works (PG 100)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Shakespeare", "plays"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/100"
    added_at: 2026-02-26

  - id: LIB-0112
    title: "Much Ado About Nothing"
    lane: "canon"
    type: "story"
    volume: "Shakespeare, Complete Works (PG 100)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Shakespeare", "plays"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/100"
    added_at: 2026-02-26

  - id: LIB-0113
    title: "Julius Caesar"
    lane: "canon"
    type: "story"
    volume: "Shakespeare, Complete Works (PG 100)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Shakespeare", "plays"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/100"
    added_at: 2026-02-26

  - id: LIB-0114
    title: "Stories from Shakespeare (all plays)"
    lane: "canon"
    type: "story"
    volume: "Shakespeare, Complete Works (PG 100)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Shakespeare", "plays"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/100"
    added_at: 2026-02-26

  - id: LIB-0115
    title: "Oliver Twist"
    lane: "canon"
    type: "story"
    volume: "Dickens (PG author 37)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Dickens", "classics"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/730"
    added_at: 2026-02-26

  - id: LIB-0116
    title: "David Copperfield"
    lane: "canon"
    type: "story"
    volume: "Dickens (PG author 37)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Dickens", "classics"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/766"
    added_at: 2026-02-26

  - id: LIB-0117
    title: "Great Expectations"
    lane: "canon"
    type: "story"
    volume: "Dickens (PG author 37)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Dickens", "classics"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/1400"
    added_at: 2026-02-26

  - id: LIB-0118
    title: "A Tale of Two Cities"
    lane: "canon"
    type: "story"
    volume: "Dickens (PG author 37)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Dickens", "classics"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/98"
    added_at: 2026-02-26

  - id: LIB-0119
    title: "Bleak House"
    lane: "canon"
    type: "story"
    volume: "Dickens (PG author 37)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Dickens", "classics"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/1023"
    added_at: 2026-02-26

  - id: LIB-0120
    title: "Dickens (other novels)"
    lane: "canon"
    type: "story"
    volume: "Dickens (PG author 37)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Dickens", "classics"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/author/37"
    added_at: 2026-02-26

  - id: LIB-0121
    title: "Aladdin and the Wonderful Lamp"
    lane: "canon"
    type: "story"
    volume: "Arabian Nights (Lang, PG 128)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Arabian Nights", "tales"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/128"
    added_at: 2026-02-26

  - id: LIB-0122
    title: "Sindbad the Sailor"
    lane: "canon"
    type: "story"
    volume: "Arabian Nights (Lang, PG 128)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Arabian Nights", "tales"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/128"
    added_at: 2026-02-26

  - id: LIB-0123
    title: "Ali Baba and the Forty Thieves"
    lane: "canon"
    type: "story"
    volume: "Arabian Nights (Lang, PG 128)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Arabian Nights", "tales"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/128"
    added_at: 2026-02-26

  - id: LIB-0124
    title: "The Fisherman and the Jinni"
    lane: "canon"
    type: "story"
    volume: "Arabian Nights (Lang, PG 128)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Arabian Nights", "tales"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/128"
    added_at: 2026-02-26

  - id: LIB-0125
    title: "Arabian Nights (full collection)"
    lane: "canon"
    type: "story"
    volume: "Arabian Nights (Lang, PG 128)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Arabian Nights", "tales"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/128"
    added_at: 2026-02-26

  - id: LIB-0126
    title: "Pride and Prejudice"
    lane: "canon"
    type: "story"
    volume: "Jane Austen (PG author 68)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Jane Austen", "novels", "classics"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/1342"
    added_at: 2026-02-26

  - id: LIB-0127
    title: "Sense and Sensibility"
    lane: "canon"
    type: "story"
    volume: "Jane Austen (PG author 68)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Jane Austen", "novels", "classics"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/161"
    added_at: 2026-02-26

  - id: LIB-0128
    title: "Emma"
    lane: "canon"
    type: "story"
    volume: "Jane Austen (PG author 68)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Jane Austen", "novels", "classics"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/158"
    added_at: 2026-02-26

  - id: LIB-0129
    title: "Mansfield Park"
    lane: "canon"
    type: "story"
    volume: "Jane Austen (PG author 68)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Jane Austen", "novels", "classics"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/141"
    added_at: 2026-02-26

  - id: LIB-0130
    title: "Northanger Abbey"
    lane: "canon"
    type: "story"
    volume: "Jane Austen (PG author 68)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Jane Austen", "novels", "classics"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/121"
    added_at: 2026-02-26

  - id: LIB-0131
    title: "Persuasion"
    lane: "canon"
    type: "story"
    volume: "Jane Austen (PG author 68)"
    status: "active"
    engagement_status: "planned"
    lookup_priority: "low"
    scope: ["Jane Austen", "novels", "classics"]
    maturity: 3
    source: "manual"
    pd_url: "https://www.gutenberg.org/ebooks/105"
    added_at: 2026-02-26


  # --- Grace-mar-specific (reference, videos) ---
  - id: LIB-0132
    title: "Civilization Memory Codex"
    lane: "reference"
    type: "reference"
    status: "active"
    engagement_status: "primary"
    lookup_priority: "high"
    scope: ["civilizations", "history", "Rome", "China", "ancient", "emperors", "pharaohs"]
    source: "manual"
    url: "https://github.com/rbtkhn/grace-mar/blob/main/docs/civilization-memory/README.md"
    added_at: 2026-02-26
    notes: "Civilizational lookup. Essay canon grace-mar–owned: docs/civilization-memory/. Optional upstream repo repos/civilization_memory. See docs/civilization-memory/README.md."

  - id: LIB-0133
    title: "Coppélia. HD. Bolshoi Ballet. Natalia Osipova. Finale"
    lane: "influence"
    type: "video"
    status: "active"
    engagement_status: "recurring"
    lookup_priority: "none"
    scope: ["ballet", "Coppélia", "Bolshoi", "dance"]
    source: "manual"
    added_at: 2026-02-26
    notes: "Bolshoi Ballet performance; watched a lot recently; described as sublime."

  - id: LIB-0134
    title: "The Best of Debussy / Classical Piano Music"
    lane: "influence"
    type: "video"
    status: "active"
    engagement_status: "recurring"
    lookup_priority: "none"
    scope: ["Debussy", "classical", "piano", "bedtime", "Clair de lune", "Arabesque"]
    source: "manual"
    added_at: 2026-02-26
    notes: "2-hour Debussy piano collection; used for bedtime; described as perfect."

  # --- Theology (thematic; see ## Theology below) ---
  - id: LIB-0135
    title: "The Simple Condition"
    author: "Robert Kuhne"
    lane: "reference"
    type: "article"
    status: "active"
    engagement_status: "trusted"
    lookup_priority: "medium"
    scope: ["theology", "ethics", "coordination", "dignity", "civilization_memory"]
    source: "manual"
    url: "https://github.com/rbtkhn/grace-mar/blob/main/docs/civilization-memory/essays/THE-SIMPLE-CONDITION.md"
    added_at: 2026-03-14
    notes: "Essay — grace-mar path docs/civilization-memory/essays/. ENCYCLOPEDIA.md anchor ## CM:essays/THE-SIMPLE-CONDITION.md"

  # --- Civ-mem hybrid doors (see docs/civ-mem-encyclopedia-hybrid.md) ---
  - id: LIB-0136
    title: "Civ-mem — Essays index"
    author: "grace-mar"
    lane: "reference"
    type: "article"
    status: "active"
    engagement_status: "trusted"
    lookup_priority: "medium"
    scope: ["essays", "civilization_memory", "taxonomy", "grace_mar_owned"]
    source: "url"
    url: "https://github.com/rbtkhn/grace-mar/blob/main/docs/civilization-memory/essays/README.md"
    added_at: 2026-03-15
    notes: "docs/civilization-memory/essays/README.md — ENCYCLOPEDIA anchor ## CM:essays/README.md"

  - id: LIB-0137
    title: "Civ-mem — The Coordination Hypothesis"
    author: "grace-mar"
    lane: "reference"
    type: "article"
    status: "active"
    engagement_status: "trusted"
    lookup_priority: "medium"
    scope: ["essays", "coordination", "civilization_memory", "theology"]
    source: "url"
    url: "https://github.com/rbtkhn/grace-mar/blob/main/docs/civilization-memory/essays/THE-COORDINATION-HYPOTHESIS.md"
    added_at: 2026-03-15
    notes: "ENCYCLOPEDIA anchor ## CM:essays/THE-COORDINATION-HYPOTHESIS.md"

```

---

## Theology

**Purpose:** A named shelf for sources that bear on **belief, practice, sacred narrative, ethics-as-tradition, or comparative religion** — without mixing them into geography/science/history lanes by default.

**How it works (schema-aligned):**
- Entries still use the normal **lanes** (`reference`, `canon`, `influence`) and **types** from [library-schema.md](../../docs/library-schema.md).
- Mark theological material by adding **`theology`** (and narrower tags if useful, e.g. `Christianity`, `myth-and-rite`) to **`scope`** so lookup and human scan can filter.
- Nothing here bypasses the **gated pipeline**: facts or claims about the companion’s beliefs belong in SELF via RECURSION-GATE; LIBRARY only holds **approved return-to sources** (books, articles, essays, video, etc.).

**Current entries:** **LIB-0135** — *The Simple Condition* (essay; `scope` includes `theology`).

---

## Physics, chemistry & biology

**Purpose:** One shelf for **physical and life sciences** — motion, matter, energy, reactions, living systems, genetics, and lab framing — so lookup does not split STEM by department unless you add finer tags.

**How it works (schema-aligned):**
- Entries keep normal **lanes** and **types** ([library-schema.md](../../docs/library-schema.md)).
- Tag **`scope`** with one or more of:
  - **`physics`** — forces, motion, energy, space, astronomy, flight  
  - **`chemistry`** — atoms, reactions, materials, mixtures  
  - **`biology`** — life, cells, body systems, ecology, DNA/genes  
- **`science`** still means mixed or general STEM.

**Current entries (examples):** **LIB-0003** — Usborne Science Encyclopedia (`scope` includes `physics`, `chemistry`, `biology`, `gravity`, `flight`, `genes`, `DNA`). Add more LIB rows with any of these tags as approved.

---

## History

**Purpose:** A named shelf for **chronology, civilizations, primary/secondary historical sources, and world-regional narrative** — without duplicating pure mythology-as-story unless the entry is history-forward (timelines, empires, documents).

**How it works (schema-aligned):**
- Entries keep normal **lanes** and **types**.
- Add **`history`** or **`world history`** (and tags like `ancient`, `Rome`, `China`, `civilizations`) to **`scope`**.
- Myth-heavy canon can still touch history; prefer this shelf when the **return-to reason** is historical context, not myth retell alone.

**Current entries (examples):** **LIB-0002** — Usborne World History Encyclopedia (`world history`, maps, time charts). **LIB-0132** — Civilization Memory Codex (`history`, civilizations, Rome, China, ancient). Add more with `scope: … history …` as approved.

---

## Metadata

```yaml
total_entries: 137
clone_source: "companion-self users/_template/self-library.md (2026-02-26)"
grace_mar_additions: "… LIB-0135 (Simple Condition), LIB-0136..0137 (CMC hybrid essays doors)"
maturity_levels: "1=young/all ages, 2=middle grade, 3=older/teen+"
last_updated: 2026-03-15
library_lanes: "reference, canon, influence"
taxonomy_note: "engagement_status replaces read_status; lookup_priority marks runtime lookup preference"
sections: "Entries · Theology · Physics/chemistry/biology · History (thematic shelves; tag scope) · Metadata"
```
