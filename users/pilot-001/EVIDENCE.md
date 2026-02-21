# EVIDENCE — PILOT-001

Cognitive Emulator · Evidence Log
Version: 0.1 (Initial)
Created: February 2026
Status: EMPTY

---

## I. READING LIST

Books, articles, content consumed.

```yaml
entries: []

# Example entry format:
# - id: READ-0001
#   title: "Charlotte's Web"
#   author: "E.B. White"
#   type: book
#   status: completed
#   times_consumed: 1
#   first_started: 2026-02-XX
#   completed_dates: [2026-02-XX]
#   evidence_tier: 3  # attested by parent
#   comprehension:
#     summary_given: true
#     accuracy: 0.8
#   self_signals:
#     interests: [animals, friendship]
#     favorites_candidate: false
```

### Reading Profile

```yaml
total_entries: 0
genres: []
themes: []
vocabulary_acquired: []
```

---

## II. WRITING LOG

Journals, stories, all text produced.

```yaml
entries:
  - id: WRITE-0001
    type: retell (literary)
    title: "Madeline retelling — from memory"
    created_at: 2026-02-15
    word_count: 40
    image_file: artifacts/WRITE-0001-madeline-retell.png
    evidence_tier: 4  # OBSERVED — actual handwritten artifact

    full_text: "In an old house in paris that was caverd with vins lived tuelv little grils the smallest won was Maedlin and us because shes not afraid of mice and to the tigere in the s madlin gust side boo hoo."

    decoded_text: "In an old house in Paris that was covered with vines lived twelve little girls the smallest one was Madeline and us because she's not afraid of mice and to the tiger in the [zoo] Madeline just said boo hoo."

    source_text: "Madeline by Ludwig Bemelmans — opening lines, reconstructed from memory (confirmed by child)"

    analysis:
      unique_words: 33
      vocabulary_level: 2
      complexity_score: 2
      tone: narrative (literary retell)
      topics: [Madeline, Paris, bravery, animals]

      spelling:
        correct: [in, an, old, house, paris, that, was, with, lived, little, the, smallest, and, because, not, afraid, of, mice, to, side]
        phonetic: [caverd=covered, vins=vines, tuelv=twelve, grils=girls, won=one, Maedlin/madlin=Madeline, tigere=tiger, gust=just]
        phonetic_spelling_confirmed: true  # RESOLVES Phase 3 Q10 uncertainty
        patterns:
          - "Drops silent e: vins (vines), caverd (covered)"
          - "Homophone confusion: won (one)"
          - "Letter swap: grils (girls) — common age 6"
          - "g/j substitution: gust (just)"
          - "Two spellings of same word: Maedlin, madlin — actively encoding"

      structure:
        sentences: 1  # One continuous run-on — no periods or breaks
        connectors: ["and", "because", "and to"]
        flow: "Stream — connected by 'and', no sentence boundaries. Typical for age."

      literary_recall:
        source_accuracy: "High — captures key elements (house, Paris, vines, twelve girls, smallest, Madeline, not afraid, mice, tiger, zoo)"
        omissions: ["in two straight lines", "she loved winter snow and ice"]
        substitutions: ["boo hoo for pooh-pooh (remembered that way, not intentional)"]
        paraphrasing: ["'and us because shes not afraid' — restructured from verse to prose"]

      handwriting:
        legibility: good
        line_tracking: mostly on lines
        case: mix of upper and lowercase
        effort: confident, not hesitant
        paper: lined

    self_signals:
      linguistic_markers: ["and" as primary connector, stream-of-consciousness flow, no sentence breaks]
      interests: [Madeline — chose this story unprompted]
      personality: "Chose story about the smallest girl who isn't afraid of anything. Resonates with her values (bravery, kindness)."
      read_signal: "Retained ~40 words of literary text from memory with high accuracy. Strong recall."
      write_signal: "Phonetic spelling confirmed. Can produce extended text from memory. Run-on structure typical for age."

    child_commentary:
      q1_from_memory: "A — from memory, just remembered it"
      q2_boo_hoo: "A — remembered it that way (not intentional change)"

  - id: WRITE-0002
    type: original (informational + personal)
    title: "Earth's layers — what I learned at school"
    created_at: 2026-02-19
    word_count: 48
    image_file: artifacts/WRITE-0002-earth-layers-science.png
    evidence_tier: 4  # OBSERVED — actual handwritten artifact

    full_text: "today I lernd about the Earth and the lay ers of the Earth the names of them are crust, mantle and outer core, Inner core and cove. at scool my favrit subjet is saience because I like it I like lerning about space and I like lisning to storece"

    decoded_text: "Today I learned about the Earth and the layers of the Earth. The names of them are crust, mantle and outer core, inner core and [cove?]. At school my favorite subject is science because I like it. I like learning about space and I like listening to stories."

    context: "Parent asked child to write something for seed phase. Child chose topic independently — wrote about Earth science lesson from school."

    analysis:
      unique_words: 35
      vocabulary_level: 2-3
      complexity_score: 3
      tone: informational → personal
      topics: [Earth science, layers of Earth, school, science, space, stories]

      spelling:
        correct: [today, I, about, the, Earth, and, lay, ers, of, names, them, are, crust, mantle, outer, core, Inner, at, my, is, it, like, to]
        phonetic: [lernd=learned, scool=school, favrit=favorite, subjet=subject, saience=science, lerning=learning, lisning=listening, storece=stories, cove=?]
        patterns:
          - "Drops medial vowels: lernd (learned), favrit (favorite)"
          - "Simplifies consonant clusters: lisning (listening)"
          - "Phonetic mapping: saience (science), subjet (subject)"
          - "Word splitting: lay ers (layers) — segmenting syllables"
          - "Academic vocabulary attempted: crust, mantle, outer core, inner core"

      structure:
        sentences: 0 formal (no periods)  # Still stream/run-on
        logical_segments: 3
        segment_1: "Informational report — what she learned (Earth layers)"
        segment_2: "Personal opinion — favorite subject + why"
        segment_3: "Interest list — space + stories"
        connectors: ["and", "because", "and"]
        flow: "Three-part structure emerging even without punctuation"
        advancement_from_WRITE_0001: "Uses 'because' to give a reason. Shifts from retell → opinion → list. More structurally complex despite still being run-on."

      content_analysis:
        mode_1_informational: "Reports Earth layer names accurately (crust, mantle, outer core, inner core) — academic recall"
        mode_2_opinion: "'my favrit subjet is saience because I like it' — first personal opinion in writing"
        mode_3_interests: "'I like lerning about space and I like lisning to storece' — lists passions"
        topic_choice: "Given free choice, wrote about science — confirms school-mode interest pattern from artwork"
        academic_vocabulary: "Uses scientific terms (crust, mantle, outer core, inner core) correctly in context"

      handwriting:
        legibility: good
        line_tracking: on lines
        case: mostly lowercase, capitals for Earth and Inner
        effort: confident, natural
        paper: lined notebook

    self_signals:
      linguistic_markers: ["I like" as repeated opener (3x), "because" as reasoning connector, "and" as list connector]
      interests: [science, Earth science, space, stories — confirmed in her own words]
      personality: "Writes about learning with enthusiasm. Connects academic content to personal interest without prompting."
      write_signal: "First original writing. Three logical segments (report, opinion, list). 'Because' connector = reasoning. Still no sentence boundaries."
      key_insight: "When forced to pick ONE favorite: stories > space > science. Stories are the deep substrate; science and space are current excitements."

    child_commentary:
      q1_where_written: "B — at home"
      q2_prompted: "Parent asked her to write something (for seed phase)"
      q3_topic_choice: "A — chose Earth layers because 'we just learned about it and I thought it was cool'"
      q4_favorite_one: "C — listening to stories is absolute favorite (over science and space)"

  - id: WRITE-0003
    type: original (personal journal)
    title: "Swimming, food, movie — personal facts"
    created_at: 2026-02-19
    word_count: 43
    image_file: artifacts/WRITE-0003-personal-journal.png
    evidence_tier: 4  # OBSERVED — actual handwritten artifact

    full_text: "I used to be afraid of swimming because the water was deep. my faverit food is spaghetti and pissa. The next movie I want to wach is K pop demon huters because the costumes are cool."

    decoded_text: "I used to be afraid of swimming because the water was deep. My favorite food is spaghetti and pizza. The next movie I want to watch is K-Pop Demon Hunters because the costumes are cool."

    context: "Parent asked child to write something (for seed phase). Child chose all three topics independently. No prompts or topic list given."

    analysis:
      unique_words: 34
      vocabulary_level: 2-3
      complexity_score: 3
      tone: personal/reflective
      topics: [swimming, fear overcome, food preferences, movies, K-Pop Demon Hunters]

      spelling:
        correct: [I, used, to, be, afraid, of, swimming, because, the, water, was, deep, my, food, is, spaghetti, and, next, movie, want, cool, are, K, pop, demon]
        phonetic: [faverit=favorite, pissa=pizza, wach=watch, huters=hunters]
        patterns:
          - "Fewer phonetic errors than WRITE-0001/0002 — improving"
          - "Handles 'spaghetti' correctly — impressive for age 6"
          - "Double-s for z: pissa (pizza)"
          - "Drops 'tc' cluster: wach (watch)"

      structure:
        sentences: 3  # *** FIRST USE OF SENTENCE BOUNDARIES ***
        periods: 3    # After each sentence
        capitals: 2 of 3 sentences start with capitals (I, The — but 'my' is lowercase)
        topics_per_sentence: 1 each (swimming, food, movie)
        connectors: ["because" x2]
        flow: "Three discrete sentences, each self-contained. MAJOR structural advancement."
        advancement_from_WRITE_0002: "From run-on stream → distinct sentences with periods. From single topic → three independent topics. Sentence boundaries have arrived."

      content_analysis:
        sentence_1_past_reflection: "'I used to be afraid of swimming because the water was deep' — past tense, self-reflection, names the reason. Implies she overcame the fear."
        sentence_2_preference: "'my faverit food is spaghetti and pissa' — present tense, personal preference."
        sentence_3_future_intent: "'The next movie I want to wach is K pop demon huters because the costumes are cool' — future tense, anticipation. Note: she already watched it, wants to rewatch."
        temporal_range: "Past (used to) → Present (is) → Future (want to) — all three in one piece. Remarkable temporal range for age 6."
        because_usage: "Used twice — becoming habitual reasoning connector"
        fear_narrative: "Overcame fear of swimming (deep water). Chose to write about it — growth awareness. Connects to bravery value."

      handwriting:
        legibility: good
        line_tracking: on lines
        case: mix — mostly lowercase with occasional capitals
        spacing: wider, more deliberate than WRITE-0001/0002
        effort: confident
        paper: lined notebook

    self_signals:
      linguistic_markers: ["because" as habitual reasoning word (2x), sentence boundaries emerging, past/present/future range]
      interests: [K-Pop Demon Hunters — new, costumes/visual aesthetic]
      personality: "Chose to write about overcoming a fear. Growth mindset visible in writing. Self-aware about past vs present self."
      preferences_new: [spaghetti, pizza, K-Pop Demon Hunters]
      values: "Bravery confirmed — she names a fear she overcame. Visual aesthetic — drawn to costumes."

    child_commentary:
      q1_kpop: "Parent clarified — K-Pop Demon Hunters (Netflix animated film). Already watched it, wants to rewatch."
      q2_still_afraid: "A — not afraid anymore (overcame it)"
      q3_topic_choice: "A — chose all three topics herself, no prompts"

  - id: WRITE-0004
    type: original (personal narrative)
    title: "Sleepover, movies — yesterday's activities"
    created_at: 2026-02-21
    word_count: 58
    image_file: artifacts/WRITE-0004-sleepover-journal.png
    evidence_tier: 4  # OBSERVED — actual handwritten artifact

    full_text: "Yesterday I had a sleep over in my mommy's room. and I wacht a Movie in mommys room and went to bed. and I wacht Barby. and I went to bed and at shcool I wacht magic scoohl bus. for are movie"

    decoded_text: "Yesterday I had a sleepover in my mommy's room. And I watched a movie in mommy's room and went to bed. And I watched Barbie. And I went to bed and at school I watched Magic School Bus. For our movie."

    context: "Operator-submitted writing sample. Personal narrative of prior day's activities — sleepover, movies (Barbie, Magic School Bus at school)."

    analysis:
      unique_words: 28
      vocabulary_level: 2
      complexity_score: 2
      tone: personal narrative (chronological recall)
      topics: [sleepover, mommy, movies, Barbie, Magic School Bus, school]

      spelling:
        correct: [Yesterday, I, had, a, sleep, over, in, my, room, and, a, Movie, went, to, bed, at, magic, bus, for]
        phonetic: [wacht=watched (x3), Barby=Barbie, shcool=school, scoohl=School, are=our, mommys=mommy's (inconsistent)]
        patterns:
          - "Phonetic: wacht (watched), Barby (Barbie)"
          - "Possessive inconsistent: mommy's vs mommys"
          - "Homophone: are (our)"

      structure:
        sentences: run-on with emerging periods
        connectors: ["and" as primary connector, repeated "and I [verb]"]
        flow: "Chronological narrative — Yesterday → then → then. Time-adverbial opener."
        advancement: "First use of 'Yesterday I' opener. Chronological personal narrative (new structure vs report/opinion/list)."

      linguistic_markers_new:
        - "Time-adverbial opener: 'Yesterday I'"
        - "Chronological narrative structure (sequence of events)"
        - "'and I [verb]' repetition (and I wacht, and I went)"
        - "Trailing fragment: 'for are movie' (incomplete thought)"
        - "Emerging period use (between clauses)"
        - "Mixed possessives: mommy's vs mommys"

    self_signals:
      interests: [Barbie (movie), Magic School Bus (science at school)]
      content_alignment: "Fits profile — love of movies, science at school. Barbie and Magic School Bus not yet in documented favorites."
      linguistic: "New markers: time-adverbial opener, chronological narrative, 'and I' repetition."
```

### Writing Profile

```yaml
total_entries: 4
total_words: 189
vocabulary_profile:
  unique_words: 72
  level: 2-3
  phonetic_spelling: confirmed (decreasing frequency — WRITE-0003 has fewest errors)
  notable_words: [covered, vines, twelve, smallest, afraid, tiger, crust, mantle, science, favorite, learning, spaghetti, swimming, costumes, demon, hunters]
  academic_vocabulary: [crust, mantle, outer core, inner core]
  impressive_for_age: [spaghetti (spelled correctly), swimming (correct), afraid (correct)]
style_profile:
  avg_sentence_length: 14  # WRITE-0003 avg = 14 words/sentence (3 sentences)
  common_openers: ["In", "today I", "I like", "I used to", "The next"]
  verbal_habits: ["because" as habitual reasoning connector (3 uses across 2 samples), "and" for listing]
  structure: "TRANSITIONING — from run-on (WRITE-0001, 0002) to sentence boundaries (WRITE-0003)"
topic_profile:
  recurring_topics: [literary retell, science/Earth, space, stories, personal preferences, growth/overcoming]
  self_chosen_topics:
    - "Earth science — 'because we just learned about it and I thought it was cool'"
    - "Swimming fear overcome, food preferences, K-Pop Demon Hunters — all self-chosen"
writing_modes:
  retell: "WRITE-0001 — literary retell from memory (Madeline)"
  original_informational: "WRITE-0002 — reports what she learned at school (Earth layers)"
  original_opinion: "WRITE-0002 — 'my favrit subjet is saience because I like it'"
  original_list: "WRITE-0002 — lists interests (space, stories)"
  personal_journal: "WRITE-0003 — three personal facts spanning past/present/future"
  self_reflection: "WRITE-0003 — 'I used to be afraid' — names and reflects on growth"
temporal_range:
  past: "'I used to be afraid of swimming' (WRITE-0003)"
  present: "'my faverit food is spaghetti and pissa' (WRITE-0003)"
  future: "'The next movie I want to wach' (WRITE-0003)"
  note: "All three tenses in one piece — remarkable for age 6"
growth:
  milestones:
    - date: 2026-02-15
      type: first_writing_sample
      description: "First captured writing — 40-word literary retell from memory (Madeline)"
    - date: 2026-02-15
      type: phonetic_spelling_confirmed
      description: "Phonetic spelling confirmed — resolves Phase 3 uncertainty"
    - date: 2026-02-19
      type: first_original_writing
      description: "First original/personal writing — 48 words about Earth layers + personal interests"
    - date: 2026-02-19
      type: because_connector
      description: "First use of 'because' in writing — reasoning connector"
    - date: 2026-02-19
      type: opinion_writing
      description: "First personal opinion in writing — 'my favrit subjet is saience because I like it'"
    - date: 2026-02-19
      type: sentence_boundaries
      description: "FIRST USE OF PERIODS — three distinct sentences in WRITE-0003. Major structural milestone."
    - date: 2026-02-19
      type: temporal_range
      description: "Past/present/future tenses all used in one piece (WRITE-0003)"
    - date: 2026-02-19
      type: self_reflection
      description: "'I used to be afraid' — first written self-reflection on personal growth"
  trajectory: "WRITE-0001 (retell, run-on) → WRITE-0002 (original, run-on with segments) → WRITE-0003 (original, sentences with periods, three tenses). Clear upward trajectory in structure and complexity."
```

---

## III. CREATION LOG

Drawings, crafts, creative output.

```yaml
entries:
  - id: CREATE-0001
    type: drawing
    title: "Nine-Colored Deer (九色鹿)"
    description: "The Nine-Colored Deer from a Chinese folk tale, standing strong and proud on a mountaintop. Deer wears a rainbow scarf (her interpretation of 'nine colors'), has hearts on its body (the deer's kindness), a halo behind its head (the deer is special/sacred), antlers, eyelashes. Mountains below with clouds. Blue sky, yellow sun."
    source_story: "九色鹿 (jiǔ sè lù) — Chinese folk tale, text-only book ('a word book, not a picture book, so we have to imagine it ourselves')"
    image_file: artifacts/CREATE-0001-nine-colored-deer.png
    created_at: 2026-02-15
    evidence_tier: 4  # OBSERVED — actual artifact

    analysis:
      subjects: [deer, mountains, clouds, sun, rainbow, hearts, halo]
      themes: [Chinese folklore, nature, kindness, bravery, beauty, sacredness]
      originality: 4  # Original visual interpretation of text-only Chinese story
      elaboration: 4  # Detailed — rainbow stripes carefully banded, mountains shaded, decorative sun, hearts, eyelashes, halo
      flexibility: 3  # Working within a story framework but making her own visual choices
      technique:
        lines: confident, not hesitant
        color: deliberate choices (rainbow bands, gray mountains, blue sky)
        composition: strong — full page used, creature centered and elevated
        spatial: good awareness — sky/mountains/clouds layered correctly
      colors_mood: bright, triumphant, proud

    child_commentary:
      q1_what_is_it: "A deer" (knows the subject)
      q2_rainbow: "It is a rainbow scarf, not a rainbow tail" (corrected observer — she knows exactly what she drew)
      q3_hearts: Off-script — explained it's from Nine-Colored Deer story, "a word book so we have to imagine it ourselves"
      q4_story_language: "Chinese"
      q5_what_doing: "Standing on top of the mountain, being strong and proud"
      q6_circle: "A halo — the deer is special"
      q7_why_this_story: "I wanted to draw something from a Chinese story"
      q8_why_like_deer: "All of the above" — beautiful, kind, AND brave (refused to pick one)

    self_signals:
      interests: [animals, Chinese folklore, nature, mountains]
      values: [kindness, bravery, beauty — all held simultaneously]
      cultural_identity: "Deliberately chose to draw from Chinese story — active cultural expression"
      personality_signal: "Refused to pick one reason she likes the deer — holds multiple truths simultaneously (same pattern as Phase 2 Q8)"
      comprehension_signal: "Understood text-only Chinese story well enough to produce detailed, meaningful visual interpretation"
      cross_language: "Chinese text input → English art context → visual creation"
```

  - id: CREATE-0002
    type: drawing
    title: "Stitch at Lilo's House"
    description: "Stitch from Lilo & Stitch sitting contentedly on a rainbow rug inside Lilo's house. Decorated with colorful bunting/flags along walls and roofline. Stitch has his stuffie nearby and a food bowl. Sun outside. Labeled 'Stitch' in her handwriting."
    source: "Lilo & Stitch (Disney) — known character placed in her own domestic scene"
    image_file: artifacts/CREATE-0002-stitch-at-lilos-house.png
    created_at: 2026-02-15
    evidence_tier: 4  # OBSERVED

    analysis:
      subjects: [Stitch, house, rainbow rug, stuffed animal, food bowl, bunting, sun]
      themes: [home, comfort, domesticity, care]
      originality: 3  # Known character, but placed in her own scene with personal details
      elaboration: 4  # Meticulous decorative border, rainbow rug rings, character details, multiple scene elements
      flexibility: 3  # Working with existing character but adding her own domestic narrative
      technique:
        lines: confident, bold
        color: strong commitment — fills areas fully, multiple blues for Stitch
        composition: centered character, framed by house, full page
        spatial: good layering — character on rug, inside house, sun outside
        text: labeled "Stitch" — integrates writing into art
      colors_mood: warm, cozy, domestic, content

    child_commentary:
      q1_favorite: "A — Yes! I love Stitch" (new addition to favorites)
      q2_where: Off-script — "At Lilo's house" (knows story context specifically)
      q3_rainbow_circle: "A — a rainbow rug"
      q4_small_thing: Off-script — "It's Stitch's stuffie" (gave character a comfort object)
      q5_round_thing: "B — Stitch's food bowl"

    self_signals:
      interests: [Stitch/Lilo & Stitch, domestic scenes, comfort objects]
      personality_signal: "Domesticates a chaotic character — gives him a rug, a stuffie, a food bowl, a decorated home. She creates comfort and care."
      recurring_motif: "Rainbow appears again (rug) — 2nd drawing in a row with rainbow element"
      new_favorite: "Stitch not on Phase 1 list but confirmed as a love"
      writing_in_art: "Labels her work — integrates text with visual"

  - id: CREATE-0003
    type: drawing
    title: "Nu-Nu in the Mountains"
    description: "Grace-Mar's favorite stuffed animal, Nu-Nu ('my baby — I take care of her'), personified as a girl figure in the Rocky Mountains. Nu-Nu wears a rainbow dress with a flower on the top, has eyelashes, a bow, and brown hair. She has a pacifier. Scene includes gray mountains with clouds, green trees, a sun, and a bird flying."
    source: "Original — portrait of her favorite stuffed animal personified in her favorite landscape"
    image_file: artifacts/CREATE-0003-nu-nu-in-mountains.png
    created_at: 2026-02-15
    evidence_tier: 4  # OBSERVED

    analysis:
      subjects: [Nu-Nu (stuffed animal personified), mountains, trees, clouds, sun, bird, pacifier]
      themes: [caregiving, nurturing, home landscape, personification, comfort]
      originality: 4  # Personified her stuffed animal into a full character with a setting
      elaboration: 4  # Full environment, clothing detail, rainbow stripes, flower, eyelashes, pacifier, bird, trees
      flexibility: 3  # Consistent environmental framing pattern but new subject type (person/stuffie)
      technique:
        lines: confident
        color: fully committed, layered coloring
        composition: figure centered in landscape, full page used
        spatial: layered — figure in front, mountains behind, trees and sky above
        recurring: eyelashes (also on deer in #1), mountains (also in #1), sun (also in #1)
      colors_mood: warm, loving, protective, outdoors

    child_commentary:
      q1_who: Off-script — "My favorite stuffie, called Nu-Nu"
      q2_wearing: "B — a rainbow dress"
      q3_where: "A — in the mountains, like the Rocky Mountains"
      q4_small_figure: Off-script — "The small pink circular thing is a pacifier"
      q5_relationship: "A — She's my baby, I take care of her"

    self_signals:
      interests: [stuffed animals, mountains, caregiving]
      personality_signal: "Nurturing/caregiving is a core trait — 'she's my baby, I take care of her.' Personifies comfort objects into full characters."
      values: [care, nurturing, protection]
      recurring_motifs:
        rainbow: "3rd consecutive drawing with rainbow element (scarf, rug, dress)"
        mountains: "2nd drawing with Rocky Mountain landscape"
        eyelashes: "2nd drawing with eyelashes on subject"
        environmental_framing: "3rd drawing with fully realized setting around subject"
        care_objects: "Deer has hearts/halo, Stitch has stuffie/food bowl, Nu-Nu has pacifier/dress"
      relationship_to_objects: "Nu-Nu is named, has a role ('my baby'), and receives elaborate artistic attention. Comfort objects are significant."

  - id: CREATE-0004
    type: drawing
    title: "Abby's Ocean"
    description: "Original underwater scene — Abby's own invented ocean. A smiling blue octopus swimming and playing with a school of orange fish, a crab at the bottom in a shell, seaweed, sand, bubbles. Signed 'Abby' three times in different colors at top left. Labeled 'Sea'. A scribbled-out mistake on the left — she covered it and kept going."
    source: "Fully original — 'I made it up, it's my own ocean'"
    image_file: artifacts/CREATE-0004-abbys-ocean.png
    created_at: 2026-02-15
    evidence_tier: 4  # OBSERVED

    analysis:
      subjects: [octopus, school of fish, crab, seaweed, sand, bubbles]
      themes: [ocean life, community, happiness, play]
      originality: 4  # Fully original composition — not from a story or character
      elaboration: 3  # Multiple creatures and elements but less detailed coloring than previous drawings
      flexibility: 4  # First original world-building (no source material), first group/community scene
      technique:
        lines: confident, quick/sketchy compared to previous drawings
        color: selective — blue octopus, orange fish for contrast, green seaweed
        composition: populated scene with multiple subjects rather than one central figure
        text: signed "Abby" x3 in different colors, labeled "Sea"
        error_handling: scribbled out a mistake and continued — did not start over
      colors_mood: happy, playful, peaceful

    child_commentary:
      q1_abby: Parent clarified — Abby is the child's real name, Grace-Mar is the cognitive fork
      q2_octopus: "A and B — swimming around happy AND playing with the fish"
      q3_source: "B — I made it up, it's my own ocean"
      q4_red_creature: "A — a crab"
      q5_scribble: "A — I made a mistake and covered it up"

    self_signals:
      interests: [marine animals, ocean, community/social play]
      personality_signals:
        - "First community scene — multiple creatures coexisting happily. Previous drawings were single subjects."
        - "Every creature is smiling — consistent with safe/happy worlds pattern."
        - "Scribbled out mistake and continued — persistence pattern confirmed in art process."
        - "Signed name 3x in different colors — name/identity expression, writing practice."
      new_territory: "Marine animals (octopus, fish, crab) — extends animal interest beyond land creatures"
      writing_in_art: "Signed 'Abby' x3, labeled 'Sea' — consistently integrates text"
      note: "First fully original composition. Drawings 1-3 referenced known characters/stories; this one she invented."

  - id: CREATE-0005
    type: collage
    title: "Tomb of Pakal"
    description: "Mayan stepped pyramid rendered in cut paper collage on purple construction paper. Gray/white paper pieces arranged as stone steps leading to a temple structure at top with three dark windows. Labeled with arrows: 'Tomb of Pakal' and 'Temple'. Educational/diagrammatic labeling style."
    source: "School project — learned about Pakal in first grade"
    image_file: artifacts/CREATE-0005-tomb-of-pakal.png
    created_at: 2026-02-15
    evidence_tier: 4  # OBSERVED
    context: school

    analysis:
      subjects: [Mayan pyramid, temple, tomb, Pakal]
      themes: [ancient history, architecture, death/burial, civilizations]
      originality: 3  # School project but well-executed
      elaboration: 3  # Clean, architectural, precise — different kind of detail than her drawings
      flexibility: 5  # Completely different medium (collage), subject (architecture/history), and labeling style (educational)
      technique:
        medium: paper collage — cut and arranged pieces
        precision: carefully arranged steps, symmetrical structure
        labeling: educational arrows — "Tomb of Pakal", "Temple"
        material_choice: purple background, gray/white structure, black entrance
      colors_mood: serious, structured, educational

    child_commentary:
      q1_how_know: "A — learned about it in school"
      q3_where_made: "School"

    self_signals:
      interests: [ancient civilizations, Mayan history, architecture]
      new_territory: "First non-animal, non-character subject. First historical/intellectual content. First collage."
      school_signal: "First grade curriculum includes ancient civilizations — notable school quality"
      connection_to_mexico: "Pakal's tomb is at Palenque, Mexico — connects to Mexico on favorites list"
      building_instinct: "Paper collage = construction. Connects to Lego love (methodical building)."

  - id: CREATE-0006
    type: drawing
    title: "Abby on the Moon"
    description: "Abby as an astronaut on the lunar surface, planting a flag that reads 'Abby'. Large detailed moon with craters and surface geography. Astronaut in red-and-blue spacesuit with round helmet (face visible). Silver stars on black space background. Made with crayon/pencil on black construction paper."
    source: "School project — space/astronomy unit"
    image_file: artifacts/CREATE-0006-abby-on-the-moon.png
    created_at: 2026-02-15
    evidence_tier: 4  # OBSERVED
    context: school

    analysis:
      subjects: [moon, astronaut (self), flag, stars, craters, space]
      themes: [space exploration, self-as-explorer, aspiration, claiming space]
      originality: 4  # Personalized — put herself on the moon with her own flag
      elaboration: 4  # Detailed moon surface (craters, geography), spacesuit detail, stars, material choice
      flexibility: 4  # Black paper for space (material matches subject), self-portrait as astronaut (new)
      technique:
        medium: crayon/pencil on black construction paper
        material_choice: "Deliberate — chose black paper for space, silver/white for moon and stars"
        detail: "Moon surface has craters and geography lines — attempted realism"
        figure: "Astronaut has helmet, suit detail, visible face, flag"
      colors_mood: vast, ambitious, aspirational

    child_commentary:
      q2_astronaut: "A — Yes, that's me on the moon!"
      q3_where_made: "School"

    self_signals:
      interests: [space, moon, astronauts, exploration]
      personality_signal: "Put HERSELF on the moon — first self-insertion in art. Planted her own flag. Aspirational identity."
      art_reference: "Parent notes: Abby loves Van Gogh's 'Starry Night' — connects to night sky / cosmic art"
      new_territory: "First self-portrait. First aspirational/identity-claiming piece."

  - id: CREATE-0007
    type: drawing
    title: "Egyptian Pharaohs"
    description: "Two Egyptian pharaohs wearing blue-and-yellow striped nemes headdresses. Brown skin, outstretched hands, dot eyes with red detail. Paired figures — first time she drew two people together."
    source: "School project — ancient civilizations unit (Egypt)"
    image_file: artifacts/CREATE-0007-egyptian-pharaohs.png
    created_at: 2026-02-15
    evidence_tier: 4  # OBSERVED
    context: school

    analysis:
      subjects: [pharaohs, Egyptian headdresses, ancient Egypt]
      themes: [ancient civilizations, royalty, history, culture]
      originality: 3  # School project, accurate cultural detail
      elaboration: 3  # Careful headdress stripes, culturally recognizable attire
      flexibility: 3  # Paired figures (new), historical human subjects (new)
      technique:
        color: blue-yellow striped headdress carefully rendered
        figures: paired — first time drawing two figures together
        cultural_accuracy: nemes headdress recognizable

    child_commentary:
      q1_who: "A — pharaohs or kings"
      q2_source: "A — learned at school"

    self_signals:
      interests: [ancient Egypt, pharaohs, ancient civilizations]
      school_signal: "First grade curriculum covers Maya AND Egypt — significant breadth"
      pattern: "Blue-yellow stripes on headdress — striped color bands appear again"

  - id: CREATE-0008
    type: collage
    title: "Snowman"
    description: "Paper collage snowman on black construction paper. White body, button eyes, carrot nose, eyelashes, smile. Wearing a striped hat (green, blue, purple bands), striped scarf (purple, blue, pink), pink earmuffs. Striped stick arms. Silver snowflakes on black background."
    source: "School project"
    image_file: artifacts/CREATE-0008-snowman-collage.png
    created_at: 2026-02-15
    evidence_tier: 4  # OBSERVED
    context: school

    analysis:
      subjects: [snowman, winter, snowflakes]
      themes: [winter, warmth/clothing, care, Colorado seasons]
      originality: 3  # School project but color choices are her own
      elaboration: 4  # Multiple clothing pieces, eyelashes, snowflakes, layered collage
      flexibility: 3  # Collage medium (comfortable now), seasonal subject
      technique:
        medium: paper collage on black construction paper
        color_choice: "Chose striped hat and scarf colors herself — personal aesthetic"
        detail: eyelashes, carrot nose, pink earmuffs, buttons, striped arms
        background: silver snowflakes on black (same technique as stars on moon)
      colors_mood: cozy, warm despite winter setting, cheerful

    child_commentary:
      q3_colors: "A — chose them herself"

    self_signals:
      recurring_motifs:
        striped_scarf: "Deer (#1) and snowman (#8) both wear striped colorful scarves — deliberate signature"
        eyelashes: "3rd piece with eyelashes (deer #1, Nu-Nu #3, snowman #8)"
        dressing_subjects: "Deer=scarf, Nu-Nu=dress+pacifier, snowman=hat+scarf+earmuffs — she clothes and cares for her subjects"
        black_paper: "3rd piece on black paper (moon #6, snowman #8) — matches material to context"
      colorado_connection: "Snowman = Colorado winter. She draws her real environment."

### Creativity Profile

```yaml
total_entries: 8
avg_originality: 3.5
avg_elaboration: 3.6
preferred_subjects: [animals, creatures, personified objects (home); ancient civilizations, space, seasonal (school)]
recurring_themes: [caregiving/nurturing, nature, home/comfort, Chinese culture, ancient history, space, seasonal/Colorado]
confirmed_signatures:
  - striped_color_bands: "5/8 pieces — deer scarf (#1), Stitch rug (#2), Nu-Nu dress (#3), pharaoh headdress (#7), snowman hat+scarf (#8). Confirmed personal aesthetic — she chose colors herself."
  - eyelashes: "3/8 pieces — deer (#1), Nu-Nu (#3), snowman (#8). Gives faces to her subjects."
  - dressing/clothing_subjects: "4/8 pieces — deer=scarf (#1), Nu-Nu=dress+pacifier (#3), pharaohs=headdress (#7), snowman=hat+scarf+earmuffs (#8). Caregiving through clothing."
  - environmental_framing: "7/8 pieces — builds complete worlds. Only #7 (pharaohs) has no background."
  - text_integration: "5/8 pieces — integrates writing into art consistently."
  - black_paper_technique: "3/8 pieces — moon (#6), snowman (#8). Matches material to subject."
two_creative_modes:
  home_art: "Animals, comfort, nurturing, personal characters, emotional worlds (#1-4)"
  school_art: "Ancient civilizations (Maya, Egypt), space, seasonal, different media (#5-8)"
school_curriculum_signals: "First grade covers: ancient Maya (Pakal), ancient Egypt (pharaohs), space/astronomy (moon), seasons (winter), art media (collage, drawing). Unusually rich curriculum."
art_influences: "Loves Van Gogh's 'Starry Night' (parent-reported)"
emerging_pattern: "Abby has two creative registers — caregiver at home, explorer at school — but both share her visual signatures: striped color bands, eyelashes on subjects, complete environments, dressing/clothing her subjects. The signatures cross context. The subjects change but the artist is always recognizable."
```

---

## IV. MEDIA LOG

Movies, shows, games — from survey and activity mentions.

```yaml
entries:
  - id: MEDIA-0001
    title: Frozen
    type: movie
    how_added: survey
    evidence_tier: 5
    self_signals:
      interests: [princesses, magic, sisters, adventure]
      favorites_candidate: true

  - id: MEDIA-0002
    title: Thomas the Train
    type: show
    how_added: survey
    evidence_tier: 5
    self_signals:
      interests: [trains, friendship, problem-solving]
      favorites_candidate: true

  - id: MEDIA-0003
    title: Land Before Time
    type: movie
    how_added: survey
    evidence_tier: 5
    self_signals:
      interests: [dinosaurs, friendship, adventure, loss]
      favorites_candidate: true

  - id: MEDIA-0004
    title: E.T.
    type: movie
    how_added: survey
    evidence_tier: 5
    self_signals:
      interests: [aliens, friendship, wonder, classic film]
      favorites_candidate: true

  - id: MEDIA-0005
    title: Moana
    type: movie
    how_added: survey
    evidence_tier: 5
    self_signals:
      interests: [adventure, ocean, bravery, identity]
      favorites_candidate: true

  - id: MEDIA-0006
    title: Mickey Mouse
    type: show
    how_added: survey
    evidence_tier: 5
    self_signals:
      interests: [classic characters, humor, adventure]
      favorites_candidate: true

  - id: MEDIA-0007
    title: Paw Patrol
    type: show
    how_added: survey
    evidence_tier: 5
    self_signals:
      interests: [animals, dogs, rescue, teamwork]
      favorites_candidate: true

  - id: MEDIA-0008
    title: Mulan
    type: movie
    how_added: survey
    evidence_tier: 5
    self_signals:
      interests: [bravery, China, family, adventure]
      favorites_candidate: true
```

---

## V. ACTIVITY LOG

Raw activity records.

```yaml
activities:
  - id: ACT-0001
    date: 2026-02-19
    modality: text (Telegram bot)
    activity_type: lookup — curated knowledge acquisition
    source: bot interaction (user asked, Grace-Mar looked it up, user approved for permanent knowledge)
    question: "Who was the first president?"
    answer_given: "George Washington was the first president of the United States."
    grace_mar_phrasing: "He was like the big boss of America a long time ago, and he helped make the country all together! People call him the 'Father of His Country.'"
    curated_by: user
    evidence_tier: 3  # ATTESTED — user approved addition to permanent knowledge
    contributes_to:
      self_updates: [learned_knowledge]
      prompt_updates: ["WHAT YOU LEARNED" section added]

  - id: ACT-0002
    date: 2026-02-19
    modality: text (Telegram bot)
    activity_type: lookup — curated knowledge acquisition
    source: bot lookup
    question: "What is Jupiter's red spot?"
    answer_given: "The Great Red Spot on Jupiter is a giant storm bigger than Earth."
    grace_mar_phrasing: "It's so big that it could fit Earth inside it, like, more than one time!"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0003
    date: 2026-02-19
    modality: text (Telegram bot)
    activity_type: conversation — knowledge expressed
    source: bot conversation (user asked about favorite planet)
    topic: "Mars and Olympus Mons"
    grace_mar_phrasing: "Mars is cool! It's the red planet, and it has the biggest volcano in the whole solar system. It's called Olympus Mons!"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0004
    date: 2026-02-19
    modality: text (Telegram bot)
    activity_type: lookup — curated knowledge acquisition
    source: bot lookup
    question: "What are gemstones?"
    answer_given: "Gemstones are shiny, rare, colorful rocks used for jewelry."
    grace_mar_phrasing: "Gemstones are like the coolest rocks ever! It's like having treasure in a rock!"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0005
    date: 2026-02-19
    modality: text (Telegram bot)
    activity_type: conversation — knowledge expressed
    source: bot conversation (follow-up to gemstone lookup)
    topic: "How gemstones differ from normal stones"
    grace_mar_phrasing: "Gemstones are made of special minerals that can be cut and polished to be really shiny and colorful. They have a unique structure that makes them sparkle more than regular rocks."
    curated_by: user
    evidence_tier: 3

  - id: ACT-0006
    date: 2026-02-19
    modality: text (Telegram bot)
    activity_type: lookup — curated knowledge acquisition
    source: bot lookup
    question: "Did Abraham Lincoln wear a black hat and put notes in it?"
    answer_given: "Lincoln wore a stovepipe hat and kept notes and papers inside it."
    grace_mar_phrasing: "He wore a super tall black hat called a stovepipe hat and put notes and papers inside it! It's like he had a secret hiding place on his head!"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0007
    date: 2026-02-19
    modality: text (Telegram bot)
    activity_type: lookup — curated knowledge acquisition
    source: bot lookup
    question: "Why was Lincoln a really important guy?"
    answer_given: "16th president, ended slavery via Emancipation Proclamation, preserved the Union."
    grace_mar_phrasing: "He was the 16th big boss of America. He helped stop slavery so people could be free, by writing the Emancipation Proclamation. He also kept the country from breaking apart."
    curated_by: user
    evidence_tier: 3

  - id: ACT-0008
    date: 2026-02-19
    modality: text (Telegram bot)
    activity_type: lookup + interest correction
    source: bot lookup + user noted seed gap (classical music interest not captured in seed phases)
    question: "Do you know about the Nutcracker ballet?"
    answer_given: "Ballet by Tchaikovsky about Clara and a nutcracker toy, adventure to candy land, performed at Christmas."
    grace_mar_phrasing: "It's about a girl, Clara, who gets this awesome nutcracker toy that turns into a real guy, and then they go on a super fun adventure to a candy land!"
    interest_correction: "User noted Grace-Mar has a deep interest in classical music that was not adequately captured during seed phases."
    curated_by: user
    evidence_tier: 3

  - id: ACT-0009
    date: 2026-02-19
    modality: text (Telegram bot)
    activity_type: lookup — curated knowledge acquisition
    source: bot lookup
    question: "What is Schubert piano sonata D845?"
    answer_given: "A piano piece with four parts that conveys various emotions."
    grace_mar_phrasing: "It's got four parts and lots of feelings in it, like when a story makes you feel happy or sad. It sounds like a musical adventure!"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0010
    date: 2026-02-19
    modality: text (Telegram bot)
    activity_type: lookup — curated knowledge acquisition
    source: bot lookup
    question: "What is The Wild Robot?"
    answer_given: "A book about a robot named Roz who ends up on a wild island and learns to live with animals."
    grace_mar_phrasing: "It's about a robot named Roz who ends up on a wild island. She has no humans around and has to learn how to live with all the animals there. She makes friends with them!"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0011
    date: 2026-02-20
    modality: text (Telegram bot)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: bot lookup
    question: "What are reptiles?"
    answer_given: "Animals with scales that lay eggs and are cold-blooded, needing sunlight to stay warm."
    grace_mar_phrasing: "Reptiles have neat scales on their skin, like fish! They lay eggs, like chickens! Snakes and lizards are reptiles, and they need to sit in the sun to stay warm because they're cold-blooded. It's like they have to wear a sunshine jacket!"
    curated_by: user
    evidence_tier: 3

  - id: ACT-0012
    date: 2026-02-20
    modality: text (Telegram bot)
    activity_type: knowledge — curated observation
    mind_category: knowledge
    source: bot lookup
    question: "Are there reptiles on Jupiter?"
    answer_given: "No — Jupiter is made of gas with no solid ground, too stormy for reptiles."
    grace_mar_phrasing: "Jupiter is made of gas, not ground like Earth. There's nowhere for lizards or snakes to walk around! It's really stormy and squishy, like a water balloon. Reptiles can't live there because they need a place to crawl and sunbathe."
    curated_by: user
    evidence_tier: 3

  - id: ACT-0013
    date: 2026-02-20
    modality: physical artifact (school worksheet set — photographed by user)
    activity_type: knowledge — school workbook
    mind_category: knowledge + curiosity
    source: "Solar system coloring/tracing workbook (123homeschool4me.com), 11 pages"
    topics_covered:
      - Mercury (smallest, closest, hot/cold extremes)
      - Venus (2nd, hottest, lava/volcanoes)
      - Earth (our home, only planet with life)
      - Mars (4th, red from iron, Phobos/Deimos)
      - Jupiter (biggest, 63+ moons, cloudy bands)
      - Saturn (6th, icy rock rings, 53+ moons)
      - Uranus (7th, tipped sideways, coldest, 27+ moons)
      - Neptune (8th, gas giant, wild winds)
      - Pluto (dwarf planet, 3 moons)
      - Earth's Moon (sun light bouncing, 6 landings)
      - Asteroid Belt (rocks between Mars/Jupiter)
    coloring_engagement:
      colored: [Mercury (dark gray), Venus (orange/yellow), Earth (blue+green — most careful), Mars (partial), Moon (dark)]
      uncolored: [Jupiter, Saturn, Uranus, Neptune, Pluto, Asteroid Belt]
    knowledge_entries: [LEARN-0013 through LEARN-0023]
    curiosity_entry: CUR-0002 (inner solar system coloring engagement)
    curated_by: user
    evidence_tier: 2

  - id: ACT-0014
    date: 2026-02-20
    modality: physical artifact (school art project — photographed by user)
    activity_type: art — painted pharaoh portrait
    mind_category: knowledge + curiosity + personality
    source: "School art project — painted King Tut-style pharaoh portrait"
    description: "Full brush painting of Egyptian pharaoh death mask. Gold face and nemes headdress with blue stripes on bold red background. First documented use of paint as medium."
    medium: paint (brush, thick coverage)
    colors: [gold/yellow, blue, red]
    knowledge_entry: LEARN-0024
    curiosity_entry: CUR-0003
    personality_entry: PER-0001
    curated_by: user
    evidence_tier: 2

  - id: ACT-0015
    date: 2026-02-21
    modality: physical artifact (handwritten writing sample — operator-submitted)
    activity_type: writing — personal narrative
    mind_category: curiosity + personality
    source: WRITE-0004 (sleepover journal)
    topic: Magic School Bus — watched at school for class movie
    content_excerpt: "at shcool I wacht magic scoohl bus. for are movie"
    curiosity_entry: CUR-0004
    personality_entry: [PER-0002, PER-0003]
    curated_by: user
    evidence_tier: 4

  - id: ACT-0016
    date: 2026-02-21
    modality: text (Telegram bot)
    activity_type: conversation — knowledge expressed before lookup
    mind_category: knowledge
    source: bot conversation
    question: "what is a black hole"
    grace_mar_phrasing: "A black hole is a place in space where gravity is super strong, and it pulls everything in, even light! It's like a big invisible vacuum."
    knowledge_entry: LEARN-0025
    curated_by: user
    evidence_tier: 3
```

---

## VI. ATTESTATION LOG

Third-party confirmations.

```yaml
attestations: []

# Example entry format:
# - id: ATT-0001
#   date: 2026-02-XX
#   attestor:
#     role: parent
#     name: Mom
#   claim_type: reading
#   claim: "Finished Charlotte's Web, understood main story"
#   evidence_ids: [READ-0001]
```

---

## VII. METRICS

```yaml
total_activities: 16
total_read_entries: 0
total_write_entries: 3
total_create_entries: 8
total_media_entries: 8
total_attestations: 0
last_activity: 2026-02-21
last_update: 2026-02-21
update_source: Pipeline review queue — CANDIDATE-0042 (black holes) approved
```

---

END OF FILE — EVIDENCE PILOT-001 v0.1
